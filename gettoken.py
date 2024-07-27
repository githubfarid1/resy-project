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



def intercept_request(request):
    # print(request.url)
    # we can update requests with custom headers
    if "config" in request.url :
        breakpoint()
        print(request.headers['x-resy-auth-token'])
        # request.headers['x-secret-token'] = "123"
    #     print("patched headers of a secret request")
    # # or adjust sent data
    # if request.method == "POST":
    #     request.post_data = "patched"
    #     print("patched POST request")
    return request


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    # More user agents can be added here
]


chrome_user_data = f"{CHROME_USER_DATA}\\Profile3"
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
    # proxy_server = "http://kpeqkzlp:0sdrl0jganhc@38.154.227.167:5868"
    browser =  pr.chromium.launch_persistent_context(user_data_dir=chrome_user_data, 
            headless=True, 
            args=wargs, 
            user_agent=user_agent,
            permissions=['geolocation', 'notifications'],
            java_script_enabled=True,
            no_viewport=True,
            )


    page = browser.pages[0]
    stealth_sync(page)
    # page.on("request", lambda msg: logging.debug(f"PAGE LOG: {msg.text}"))
    page.on("request", intercept_request)
    page.goto("https://resy.com", wait_until='domcontentloaded')
    breakpoint()



# def main():
#     parser = argparse.ArgumentParser(description="Resy Bot v2")
#     parser.add_argument('-cp', '--chprofile', type=str,help="Chrome Profile Name")
#     args = parser.parse_args()

#     chprofile = args.chprofile

#     user_agents = [
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
#         "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
#         # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
#         # More user agents can be added here
#     ]
#     chrome_user_data = f"{CHROME_USER_DATA}\\{chprofile}"
#     try:
#         user_agent = random.choice(user_agents)
#         with sync_playwright() as pr:
#             wargs = []
#             # wargs.append('--enable-logging=stderr')
#             # list chromium arguments: https://peter.sh/experiments/chromium-command-line-switches/
#             wargs.append('--v=1')
#             wargs.append('--no-sandbox')
#             wargs.append('--enable-features=NetworkService,NetworkServiceInProcess')
#             wargs.append('--enable-automation')
#             wargs.append('--disable-popup-blocking')
#             wargs.append('--disable-web-security')
#             wargs.append('--start-maximized')

#             wargs.append('--disable-fetching-hints-at-navigation-start')
#             wargs.append('--force-first-run')
#             wargs.append('--content-shell-hide-toolbar')
#             wargs.append('--suppress-message-center-popups')
#             wargs.append('--no-first-run')
#             wargs.append('--force-show-update-menu-badge')


#             # browser =  pr.chromium.launch(headless=headless, args=wargs)
#             # breakpoint()
#             proxy_server = "http://kpeqkzlp:0sdrl0jganhc@38.154.227.167:5868"
#             browser =  pr.chromium.launch_persistent_context(user_data_dir=chrome_user_data, 
#                     headless=True, 
#                     args=wargs, 
#                     user_agent=user_agent,
#                     permissions=['geolocation', 'notifications'],
#                     java_script_enabled=True,
#                     no_viewport=True,
#                     )


#             page = browser.pages[0]
#             stealth_sync(page)
#             page.goto("https://resy.com", wait_until='domcontentloaded')
#             breakpoint()
#     except:
#         pass


# if __name__ == '__main__':
#     main()