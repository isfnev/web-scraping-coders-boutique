import pandas as pd
import requests
from bs4 import BeautifulSoup

with open('textfiles/scraping_keyzar.txt') as file:
    
        url = file.readline().strip()

        r = requests.get(url)

        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')

            base_url = 'https://keyzarjewelry.com'
            link_carat_weight = []
            for a_tag in soup.find('div', class_='flex flex-wrap gap-2 md:max-w-[350px]').find_all('a'):
                link_carat_weight.append(base_url+a_tag.get('href'))

            link_center_stone_shape = []
            div_tags_contains_link = soup.find_all(class_='cmsi-item-option md:px-1 inline-flex')
            for i in range(4):
                link_center_stone_shape.append(base_url+div_tags_contains_link[i].find('a').get('href'))

            # hidden_tags = soup.find_all('div', class_='hidden lg:block')
            # for a_tag in hidden_tags[0].find_all('a'):
            #     link_center_stone_shape.append(base_url+a_tag.get('href'))

            link_carat_material = []
            for i in range(4,8):
                link_carat_material.append(base_url+div_tags_contains_link[i].find('a').get('href'))

            # for a_tag in hidden_tags[1].find_all('a'):
            #     link_carat_material.append(base_url+a_tag.get('href'))
            data = []

            for link_weight in link_carat_weight:
                r = requests.get(link_weight)
                soup = BeautifulSoup(r.content, 'lxml')
                for link_shape in link_center_stone_shape:
                    r = requests.get(link_shape)
                    soup = BeautifulSoup(r.content, 'lxml')
                    for link_material in link_carat_material:
                        r = requests.get(link_material)
                        soup = BeautifulSoup(r.content, 'lxml')
                        
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
                            nickle = metals_tags[3].get_text()
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

                            dict = {
                                'Title':title,
                                'price':price,
                                'description':description,
                                'carat':carat_weight,
                                'shape':center_stone_shape,
                                'material':carat_material,
                                'photos':'',
                                'width':width,
                                'approx. tc':approx,
                                'metal name':metal,
                                'metal1':gold,
                                'metal2':copper,
                                'metal3':zinc,
                                'metal4':nickle,
                                'color':color_accent_tags,
                                'clarity':clarity_accent_tags,
                                'profile':profile,
                                'carat':carat,
                                'color':color,
                                'clarit':clarity
                            }
                            data.append(dict)
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
            df = pd.DataFrame(data)
            print(df)
        else:
            print("Failed to extract content from the url :", url)
        