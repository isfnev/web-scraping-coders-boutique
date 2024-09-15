import requests 
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

with open('Scrap_A and D/textfiles/extract_lab.txt') as file:
    data = [line.strip() for line in file]

base_url = 'https://weighing.andonline.com'

def bring_inner_urls(url):
    r = requests.get(url)
    if r.status_code == 200 :
        soup = BeautifulSoup(r.content, 'lxml')

        with open('Scrap_A and D/textfiles/extract_inner_links.txt','a') as file:
            for h_tags in soup.find_all(class_='heading-4'):
                file.write(base_url+h_tags.find('a').get('href')+'\n')

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(bring_inner_urls, data)