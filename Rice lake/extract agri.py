import requests
from bs4 import BeautifulSoup

url = 'https://www.ricelake.com/product-landing-pages/livestock-scales/'
r = requests.get(url)

try:
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'lxml')

        base_url = 'https://www.ricelake.com'
        with open('Rice lake/textfiles/extract agri link.txt','w') as f:
            for div in soup.find_all('div', class_='card-view box col-xs-12 col-sm-6 col-md-4'):
                for a in div.find_all('a'):
                    f.write(base_url+a.get('href')+'\n')
    else:
        print("Failed to get the url :", url)
except Exception as e:
    print(e,':',url)