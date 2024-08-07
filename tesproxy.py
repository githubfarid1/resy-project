# import requests
# from urllib.parse import urlencode

# proxy_params = {
#       'api_key': '6456b40c-0bb9-4277-a24d-82901d1eae56',
#       'url': 'http://httpbin.org/ip', 
#   }

# response = requests.get(
#   url='https://proxy.scrapeops.io/v1/',
#   params=urlencode(proxy_params),
#   timeout=120,
# )
# # breakpoint()
# print('Body: ', response.content)

import requests

api_key = '6456b40c-0bb9-4277-a24d-82901d1eae56'
target_url = 'https://resy.com'
proxy_url = f'http://scrapeops:{api_key}@residential-proxy.scrapeops.io:8181'

proxies = {
    'http': proxy_url,
    'https': proxy_url,
}

response = requests.get(
    url=target_url,
    proxies=proxies,
    timeout=120,
)

print('Body:', response.content)
