Installation guide (windows 11):
1. open terminal/powershell
2. go to resy-project folder.
3. create new python environment:
python -m venv venv
4. activate the environment:
venv\Scripts\activate
5. install python components:
pip install -r requirements.txt
6. install playwright:
playwright install
7. run the script:
python main.py
8....

free proxy:
https://scrapeops.io/
user: opencartplugin@gmail.com
pass: workshop21

format residential proxy:
PROXY_TYPE://USERNAME:PASSWORD@PROXY_ADDRESS:PORT_NUMBER
example:
PROXIES = {
    'http': f'http://scrapeops:6456b40c-0bb9-4277-a24d-82901d1eae56@residential-proxy.scrapeops.io:8181',
    'https': f'http://scrapeops:6456b40c-0bb9-4277-a24d-82901d1eae56@residential-proxy.scrapeops.io:8181',
}
