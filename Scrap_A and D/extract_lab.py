import requests
import json
from bs4 import BeautifulSoup

def extract_link():
    url = 'https://weighing.andonline.com/category/laboratory'
    base_url = 'https://weighing.andonline.com'

    r = requests.get(url)
    if r.status_code == 200 :
        soup = BeautifulSoup(r.content, 'lxml')

        with open('Scrap_A and D/textfiles/extract_lab.txt','a') as file:
            for h_tag in soup.find_all(class_="heading-4"):
                link = base_url+h_tag.find('a').get('href')
                file.write(link+'\n')

        # print(link)
        # print(label)
        # print(img)
    else:
        print("Failed", url, "with error code :", r.status_code)

if __name__=='__main__':
    extract_link()