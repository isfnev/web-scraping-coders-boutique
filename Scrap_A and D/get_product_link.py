import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def get_product_link(url):
    r = requests.get(url)
    try:
        if r.status_code == 200 :
            soup = BeautifulSoup(r.content, 'lxml')
            base_url = 'https://weighing.andonline.com'

            a_tag_container_tag = soup.find_all(class_='field field--title')
            with open('Scrap_A and D/textfiles/get_product_link.txt', 'a') as file:
                for i in range(1, len(a_tag_container_tag)):
                    file.write(base_url+a_tag_container_tag[i].find('a').get('href')+'\n')
        else:
            print("Failed", url, "with error code :", r.status_code)
            with open('Scrap_A and D/textfiles/failed.txt', 'a') as file:
                file.write(url+'\n')
    except Exception as e:
        print(e)
        with open('Scrap_A and D/textfiles/exception.txt', 'a') as file:
            file.write(url+'\n')

if __name__=='__main__':
    with open('Scrap_A and D/textfiles/extract_inner_links.txt') as file:
        data = [line.strip() for line in file]

    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(get_product_link, data)