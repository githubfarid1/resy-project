# import requests

# response = requests.get(
#   url='https://proxy.scrapeops.io/v1/',
#   params={
#       'api_key': 'f2d43fe5-5bee-41ab-83f9-da70ae59c60a',
#       'url': 'https://quotes.toscrape.com/', 
#   },
# )

# print('Response Body: ', response.content)

import requests

# proxies = {
#   "http": "http://scrapeops:f2d43fe5-5bee-41ab-83f9-da70ae59c60a@residential-proxy.scrapeops.io:8181",
#   "https": "http://scrapeops:f2d43fe5-5bee-41ab-83f9-da70ae59c60a@residential-proxy.scrapeops.io:8181"
# }
# response = requests.get('https://quotes.toscrape.com/', proxies=proxies, verify=False)
# print(response.text)

proxies = {
  "http": "http://14add03797816:36a716f2fd@89.47.126.163:12323",
  "https": "http://14add03797816:36a716f2fd@89.47.126.163:12323"
}
response = requests.get('https://quotes.toscrape.com/', proxies=proxies, verify=False)
print(response.text)


