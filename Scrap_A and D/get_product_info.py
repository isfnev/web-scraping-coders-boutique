import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def make_len_equal(list, m):
    while len(list) < m:
        list.append('')

def get_product_info(url):
    r = requests.get(url)
    try:
        if r.status_code == 200 :
            soup = BeautifulSoup(r.content, 'lxml')
            base_url = 'https://weighing.andonline.com'

            max_length = 0
            
            list_title = []
            list_title.append(soup.find(class_='field field--title').text)
            
            heading_tag = soup.find(class_='heading-5')
            if heading_tag.find('p'):
                heading_tag.find_all('p')[-1].decompose()
        
            
            list_of_content = []
            for p in heading_tag.find_all('p'):
                list_of_content.append(p.text.strip())
            for ul in heading_tag.find_all('ul'):
                for li in ul.find_all('li'):
                    list_of_content.append(li.text.replace('\xa0',''))
            max_length = max( max_length, len(list_of_content))

            try:
                list_of_key_features = set()
            except Exception as e:
                print("Block 3-1 :", e)
            try:
                temp = soup.find('div', class_='grid grid--small-2 grid--medium-3')
            except Exception as e:
                print("Block 3-2 :", e)
            try:
                if temp != None:
                    temp2 = temp.find_all('div')
            
                    if temp2:
                        for div in temp2:
                            list_of_key_features.add(div.text.strip())
            except Exception as e:
                print("Block 3-4 :", e)
            try:        
                list_of_key_features = list(list_of_key_features)
            except Exception as e:
                print("Block 3-5 :", e)
            try:
                max_length = max( max_length, len(list_of_key_features))
            except Exception as e:
                print("Block 3-6 :", e)
            
            list_of_feature = []
            
            temp2 = soup.find_all('div', class_='text-long')
            if len(temp2) >= 2:
                temp = temp2[1]

            for tag in temp.children :
                if tag.name == 'p':
                    list_of_feature.append(tag.get_text().strip())
                elif tag.name == 'ul':
                    for li in tag.find_all('li'):
                        list_of_feature.append(li.text)
            max_length = max( max_length, len(list_of_feature))

            try:
                specification_1 = []
                specification_2 = []
                
                if soup.find('tbody'):
                    for tr in soup.find('tbody').find_all('tr'):
                        tds = tr.find_all('td')
                        specification_1.append(tds[0].text)
                        specification_2.append(tds[1].text)
                else:
                    specification_1.append('')
                    specification_2.append('')

                max_length = max( max_length, len(specification_1))
                max_length = max( max_length, len(specification_2))
            except Exception as e:
                print("Block 5 :", e)
            try:
                accessories_1 = []
                accessories_2 = []
                if len(soup.find_all('tbody')) > 1:
                    temp = soup.find_all('tbody')

                    for tr in temp[1].find_all('tr'):
                        tds = tr.find_all('td')
                        accessories_1.append(tds[0].text)
                        accessories_2.append(tds[1].text)
                if len(accessories_1) == 0:
                    accessories_1.append('')
                    accessories_2.append('')
                max_length = max( max_length, len(accessories_1))
                max_length = max( max_length, len(accessories_2))
            except Exception as e:
                print("Block 6 :", e)
            
            download_tags = soup.find_all('span', class_='file file--mime-application-pdf file--application-pdf')
            n = len(download_tags)//2
            download_col1 = []
            download_col2 = []
            for i in range(n):
                download_col1.append(download_tags[i].find('a').text)
                download_col2.append(download_tags[i].find('a').get('href'))
            max_length = max( max_length, len(download_col1))
            max_length = max( max_length, len(download_col2))
        
            
            # photos
            images_link_list = []
            image_div_tags = soup.find_all('div', class_='field field--field-image-file')
            n = len(image_div_tags)//2
            for i in range(n):
                images_link_list.append(base_url+image_div_tags[i].find('img').get('src'))
            max_length = max( max_length, len(images_link_list))
            
            try:
                make_len_equal(list_title, max_length)
                make_len_equal(list_of_content, max_length)
                make_len_equal(list_of_key_features, max_length)
                make_len_equal(list_of_feature, max_length)
                make_len_equal(specification_1, max_length)
                make_len_equal(specification_2, max_length)
                make_len_equal(accessories_1, max_length)
                make_len_equal(accessories_2, max_length)
                make_len_equal(download_col1, max_length)
                make_len_equal(download_col2, max_length)
                make_len_equal(images_link_list, max_length)
                Url = []
                Url.append(url)
                make_len_equal(Url, max_length)
            except Exception as e:
                print("Block 9 :", e)
            
            df = pd.DataFrame({
                'title':list_title,
                'content':list_of_content,
                'key features':list_of_key_features,
                'features':list_of_feature,
                'specification col one':specification_1,
                'specification col second':specification_2,
                'accessory col one':accessories_1,
                'accessory col second':accessories_2,
                'download text':download_col1,
                'download link':download_col2,
                'images link':images_link_list,
                'URL of website': Url
            })
            # print(title)
            # print(list_of_content)
            # print(list_of_key_features)
            # print(list_of_feature)
            # print(specification_1)
            # print(specification_2)
            # if len(soup.find_all('tbody')) > 1:
            #     print(accessories_1)
            #     print(accessories_2)
            # print(download_col1)
            # print(download_col2)
            # print(images_link_list)
            
            return df
        else:
            print("Failed", url, "with error code :", r.status_code)
            with open('Scrap_A and D/textfiles/get_product_info_failed.txt', 'a') as file:
                file.write(url+'\n')
    except Exception as e:
        print(e)
        with open('Scrap_A and D/textfiles/get_product_info_exception2.txt', 'a') as file:
            file.write(url+'\n')

def process_task(ten_urls):
    df = pd.DataFrame()
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(get_product_info, ten_urls)
        for new_df in results:
            df = pd.concat([df, new_df])
    return df

# url = 'https://weighing.andonline.com/product/borealis-ba-series-semi-microbalances/ba-225te?commerce_product=96'
# get_product_info(url)

# with ThreadPoolExecutor(max_workers=8) as executor:
#     executor.submit(get_product_info, url)
#     executor.map(get_product_info, url)

if __name__=='__main__':
    with open('Scrap_A and D/textfiles/get_product_info_exception.txt') as file:
        urls = [line.strip() for line in file]

    data = [urls[i:i+10] for i in range(0, len(urls), 10)]
    del urls

    df = pd.DataFrame()
    with ProcessPoolExecutor(max_workers=8) as executor:
        results = executor.map(process_task, data)
        for new_df in results:
            df = pd.concat([df, new_df])
    df.to_csv('Scrap_A and D/textfiles/output.csv', index=False)
