import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
# from dotenv import load_dotenv
import logging
import random
import time
from playwright_stealth import stealth_sync
import logging
import re
import sys
import argparse
import json
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from settings import CLOSE_MESSAGE, CHROME_USER_DATA, CONTINUE_MESSAGE

logging.basicConfig(filename='bot.log', filemode='w', level=logging.INFO,  format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')

def login_to_resy(page, email, password):
    """Login to Resy with enhanced stability and error handling."""
    try:
        page.wait_for_selector('.AnnouncementModal__icon-close', timeout=5000)
        page.click('.AnnouncementModal__icon-close')
    except Exception:
        logging.info("No announcement modal to close.")
    # breakpoint()
    page.click("text=Log in", timeout=30000)
    page.click("text=Use Email and Password instead", timeout=30000)

    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', password)
    
    page.click('[name="login_form"] button', timeout=10000)
    page.evaluate("() => document.fonts.ready")

def random_delay(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))

def reserve_restaurant(page, selected_reservation):
    """Reserve the restaurant with improved error handling and explicit waits."""
    print(f"Trying to reservation...", end=" ", flush=True)
    try:
        selected_reservation.click()
        frame_element = page.wait_for_selector('iframe[title="Resy - Book Now"]', timeout=10000)
        frame = frame_element.content_frame()
        time.sleep(2)
        for i in range(5):
            page.mouse.wheel(0, 15000)
            time.sleep(1)     
        # page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        frame.wait_for_selector('[data-test-id="order_summary_page-button-book"]', timeout=30000)
        frame.query_selector('[data-test-id="order_summary_page-button-book"]').click()
        time.sleep(2)
        if frame.query_selector('[data-test-id="order_summary_page-button-book"]'):
            frame.query_selector('[data-test-id="order_summary_page-button-book"]').click()
        time.sleep(2)
        if frame.query_selector('.StripeForm__header'):
            print("Failed")
            message = frame.query_selector('.StripeForm__header').inner_text().split('\n')[0]
            logging.info(message)
            print(" ".join([message, CONTINUE_MESSAGE]))
            return 0
        print("Passed")
        frame.wait_for_selector('.ConfirmationPage__header', timeout=60000)
        confirmation_message = frame.query_selector('.ConfirmationPage__header').inner_text()
        message1 = f"Reservation confirmation message: {confirmation_message}"
        message2 = "Reservation confirmed."
        logging.info(message1)
        logging.info(message2)
        print(" ".join([message1, message2, CONTINUE_MESSAGE]))
        return 1
    except Exception as e:
        print("error on reserve", e)
        return 2

def print_list_bookings(listbookings):
    print("List of Bookings:")
    for idx, lb in enumerate(listbookings):
        print(f"{idx+1}.", "Restaurant Name:", str(lb['baseurl']).split("/")[-1], "| Period:", lb['period'], "| Date:", lb['date'], "| Time:", lb['time'], "| Seats:", lb['seats'] )

def main():
    parser = argparse.ArgumentParser(description="Resy Bot v1")
    parser.add_argument('-cp', '--chprofile', type=str,help="Chrome Profile Name")
    parser.add_argument('-em', '--email', type=str,help="Resy Email")
    parser.add_argument('-pw', '--password', type=str,help="Resy Password")
    parser.add_argument('-hl', '--headless', type=str,help="Headless Mode")
    parser.add_argument('-ex', '--exemode', type=str,help="Execute Mode")
    args = parser.parse_args()
        
    if not args.chprofile or not args.email or not args.password or not args.headless  or not args.exemode:
        input(" ".join(['Please add complete parameters, ex: python resybotv3 -cp [chrome_profile] -em [email] -pw [password] -hl [headless] -ex [exemode]', CLOSE_MESSAGE]))
        sys.exit()

    chprofile = args.chprofile
    email = args.email
    password = args.password
    headless = args.headless
    headless = True if headless == 'Yes' else False
    single = True if args.exemode == 'Single' else False

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        # More user agents can be added here
    ]
    chrome_user_data = f"{CHROME_USER_DATA}\\{chprofile}"
    try:
        user_agent = random.choice(user_agents)
        with sync_playwright() as pr:
            wargs = []
            # wargs.append('--enable-logging=stderr')
            # list chromium arguments: https://peter.sh/experiments/chromium-command-line-switches/
            wargs.append('--v=1')
            wargs.append('--no-sandbox')
            wargs.append('--enable-features=NetworkService,NetworkServiceInProcess')
            wargs.append('--enable-automation')
            wargs.append('--disable-popup-blocking')
            wargs.append('--disable-web-security')
            wargs.append('--start-maximized')

            wargs.append('--disable-fetching-hints-at-navigation-start')
            wargs.append('--force-first-run')
            wargs.append('--content-shell-hide-toolbar')
            wargs.append('--suppress-message-center-popups')
            wargs.append('--no-first-run')
            wargs.append('--force-show-update-menu-badge')


            # browser =  pr.chromium.launch(headless=headless, args=wargs)
            # breakpoint()
            proxy_server = "http://kpeqkzlp:0sdrl0jganhc@38.154.227.167:5868"
            browser =  pr.chromium.launch_persistent_context(user_data_dir=chrome_user_data, 
                    headless=headless, 
                    args=wargs, 
                    user_agent=user_agent,
                    permissions=['geolocation', 'notifications'],
                    java_script_enabled=True,
                    no_viewport=True,
                    # geolocation=False,
                    # locale='US_en',
                    # bypass_csp=True,
                    # proxy={'server': proxy_server}
                    )

            # def slow_down_route(route, request):
            #     # Slow down network request by 2000 milliseconds.
            #     route.continue_()
            # browser.route('**', slow_down_route)          

            page = browser.pages[0]
            stealth_sync(page)
                            
            page.on("console", lambda msg: logging.debug(f"PAGE LOG: {msg.text}"))
            page.on("pageerror", lambda msg: logging.error(f"PAGE ERROR: {msg}"))
            page.on("response", lambda response: logging.debug(f"RESPONSE: {response.url} {response.status}"))
            page.on("requestfailed", lambda request: logging.error(f"REQUEST FAILED: {request.url} {request.failure}"))

            file = open("commandlist.json", "r")
            commandlist = json.load(file)
            login = False
            commandlist = [{"baseurl": cmd['baseurl'], "date": cmd['date'], "period":cmd['period'], "time": cmd['time'], "seats": cmd['seats'], "reservation_type": cmd['reservation_type'], "status": False} for cmd in commandlist]
            print_list_bookings(commandlist)
            # breakpoint()
            print("")
            message = f"Bot is running... [{chprofile}]"
            logging.info(message)
            print(message)
            maxtrial = 5
            hasrec = True
            trial = 0
            while True:
                random_delay(3, 6)
                if not hasrec or trial >= maxtrial:
                    break
                trial += 1
                for idx, command in enumerate(commandlist):
                    if command['status']:
                        hasrec = False    
                        continue
                    hasrec = True
                    baseurl = command['baseurl']
                    date_wanted = command['date']
                    period_wanted = command['period']
                    time_wanted = command['time']
                    seats = command['seats']
                    reservation_type = command['reservation_type']
                    restaurant_link = f"{str(baseurl).split('?')[0]}?date={date_wanted}&seats={seats}"
                    print(f"Trying going to {restaurant_link}...", end=" ", flush=True)
                    page.goto(restaurant_link, wait_until='domcontentloaded')
                    if  not login and page.query_selector('button.Button--login'):
                        login_to_resy(page, email, password)
                        message = "Logged in successfully."
                    login = True
                    page.evaluate("() => document.fonts.ready")
                    print("Passed")

                    # breakpoint()
                    if page.query_selector('//button[contains(@class,"AnnouncementModal__icon-close")]'):
                        page.query_selector('//button[contains(@class,"AnnouncementModal__icon-close")]').click()
                    if page.query_selector('//div[contains(@class,"ShiftInventory__availability-message")]'):
                        message = page.query_selector(f'//div[contains(@class,"ShiftInventory__availability-message")]').text_content()
                        logging.info(message)
                        print(" ".join([message, CONTINUE_MESSAGE]))
                    else:
                        print(f"Looking for {period_wanted}...", end=" ", flush=True)
                        page.wait_for_selector(f'//div[contains(@class,"VenuePage__Selector-Wrapper")]', timeout=30000)
                        try:
                            page.wait_for_selector(f'//div[contains(@class,"ShiftInventory__shift ShiftInventory__shift--last")]', timeout=2000)
                        except:
                            pass
                        menu = page.query_selector(f'//div[contains(@class,"ShiftInventory__shift")][h2[text()="{period_wanted.lower()}"]]')
                        if not menu:
                            print("Not Found")
                            message = f"No reservation available on {period_wanted}"
                            logging.info(message)
                            print(" ".join([message, CONTINUE_MESSAGE]))
                            continue
                            # sys.exit()
                        print("Found")
                        if page.query_selector('//button[contains(@class,"AnnouncementModal__icon-close")]'):
                            page.query_selector('//button[contains(@class,"AnnouncementModal__icon-close")]').click()
                        # breakpoint()
                        print(f"Looking for {time_wanted} on {reservation_type}...", end=" ", flush=True)
                        selected_reservation = menu.query_selector(f'//button[div[text()="{time_wanted}"]][div[translate(normalize-space(text()),"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")="{str(reservation_type).lower()}"]]')
                        if selected_reservation:
                            print("Found")
                            message = f"Reservation available at {time_wanted} for {seats} people {reservation_type}"
                            logging.info(message)
                            print(message)
                            status = reserve_restaurant(page, selected_reservation)
                            if  status == 1 or status == 2:
                                commandlist[idx]['status'] = True
                            random_delay(3, 6)
                        else:
                            print("Not Found")
                            message = "No reservation available"
                            logging.info(message)
                            print(" ".join([message, CONTINUE_MESSAGE]))
                            continue
                            # sys.exit()

            
           # break  
    except Exception as e:
        # Show all error details in log file
        message = "An error occurred"
        print(message, e)
        logging.exception(message)
        # sys.exit()
        # continue
        # return e


if __name__ == '__main__':
    main()