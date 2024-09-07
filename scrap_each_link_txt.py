from bs4 import BeautifulSoup
import requests
# import time

with open('textfiles/scraping_keyzar.txt') as file:
    url = file.readline().strip()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

response = requests.get(url, headers=headers)
file = open('work.csv','w')

if response.status_code == 200:        
    soup = BeautifulSoup(response.content, 'html.parser')

    # h1 tag for title
    print(soup.h1.string)

    # for description
    description_tag = soup.find_all(style="font-weight: 400;")
    print(description_tag[1].string)

    # list of all possible options
    list_carat_weight = ['1','1-5','2','2-5','3']
    list_carat_shape = ['round','oval','pear','cushion']
    list_carat_material = ['14k-white-gold','14k-yellow-gold','14k-rose-gold','platinum']

    # width in know your settings
    know_your_setting_tags = soup.find_all(class_=['StoneDetailBlock__content-value'])
    print(know_your_setting_tags[0].string)

    # Approx. TCW in know your settings
    print(know_your_setting_tags[1].string)

    # metal in know your settings
    print(know_your_setting_tags[2].string)

    # metal in know your settings
    # print(know_your_setting_tags[3].string)

    # all metal percentage
    metals_tags = soup.find_all(class_="SettingDetailBlock__graph-text flex items-center gap-2")
    print(metals_tags[0].get_text())
    print(metals_tags[1].get_text())
    print(metals_tags[2].get_text())
    print(metals_tags[3].get_text())

    #accent gems
    color_accent_tags = know_your_setting_tags[3].p.string
    print(color_accent_tags)

    clarity_accent_tags = know_your_setting_tags[4].p.string
    print(clarity_accent_tags)

    profile = know_your_setting_tags[5].p.string
    print(profile)

    # know your stone
    know_your_stone_tags = know_your_setting_tags
    print(know_your_stone_tags[6].string)
    print(know_your_stone_tags[7].string)
    print(know_your_stone_tags[8].string)

    for weight in list_carat_weight:
        for shape in list_carat_shape:
            for material in list_carat_material:
                variable_url = url
                variable_url = variable_url.replace(list_carat_weight[0], weight)
                variable_url = variable_url.replace(list_carat_shape[0], shape)
                variable_url = variable_url.replace(list_carat_material[0], material)
                print("Url =======", variable_url)
                print(type(variable_url))

                response = requests.get(url, headers=headers)
                if response.status_code == 200:        
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # for price
                    price_tag = soup.find_all(class_='tangiblee-price text-lg leading-none text-black font-semibold md:text-1.5xl')
                    print(price_tag[0].string)

                    current_row = ''
                    # if weight == list_carat_weight and shape == list_carat_shape and material == list_carat_material:
                    current_row += soup.h1.string+','
                    # else:
                        # current_row += ','
                    current_row += price_tag[0].string+','
                    # if weight == list_carat_weight and shape == list_carat_shape and material == list_carat_material:
                    current_row += description_tag[1].string+','
                    # else:
                    #     current_row += ','
                    
                    current_row += weight+','
                    current_row += shape+','
                    current_row += material+','

                    # if weight == list_carat_weight and shape == list_carat_shape and material == list_carat_material:

                    current_row += know_your_setting_tags[0].string+','
                    current_row += know_your_setting_tags[1].string+','
                    current_row += know_your_setting_tags[2].string+','

                    current_row += metals_tags[0].get_text()+','
                    current_row += metals_tags[1].get_text()+','
                    current_row += metals_tags[2].get_text()+','
                    current_row += metals_tags[3].get_text()+','


                    #accent gems
                    current_row += color_accent_tags+','
                    current_row += clarity_accent_tags+','
                    current_row += profile+','

                    # know your stone
                    current_row += know_your_stone_tags[6].string+','
                    current_row += know_your_stone_tags[7].string+','
                    current_row += know_your_stone_tags[8].string+','
                    # else:
                    #     current_row += ','*13
                    current_row +='\n'
                    file.write(current_row)
                
                else:
                    print(f"Failed to retrieve content. Status code: {response.status_code}")
                # time.sleep(3)
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")

file.close()