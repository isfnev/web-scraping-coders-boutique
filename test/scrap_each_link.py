import requests
import csv
from bs4 import BeautifulSoup

def return_url():
    with open('textfiles/scraping_keyzar.txt') as file:
        for line in file:
            yield line.strip()

def return_link_carat_weight(soup):
    for a_tag in soup.find('div', class_='flex flex-wrap gap-2 md:max-w-[350px]').find_all('a'):
        yield base_url+a_tag.get('href')

def return_link_center_stone_shape(soup):
    link_center_stone_shape = []
    div_tags_contains_link = soup.find_all(class_='cmsi-item-option md:px-1inline-flex')

    for i in range(4):
        link_center_stone_shape.append(base_url+div_tags_contains_link[i].find('a').get('href'))
    hidden_tags = soup.find_all('div', class_='hidden lg:block')

    for a_tag in hidden_tags[0].find_all('a'):
        link_center_stone_shape.append(base_url+a_tag.get('href'))
    for i in link_center_stone_shape:
        yield i

def return_link_carat_material(soup):

    link_carat_material = []
    div_tags_contains_link = soup.find_all(class_='cmsi-item-option md:px-1 inline-flex')

    for i in range(4,8):
        link_carat_material.append(base_url+div_tags_contains_link[i].find('a').get('href'))
    hidden_tags = soup.find_all('div', class_='hidden lg:block')
    for a_tag in hidden_tags[1].find_all('a'):
        link_carat_material.append(base_url+a_tag.get('href'))

    for i in link_carat_material:
        yield i

gen = return_url()
url = next(gen)
r = requests.get(url)

if r.status_code == 200:

    soup = BeautifulSoup(r.content, 'lxml')
    base_url = 'https://keyzarjewelry.com'
    data = []

    for link_weight in return_link_carat_weight(soup):
        r = requests.get(link_weight)
        soup = BeautifulSoup(r.content, 'lxml')

        for link_shape in return_link_center_stone_shape(soup):
            r = requests.get(link_shape)
            soup = BeautifulSoup(r.content, 'lxml')

            for link_material in return_link_carat_material(soup):
                r = requests.get(link_material)
                soup = BeautifulSoup(r.content, 'lxml')
                print(link_material)
                
                if r.status_code == 200:
                    soup = BeautifulSoup(r.content, 'lxml')
                    title = soup.h1.string
                    price_tag = soup.find_all(class_='tangiblee-price text-lg leading-none text-black font-semibold md:text-1.5xl')
                    price = price_tag[0].string
                    description = soup.find_all(style="font-weight: 400;")[1].string
                    know_your_setting_tags = soup.find_all(class_=['StoneDetailBlock__content-value'])
                    width = know_your_setting_tags[0].string
                    approx = know_your_setting_tags[1].string
                    metal = know_your_setting_tags[2].string
                    metals_tags = soup.find_all(class_="SettingDetailBlock__graph-text flex items-center gap-2")
                    gold = metals_tags[0].get_text()
                    copper = metals_tags[1].get_text()
                    zinc = metals_tags[2].get_text()
                    nickle = metals_tags[3].get_text() if len(metals_tags) > 3 else ''
                    color_accent_tags = know_your_setting_tags[3].p.string
                    clarity_accent_tags = know_your_setting_tags[4].p.string
                    profile = know_your_setting_tags[5].p.string
                    know_your_stone_tags = know_your_setting_tags
                    carat = know_your_stone_tags[6].string
                    color = know_your_stone_tags[7].string
                    clarity = know_your_stone_tags[8].string
                    carat_features = soup.find_all(class_='inline text-customGray-500 font-normal ml-1')
                    carat_weight = carat_features[0].string
                    center_stone_shape = carat_features[1].string
                    carat_material = carat_features[2].string


                    # dict = [title, price, description, carat_weight, center_stone_shape, carat_material, '', width, approx, metal, gold, copper, zinc, nickle, color_accent_tags, clarity_accent_tags, profile, carat, color, clarity
                    # ]

                    with open('work.csv','a',newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([title, price, description, carat_weight, center_stone_shape, carat_material, '', width, approx, metal, gold, copper, zinc, nickle, color_accent_tags, clarity_accent_tags, profile, carat, color, clarity
                    ])

                    # print(title)
                    # print(description)
                    # print(width)
                    # print(approx)
                    # print(metal)
                    # print(gold)
                    # print(copper)
                    # print(zinc)
                    # print(nickle)
                    # print(color_accent_tags)
                    # print(clarity_accent_tags)
                    # print(profile)
                    # print(carat)
                    # print(color)
                    # print(clarity)
                    # print(carat_weight)
                    # print(center_stone_shape)
                    # print(carat_material)
                    # print(link_carat_weight)
                    # print(len(link_carat_weight))
                    # print(link_center_stone_shape)
                    # print(len(link_center_stone_shape))
                    # print(link_carat_material)
                    # print(len(link_carat_material))
                else:
                    print("Failed to extract content from the url :", url)
else:
    print("Failed to extract content from the url :", url)
