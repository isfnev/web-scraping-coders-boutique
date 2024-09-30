from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

import sys
sys.path.append('/home/abhishek/Desktop/web-scraping-coders-boutique')

# from utils.extract_utils import single_test
from utils.extract_utils import return_df_multiple_test
# from utils.extract_utils import return_df_async_test
from utils.time_it import time_it

@time_it
def give_url(url, j):
    print('start extract url', j)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=300000)
            dict = {}
            soup:BeautifulSoup = BeautifulSoup(page.content(), 'lxml')
            page.close()
            browser.close()

            if soup.find(class_='productView-price').text != 'Discontinued':

                dict['title'] = soup.find(class_='productView-title').string

                # dict['brand'] = soup.find(class_='productView-brand').text.strip()
                for idx, i in enumerate(soup.find_all(class_='productView-thumbnail'), 1):
                    dict[f'image {idx}'] = i.find('a').get('href')
                dict['msrp'] = soup.find(class_='price priceLabel price--rrp').string.strip()
                dict['price'] = soup.find(class_='price price--withoutTax').string

                try:
                    dict['saving'] = soup.find(class_='price price--saving').string.strip()
                except Exception as e:
                    print(e)

                calib_option:BeautifulSoup = soup.select('.form-label')
                for i in range(1, len(calib_option)-3):
                    a:BeautifulSoup = calib_option[i].find('a')
                    if a :
                        a.decompose()
                    # string = calib_option[i].text.strip()
                    # print(string)
                    # if string != None:
                    dict[f'calibration optional {i}'] = calib_option[i].text.strip()
                para:int = 1
                docu_count:int = 1
                for tag in soup.find(id='tab-description').children:
                    if tag.name == 'h2':
                        dict['description heading'] = tag.string
                    elif tag.name in ['h3','p']:
                        next_tag:BeautifulSoup = tag.next_sibling
                        if next_tag and next_tag.name != 'ul':
                            next_tag:BeautifulSoup = next_tag.next_sibling
                        if next_tag and next_tag.name == 'ul':
                            for i, li in enumerate(next_tag.find_all('li'), 1):
                                dict[f'Description {tag.text} point {i}'] = li.text
                        elif tag.name == 'p':
                            if tag.find('a'):
                                for a in tag.find_all('a'):
                                    dict[f'Description document link {docu_count}'] = a.get('href')
                                    docu_count += 1
                            elif tag.strong:
                                pass
                            else:
                                dict[f'Description paragraph {para}'] = tag.text
                                para += 1
                youtube_prefix = 'www.youtube.com/embed/'
                player:BeautifulSoup = soup.select('.videoGallery-item')
                if player:
                    for idx, tag in enumerate(player, 1):
                        dict[f'Product video {idx}'] = youtube_prefix+tag.a.get('data-video-id')
                # print(dict['description paragraph'])
                del youtube_prefix
                dict['warranty information'] = soup.find(id='tab-warranty').string.strip()
                product_review = soup.find(id='tab-specs').find('dl').find_all(True)
                for i in range(0, len(product_review), 2):
                    dict['Specification '+product_review[i].string[:-1].strip()] = product_review[i+1].string

                dict['URL'] = url
                base_url = 'https://www.scalesplus.com'
                for idx, tag in enumerate(soup.select('.col-md-4.col-sm-6'), 1):
                    a:BeautifulSoup = tag.a
                    dict[f'accessories link {idx}'] = base_url+a.get('href')
                    dict[f'accessories image {idx}'] = a.img.get('src')
                    dict[f'accessories title {idx}'] = tag.h3.text
                    dict[f'accessories price {idx}'] = tag.h3.next_sibling.text
                del base_url
                print("Done extracting url", j)

                return dict
            with open('scalesplus/textfiles/discontinued1.txt','a') as f:
                f.write(url+'\n')
            return {}
    except Exception as e:
        print(e,":",url)
        with open('scalesplus/textfiles/exception1.txt','a') as f:
            f.write(url+'\n')
        return {}

@time_it
def main()->None:
    urls_path:str = 'scalesplus/textfiles/product links NTEP.txt'
    # urls_path:str = 'scalesplus/textfiles/exception1.txt'
    df_store_path:str = 'scalesplus/textfiles/output1.csv'
    # link_index = 0
    return_df_multiple_test(give_url, df_store_path, urls_path)

if __name__=='__main__':
    main()
