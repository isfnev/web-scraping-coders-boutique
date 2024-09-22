import requests

session = requests.Session()
with open('Proxyscrape Tutorial/screenshot/proxyscrape_premium_http_proxies.txt') as f:
    data = f.readline().strip()
    session.proxies.update({
        'http':data,
        'https':data,
    })

resp = session.get('https://httpbin.org/ip')
print(resp.json())