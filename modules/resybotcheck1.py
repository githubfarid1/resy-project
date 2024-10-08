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
from pywifi import PyWiFi, const, Profile
import subprocess
from database import Database

db = Database("db.sqlite3")

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from settings import CLOSE_MESSAGE, CONTINUE_MESSAGE, TRY_MESSAGE, MIN_IDLE_TIME, MAX_IDLE_TIME

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

def connect_to_wifi(ssid, password):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    
    # Remove all existing profiles
    iface.remove_all_network_profiles()
    
    # Create a new profile
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password
    
    # Add and connect to the new profile
    iface.add_network_profile(profile)
    iface.connect(profile)
    
    # Wait for connection
    import time
    time.sleep(10)
    
    # Check connection status
    if iface.status() == const.IFACE_CONNECTED:
        return f"Successfully connected to {ssid}"
    else:
        return "Failed to connect"

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
    parser = argparse.ArgumentParser(description="Resy Bot Check")

    parser.add_argument('-id', '--id', type=str,help="Record ID")

    args = parser.parse_args()
    data = db.getCheck(id=args.id)
    id = data[0]
    url = data[1]
    startdate = data[2]
    enddate = data[3]
    seats = data[4]
    nonstop = data[5]
    proxy = data[6]
    minidle = data[7]
    maxidle = data[8]
    retsecs = data[9]
    start_date = datetime.strptime(startdate, '%Y-%m-%d').date()
    end_date = datetime.strptime(enddate, '%Y-%m-%d').date()
    get_api_key()
    file = open("logs/api_key.log", "r")
    api_key = file.read()
    https_proxy = ''
    http_proxy = ''
    if  proxy != '<Not Set>':
        proxy = db.getProxy(proxy)
        http_proxy = proxy[2]
        https_proxy = proxy[3]
    resy_config = {"api_key": api_key, "token": '', "payment_method_id": 999999, "email":'', "password":'', "http_proxy": http_proxy, "https_proxy": https_proxy, "retry_count": 1, "seconds_retry": float(retsecs)}
    venue_id = get_venue_id(resy_config=resy_config, urladdress=url)
    strdateyesterday = datetime.strftime(datetime.now()-timedelta(days=1), '%Y-%m-%d')
    flog = open(f"logs/checking_{id}.log", "w")
    # breakpoint()
    # stoptime = datetime.now() + timedelta(minutes = 5)
    try:
        while True:
            # if datetime.now() >= stoptime:
            #     stoptime = datetime.now() + timedelta(minutes = 5)
            #     if "DilarangMasuk" in str(subprocess.check_output(["netsh", "wlan", "show", "interfaces"])):
            #         testconnect = connect_to_wifi('Redmi Note 9T', '358358358')
            #     else:
            #         testconnect = connect_to_wifi('DilarangMasuk', '358358358')
            #     print(testconnect)
            #     flog.write(testconnect)

            tmpstr = f"Restaurant URL: {url}"
            print(tmpstr)
            flog.write(tmpstr + "\n")
            tmpstr = f"Range Date: {startdate} - {enddate}"
            print(tmpstr)
            flog.write(tmpstr + "\n")
            tmpstr = f"Seats Count: {seats}"
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
                "party_size": int(seats),
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
            if nonstop == "No":
                break
            else:
                tmpstr = "____________________________Repeat________________________________"
                print(tmpstr)
                flog.write(tmpstr + "\n\n")
                sleeptime = random_delay(int(minidle), int(maxidle))
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
