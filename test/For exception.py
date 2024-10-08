import requests
import csv
import concurrent.futures
from bs4 import BeautifulSoup

def return_link_carat_weight(soup):
    base_url = 'https://keyzarjewelry.com'
    return [base_url+a_tag.get('href') for a_tag in soup.find('div', class_='flex flex-wrap gap-2 md:max-w-[350px]').find_all('a')]

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

    link_carat_material = []
    div_tags_contains_link = soup.find_all(class_='cmsi-item-option md:px-1 inline-flex')

    for i in range(4,8):
        link_carat_material.append(base_url+div_tags_contains_link[i].find('a').get('href'))
    hidden_tags = soup.find_all('div', class_='hidden lg:block')
    for a_tag in hidden_tags[1].find_all('a'):
        link_carat_material.append(base_url+a_tag.get('href'))

    for i in link_carat_material:
        yield i

# def return_chunk_index():
#     chunk_index = 0
#     while chunk_index != 326:
#         filename = f'textfiles/chunk_index={chunk_index}.csv'
#         if os.path.exists(filename):
#             with open(filename, 'r') as file:
#                 line_count = sum(1 for _ in file)
#                 if line_count == 100:
#                     chunk_index += 1
#                 else:
#                     break
#         else:
#             break
    
#     return chunk_index

def give_url(link):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }

    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    
    try:
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')
            
            title = soup.h1.string
            description = soup.find_all(class_="cpst-description text-customGray-500")[0].text
            photo_tags = soup.find('div', class_='cpts-desktop-content hidden lg:grid lg:grid-cols-1 lg:gap-2 xl:grid-cols-2 lg:auto-rows-fr').find_all('img')
            photo_link = [img_tag.get('src') for img_tag in photo_tags]
            price_tag = soup.find_all(class_='tangiblee-price text-lg leading-none text-black font-semibold md:text-1.5xl')
            price = price_tag[0].string
            know_your_setting_tags = soup.find_all(class_=['StoneDetailBlock__content-value'])
            width = know_your_setting_tags[0].string
            is_metal = soup.find_all('div', class_='StoneDetailBlock__title-container flex items-center gap-1')[1].find('p').string
            approx = '' if is_metal == 'Metal' else know_your_setting_tags[1].string
            metal = know_your_setting_tags[1].string if is_metal == 'Metal' else know_your_setting_tags[2].string
            metals_tags = soup.find_all(class_="SettingDetailBlock__graph-text flex items-center gap-2")
            gold = metals_tags[0].get_text()
            copper = metals_tags[1].get_text()
            zinc = metals_tags[2].get_text()
            nickle = metals_tags[3].get_text() if len(metals_tags) > 3 else ''
            color_accent_tags = '' if is_metal == 'Metal' else know_your_setting_tags[3].p.string
            clarity_accent_tags = '' if is_metal == 'Metal' else know_your_setting_tags[4].p.string
            profile = know_your_setting_tags[2].string if is_metal == 'Metal' else know_your_setting_tags[5].p.string
            know_your_stone_tags = know_your_setting_tags
            carat = know_your_stone_tags[3].string if is_metal == 'Metal' else know_your_stone_tags[6].string
            color = know_your_stone_tags[4].string if is_metal == 'Metal' else know_your_stone_tags[7].string
            clarity = know_your_stone_tags[5].string if is_metal == 'Metal' else know_your_stone_tags[8].string
            carat_features = soup.find_all(class_='inline text-customGray-500 font-normal ml-1')
            carat_weight = carat_features[0].string
            center_stone_shape = carat_features[1].string
            carat_material = carat_features[2].string

            with open(f'textfilved.csv','a',newline='') as file:

                writer = csv.writer(file)
                writer.writerow([title, price, description, carat_weight, center_stone_shape, carat_material, photo_link, width, approx, metal, gold, copper, zinc, nickle, color_accent_tags, clarity_accent_tags, profile, carat, color, clarity, link])
            # print(title)
            # print(price)
            # print(description)
            # print(carat_weight)
            # print(center_stone_shape)
            # print(carat_material)
            # print(photo_link)
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
            # print(link)
            print('.', end='')
        else:
            print("Failed to extract content from the url :", link)
            with open('textfiles/failed_links.txt','a') as file:
                file.write(link+'\n')
    except Exception as e:
        print(e)
        with open('textfiles/exception_in_exception.txt','a') as file:
            file.write(link+'\n')

def return_url():
    with open('textfiles/exception.txt') as file:
        data = [line.strip() for line in file]
    return [data[i:i+100] for i in range(0, len(data), 100)]

def process_task(task):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(give_url, task)

if __name__=='__main__':
    print("Extracting", end='')

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        executor.map(process_task, return_url())