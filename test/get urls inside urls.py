import requests
import concurrent.futures
from bs4 import BeautifulSoup

def return_link_carat_weight(soup):
    base_url = 'https://keyzarjewelry.com'
    for a_tag in soup.find('div', class_='flex flex-wrap gap-2 md:max-w-[350px]').find_all('a'):
        yield base_url+a_tag.get('href')

def return_link_center_stone_shape(soup):
    base_url = 'https://keyzarjewelry.com'
    link_center_stone_shape = []
    div_tags_contains_link = soup.find_all(class_='cmsi-item-option md:px-1 inline-flex')

    for i in range(4):
        link_center_stone_shape.append(base_url+div_tags_contains_link[i].find('a').get('href'))

    hidden_tags = soup.find_all('div', class_='hidden lg:block')
    for a_tag in hidden_tags[0].find_all('a'):
        link_center_stone_shape.append(base_url+a_tag.get('href'))

    for i in link_center_stone_shape:
        yield i

def return_link_carat_material(soup):
    base_url = 'https://keyzarjewelry.com'

    div_tags_contains_link = soup.find_all(class_='cmsi-item-option md:px-1 inline-flex')

    with open('urls in urls.txt','a') as file:
        for i in range(4,8):
            file.write(base_url+div_tags_contains_link[i].find('a').get('href')+'\n')
            print('.', end='')
        hidden_tags = soup.find_all('div', class_='hidden lg:block')
        for a_tag in hidden_tags[1].find_all('a'):
            file.write(base_url+a_tag.get('href')+'\n')
            print('.', end='')

def return_url():
    with open('textfiles/scraping_keyzar.txt') as file:
        return [line.strip() for line in file]

def store_url(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}
    r = requests.get(url,headers=headers)

    if r.status_code == 200:

        soup = BeautifulSoup(r.content, 'lxml')

        for link_weight in return_link_carat_weight(soup):
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,                  like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}
            r = requests.get(link_weight, headers=headers)
            soup = BeautifulSoup(r.content, 'lxml')

            for link_shape in return_link_center_stone_shape(soup):
                headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}
                r = requests.get(link_shape, headers=headers)
                soup = BeautifulSoup(r.content, 'lxml')

                return_link_carat_material(soup)
    else:
        print("Failed to extract content from the url :", url)

def main():
    urls = return_url()
    print('Extracting urls', end='')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(store_url, urls)

if __name__=='__main__':
    main()