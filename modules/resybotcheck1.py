import argparse
import json
from resy_bot2.logging import logging
import os
import sys
from resy_bot2.models import ResyConfig, TimedReservationRequest
from resy_bot2.manager import ResyManager
import requests
from user_agent import generate_user_agent
from datetime import datetime, date, timedelta
import random
import time
from requests import Session, HTTPError
from resy_bot2.errors import NoSlotsError, ExhaustedRetriesError, Get500Error
from datetime import datetime, timedelta
from prettytable import PrettyTable
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from settings import CLOSE_MESSAGE, CONTINUE_MESSAGE, TRY_MESSAGE, MIN_IDLE_TIME, MAX_IDLE_TIME

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

def random_delay(min_seconds, max_seconds):
    return random.uniform(min_seconds, max_seconds)

def intercept_request(request):
    if "https://api.resy.com/2/config" in request.url:
        try:
            api_key=str(request.headers['authorization']).replace('ResyAPI api_key=', "").replace('"','')
            f = open("logs/api_key.log", "w")
            f.write(api_key)
        except:
            return request        
    return request

def get_api_key():
    with sync_playwright() as pr:
        wargs = []
        wargs.append('--v=1')
        wargs.append('--no-sandbox')
        wargs.append('--enable-features=NetworkService,NetworkServiceInProcess')
        wargs.append('--enable-automation')
        wargs.append('--disable-popup-blocking')
        wargs.append('--disable-web-security')
        wargs.append('--start-maximized')
        
        browser =  pr.chromium.launch(headless=True, args=wargs)
        page = browser.new_page()
        stealth_sync(page)
        page.on("request", lambda request: intercept_request(request))

        res = page.goto("https://resy.com", wait_until="domcontentloaded", timeout=20000)
        
def check_now(resy_config: dict, reservation_config: dict) -> str:
    config_data = resy_config
    reservation_data = reservation_config
    config = ResyConfig(**config_data)
    manager = ResyManager.build(config)
    timed_request = TimedReservationRequest(**reservation_data)
    # breakpoint()
    return manager.check_reservation_with_retries(timed_request.reservation_request)

def get_venue_id(resy_config: dict, urladdress: str) -> str:
    config_data = resy_config
    config = ResyConfig(**config_data)
    manager = ResyManager.build(config)
    return manager.get_venue_id(urladdress)
    
def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days)
    for n in range(days+1):
        yield start_date + timedelta(n)

def main():
    parser = argparse.ArgumentParser(description="Resy Bot v4")
    parser.add_argument('-u', '--url', type=str,help="Base URL")
    parser.add_argument('-sd', '--startdate', type=str,help="Date Start")
    parser.add_argument('-ed', '--enddate', type=str,help="Date End")
    parser.add_argument('-s', '--seats', type=str,help="Seats count")
    parser.add_argument('-up', '--proxy', type=str,help="Use Proxy")
    parser.add_argument('-ns', '--nonstop', type=str,help="Non Stop Checking")
    parser.add_argument('-id', '--id', type=str,help="Record ID")
    parser.add_argument('-mn', '--minidle', type=str,help="Min Idle Time")
    parser.add_argument('-mx', '--maxidle', type=str,help="Max Idle Time")

    args = parser.parse_args()
    start_date = datetime.strptime(str(args.startdate), '%Y-%m-%d').date()
    end_date = datetime.strptime(str(args.enddate), '%Y-%m-%d').date()
    get_api_key()
    file = open("logs/api_key.log", "r")
    api_key = file.read()
    https_proxy = ''
    http_proxy = ''
    if args.proxy != '<Not Set>':
        file = open("proxylist.json", "r")
        listvalue = json.load(file)
        proxy = [prof for prof in listvalue if prof['profilename']==args.proxy]
        http_proxy = proxy[0]['http_proxy']
        https_proxy = proxy[0]['https_proxy']
    resy_config = {"api_key": api_key, "token": '', "payment_method_id": 999999, "email":'', "password":'', "http_proxy":http_proxy, "https_proxy": https_proxy, "retry_count": 1}
    venue_id = get_venue_id(resy_config=resy_config, urladdress=str(args.url))
    strdateyesterday = datetime.strftime(datetime.now()-timedelta(days=1), '%Y-%m-%d')
    flog = open(f"logs/checking_{str(args.id)}.log", "w")
    # breakpoint()
    try:
        while True:
            tmpstr = f"Restaurant URL: {args.url}"
            print(tmpstr)
            flog.write(tmpstr + "\n")
            tmpstr = f"Range Date: {args.startdate} - {args.enddate}"
            print(tmpstr)
            flog.write(tmpstr + "\n")
            tmpstr = f"Seats Count: {args.seats}"
            print(tmpstr)
            flog.write(tmpstr + "\n")
            print("")
            flog.write("\n")
            for single_date in daterange(start_date, end_date):
                searchdate = single_date.strftime("%Y-%m-%d")
                print(searchdate)
                flog.write(searchdate + "\n")
                reservation_config = {
                "reservation_request": {
                "party_size": int(args.seats),
                "venue_id": venue_id,
                "window_hours": 0,
                "prefer_early": False,
                "ideal_date": searchdate,
                #   "days_in_advance": 14,
                "ideal_hour": 5,
                "ideal_minute": 0,
                "preferred_type": None
                },
                "expected_drop_hour": 9,
                "expected_drop_minute": 0, 
                "expected_drop_second": 0, 
                "expected_drop_year":strdateyesterday.split("-")[0],
                "expected_drop_month":strdateyesterday.split("-")[1],
                "expected_drop_day":strdateyesterday.split("-")[2],
                }
                try:
                    myTable = PrettyTable(["TIME","RESER. TYPE"])
                    myTable.align ="l"
                    slots = check_now(resy_config=resy_config, reservation_config=reservation_config)
                    if len(slots) != 0:
                        tmpstr = f"Found {len(slots)} Slots"
                        print(tmpstr)
                        flog.write(tmpstr + "\n")
                    for slot in slots:
                        # time.sleep(5)
                        dtime = str(slot.config.token).split("/")[-3][:5]
                        reservation = str(slot.config.token).split("/")[-1]
                        myTable.add_row([dtime, reservation])
                    # print(venue_id)
                    print(myTable)
                    flog.write(str(myTable))
                except (HTTPError, ExhaustedRetriesError, NoSlotsError) as e:
                    tmpstr = str(e)
                    print(tmpstr)
                    flog.write(tmpstr + "\n")
                except Get500Error as e:
                    tmpstr = str(e)
                    print(tmpstr)
                    flog.write(tmpstr + "\n")

                except Exception as e:
                    print("Bot Error:", str(e))
                print(datetime.now())
                flog.write("\n" + str(datetime.now()) +"\n")
                print("")
                flog.write("\n")
            if str(args.nonstop) == "No":
                break
            else:
                tmpstr = "____________________________Repeat________________________________"
                print(tmpstr)
                flog.write(tmpstr + "\n\n")
                sleeptime = random_delay(int(args.minidle), int(args.maxidle))
                print("Idle Time", int(sleeptime), "seconds")
                time.sleep(sleeptime)
        tmpstr = "Process Finished..."
        flog.write(tmpstr+"\n")
        flog.close()
        input(tmpstr)
    except:
        flog.close()
    
    sys.exit()

if __name__ == "__main__":
    main()
