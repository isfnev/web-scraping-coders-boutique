import requests
from bs4 import BeautifulSoup
import pandas as pd

import sys
sys.path.append('/home/abhishek/Desktop/web-scraping-coders-boutique')

from utils.extract_utils import single_test

dict = {}

def give_url(url):
    r = requests.get(url)

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'lxml')
        if soup.find(class_='productView-price').text != 'Discontinued':
            dict['title'] = soup.find(class_='productView-title').string
            dict['brand'] = soup.find(class_='productView-brand').text.strip()
            for idx, i in enumerate(soup.find_all(class_='productView-thumbnail'), 1):
                dict[f'image_{idx}']=i.find('a').get('href')
            dict['msrp'] = soup.find(class_='price priceLabel price--rrp').string.strip()
            dict['price'] = soup.find(class_='price price--withoutTax').string
            dict['saving'] = soup.find(class_='price price--saving').string.strip()

            calib_option = soup.select('.form-label')
            for i in range(1, 4):
                a = calib_option[i].find('a')
                if a :
                    a.decompose()
                # string = calib_option[i].text.strip()
                # print(string)
                # if string != None:
                dict[f'calibration optional (radio{i})'] = calib_option[i].text.strip()
            for tag in soup.find(id='tab-description').children:
                if tag.name == 'h2':
                    dict['description heading'] = tag.string
                elif tag.name == 'p':
                    if tag.find('a'):
                        for i, a in enumerate(tag.find_all('a'), 1):
                            dict[f'{a.string} link {i}'] = a.get('href')
                    else:
                        dict['description paragraph'] = tag.text
                elif tag.name == 'h3':
                    next_tag = tag.next_sibling
                    if next_tag != 'ul':
                        next_tag = next_tag.next_sibling
                    if next_tag.name == 'ul':
                        for i, li in enumerate(next_tag.find_all('li'), 1):
                            dict[f'{tag.text} point {i}'] = li.text
            dict['warranty information'] = soup.find(id='tab-warranty').string.strip()

        return pd.DataFrame([dict])

def main():
    urls_path = 'scalesplus/textfiles/111 links.txt'
    df_store_path = 'scalesplus/textfiles/output.csv'
    single_test(give_url, df_store_path, urls_path)

if __name__=='__main__':
    main()