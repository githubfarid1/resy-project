import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import logging
import random
import time
from playwright_stealth import stealth_sync
import logging
import re
import sys
import argparse
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from settings import RESY_EMAIL, RESY_PASSWORD, HEADLESS

load_dotenv('settings.env')

# email = os.getenv('RESY_EMAIL')
# password = os.getenv('RESY_PASSWORD')
email = RESY_EMAIL
password = RESY_PASSWORD

# PW_TEST_SCREENSHOT_NO_FONTS_READY = 1
# headless = True if os.getenv('HEADLESS') == 'yes' else False
headless = True if HEADLESS == 'yes' else False
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
    # breakpoint()
    # page.request.post("https://api.resy.com/3/auth/password", headers=headers, data=payload,)
    
    page.click('[name="login_form"] button', timeout=10000)
    # time.sleep(10)
    # page.get_by_role("button", name=re.compile("continue", re.IGNORECASE)).click()
    # page.click("text=Continue", timeout=5000)
    # page.click('/html/body/div[8]/div/div/div/div/div[2]/div[2]/div/form/div/button', timeout=5000)
    
    # breakpoint()
    # page.evaluate("document.querySelector('[name=\"login_form\"] button').click()")
    page.evaluate("() => document.fonts.ready")
    # breakpoint()
    
    # page.screenshot(path='debugging_photos/screenshot2.png')
    # logging.info("Logged in and screenshot taken.")

def random_delay(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))

def reserve_restaurant(page, selected_reservation):
    """Reserve the restaurant with improved error handling and explicit waits."""
    try:
        selected_reservation.click()
        breakpoint()
        frame_element = page.wait_for_selector('iframe[title="Resy - Book Now"]', timeout=10000)
        frame = frame_element.content_frame()
        frame.wait_for_selector('[data-test-id="order_summary_page-button-book"]', timeout=10000).click()
        # breakpoint()
        confirmation_message = frame.query_selector('.ConfirmationPage__header').inner_text()
        message1 = f"Reservation confirmation message: {confirmation_message}"
        message2 = "Reservation confirmed."
        logging.info(message1)
        logging.info(message2)
        input(" ".join([message1, message2]))
        sys.exit()
        # page.evaluate("() => document.fonts.ready")
        # page.screenshot(path='debugging_photos/screenshot3.png')
    except Exception as e:
        message = "Failed to complete reservation"
        logging.exception(message)
        input(message)
        sys.exit()


def main():
    parser = argparse.ArgumentParser(description="Resy Bot v1")
    parser.add_argument('-u', '--url', type=str,help="Base URL")
    parser.add_argument('-d', '--date', type=str,help="Date wanted")
    parser.add_argument('-t', '--time', type=str,help="Time wanted")
    parser.add_argument('-s', '--seats', type=str,help="Seats count")
    parser.add_argument('-p', '--period', type=str,help="period type")
    parser.add_argument('-r', '--reservation', type=str,help="Reservation type")

    args = parser.parse_args()
        
    if not args.url or not args.date or not args.time or not args.seats or not args.period or not args.reservation:
        input('Please add complete parameters, ex: python resybotv1 -u [url] -d [dd-mm-yyyy] -t [h:m am/pm] -s [seats_count] -p [period] -r [reservation_type]')
        sys.exit()

    # restaurants = ['carat-fine-indian-cuisine', 'marcos-oyster-bar-and-grill', 'ebeneezers-kebabs-and-pizzeria-8847']
    # date_wanted = "2024-06-30"
    # seats = "2"
    # time_wanted = "6:00 PM"
    # period_wanted = "Dinner"
    # reservation_type = "Table"
    # restaurant_link = f"https://resy.com/cities/hong-kong/venues/{restaurants[1]}?date={date_wanted}&seats={seats}"

    date_wanted = args.date
    seats = args.seats
    time_wanted = args.time
    period_wanted = args.period
    reservation_type = args.reservation
    restaurant_link = f"{args.url.split('?')[0]}?date={date_wanted}&seats={seats}"

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        # More user agents can be added here
    ]
    
    while True:
        try:
            user_agent = random.choice(user_agents)
            with sync_playwright() as pr:
                wargs = []
                # wargs.append('--enable-logging=stderr')
                wargs.append('--v=1')
                wargs.append('--no-sandbox')
                wargs.append('--enable-features=NetworkService,NetworkServiceInProcess')
                wargs.append('--enable-automation')
                wargs.append('--disable-popup-blocking')
                wargs.append('--disable-web-security')
                wargs.append('--start-maximized')


                browser =  pr.chromium.launch(headless=headless, args=wargs)
                proxy_server = "http://kpeqkzlp:0sdrl0jganhc@38.154.227.167:5868"

                context = browser.new_context(
                    user_agent=user_agent,
                    # viewport={'width': random.randint(1200, 1920), 'height': random.randint(900, 1080)},
                    # viewport={'width': 1920, 'height': 1080},
                    permissions=['geolocation', 'notifications'],
                    java_script_enabled=True,
                    no_viewport=True,
                    # bypass_csp=True,
                    # locale='US_en',
                    # geolocation=False,
                    #proxy = {
                        #'server': proxy_server
                    #}
                )
                page = context.new_page()
                stealth_sync(page)
                            
                page.on("console", lambda msg: logging.debug(f"PAGE LOG: {msg.text}"))
                page.on("pageerror", lambda msg: logging.error(f"PAGE ERROR: {msg}"))
                page.on("response", lambda response: logging.debug(f"RESPONSE: {response.url} {response.status}"))
                page.on("requestfailed", lambda request: logging.error(f"REQUEST FAILED: {request.url} {request.failure}"))
                logging.info("Bot is running...")
                
                page.goto("https://resy.com", wait_until='domcontentloaded', timeout=20000)
                # breakpoint()
                random_delay(2, 5)
                login_to_resy(page, email, password)
                logging.info("Logged in successfully.")
                random_delay(2, 5)
                page.goto(restaurant_link, wait_until='domcontentloaded')
                page.wait_for_timeout(20000)
                page.evaluate("() => document.fonts.ready")
                random_delay(2, 5)
                # page.screenshot(path="debugging_photos/screenshot1.png", timeout=120000)
                # breakpoint()
                page.query_selector('//*[@id="open-but-unavailable-without-future"]')
                if page.query_selector(f'//div[contains(@class,"ShiftInventory__availability-message")]'):
                    message = page.query_selector(f'//div[contains(@class,"ShiftInventory__availability-message")]').text_content()
                    logging.info(message)
                    input(message)
                    sys.exit()
                else:
                    menu = page.wait_for_selector(f'//div[contains(@class,"ShiftInventory__shift")][h2[text()="{period_wanted.lower()}"]]', timeout=30000)
                    selected_reservation = menu.query_selector(f'//button[div[text()="{time_wanted}"]][div[text()="{reservation_type.lower().title()}"]]')
                    if selected_reservation:
                        logging.info(
                            f"Reservation available at {time_wanted} for {seats} people {reservation_type.lower().title()}")
                        reserve_restaurant(page, selected_reservation)
                        random_delay(3, 6)
                    else:
                        message = "No reservation available"
                        logging.info(message)
                        input(message)
                        sys.exit()

                break  
        except Exception as e:
            # Show all error details in log file
            logging.exception("An error occurred")
            # sys.exit()
            continue
            # return e
    


if __name__ == '__main__':
    main()