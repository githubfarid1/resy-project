import requests

headers = {
    # 'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
    # 'cache-control': 'no-cache',
    # 'origin': 'https://resy.com',
    # 'priority': 'u=1, i',
    # 'referer': 'https://resy.com/',
    # 'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'sec-fetch-dest': 'empty',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    # 'x-origin': 'https://resy.com',
    # 'x-resy-auth-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJleHAiOjE3MjU4ODUxNzUsInVpZCI6NTIxNTY3MzcsImd0IjoiY29uc3VtZXIiLCJncyI6W10sImxhbmciOiJlbi11cyIsImV4dHJhIjp7Imd1ZXN0X2lkIjoxNjM2OTgxNTB9fQ.APESw0KvQCRhvHxMJEH5zPD8sfDSdDZgWEemfX-EjDYZB0Z5nedVw3kb49lNxON5tqRJneOIRBghlqEiwIhpjrJDAYGeKi6PXejMfKN66fF462_EuoLaVa56-uHw_gM9fn3jGwRsxVGLwRtahsPf0Zti0zEvofCX95sM4_oFBUdqN9Tf',
    'x-resy-universal-auth': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJleHAiOjE3MjU4ODUxNzUsInVpZCI6NTIxNTY3MzcsImd0IjoiY29uc3VtZXIiLCJncyI6W10sImxhbmciOiJlbi11cyIsImV4dHJhIjp7Imd1ZXN0X2lkIjoxNjM2OTgxNTB9fQ.APESw0KvQCRhvHxMJEH5zPD8sfDSdDZgWEemfX-EjDYZB0Z5nedVw3kb49lNxON5tqRJneOIRBghlqEiwIhpjrJDAYGeKi6PXejMfKN66fF462_EuoLaVa56-uHw_gM9fn3jGwRsxVGLwRtahsPf0Zti0zEvofCX95sM4_oFBUdqN9Tf',
}

params = {
    'lat': '0',
    'long': '0',
    'day': '2024-07-31',
    'party_size': '2',
    'venue_id': '82617',
}

response = requests.get('https://api.resy.com/4/find', params=params, headers=headers)
print(response.json())