from bs4 import BeautifulSoup
import json
import asyncio
import sys
import aiofiles
sys.path.append('/home/abhishek/Desktop/web-scraping-coders-boutique')

# from utils.extract_utils import single_test
from utils.extract_utils import return_df_multiple_test
# from utils.extract_utils import return_df_async_test
from utils.time_it import time_it
from utils.json_to_csv import json_to_csv

@time_it
async def give_url(url, j, browser, json_file_path, discontinued_path, exception_path, failed_file_path, categories_checker):
            print('start extract url', j)
    # try:
            page = await browser.new_page()
            await page.goto(url)
            soup:BeautifulSoup = BeautifulSoup(await page.content(), 'lxml')
            await page.close()

            isdiscontinued = soup.find(class_='productView-price')

            if isdiscontinued and isdiscontinued.text.strip() != 'Discontinued':
                dict = {}

                head = soup.find(class_='productView-title').string
                dict['title'] = head
                heading = [i for i in head.split(',')[0].split() if i]
                i = -1
                for w in reversed(heading):
                    if re.search(r'/d', w):
                        break
                    i -= 1
                i += 1
                str = ' '.join(heading[i:])
                for i, j in categories_checker.items():
                    if str in j:
                        dict['Filters'] = i
                # dict['brand'] = soup.find(class_='productView-brand').text.strip()
                for idx, i in enumerate(soup.find_all(class_='productView-thumbnail'), 1):
                    dict[f'image {idx}'] = i.find('a').get('href')
                dict['msrp'] = soup.find(class_='price priceLabel price--rrp').string.strip()
                dict['price'] = soup.find(class_='price price--withoutTax').string

                try:
                    dict['saving'] = soup.find(class_='price price--saving').string.strip()
                except Exception as e:
                    print(e)
                dict['part #'] = soup.find(class_='productView-info-value productView-info-value--sku').text

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
                                candidate_key = f'Description {tag.text} point {i}'
                                candidate_key = candidate_key.split()
                                dict[' '.join(candidate_key)] = li.text
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
                accessaries = soup.find_all(class_='.OptAcsPro-Box')
                for idx, tag in enumerate(accessaries, 1):
                    dict[f'accessaries link {idx}'] = accessaries.a.get('href')
                    dict[f'accessaries img {idx}'] = accessaries.a.img.get('src')
                    h3 = accessaries.h3
                    dict[f'accessaries heading {idx}'] = h3.text()
                    dict[f'accessaries price {idx}'] = h3.next_sibling.text()

                print("Done extracting url", j)
                Keys = [i for i in dict.keys()]
                Keys.sort()
                for i in Keys:
                    print(i)

                async with aiofiles.open(json_file_path, mode='w') as f:
                    dump = json.dumps(dict)
                    await f.write(dump)
            else:
                async with aiofiles.open( discontinued_path, mode ='a') as f:
                    await f.write(url)
    # except Exception as e:
    #     print(e,":",url)
    #     with open(exception_path,'a') as f:
    #         f.write(url+'\n')

@time_it
async def main(category_name=None)->None:
    category_name = 'single_url'
    save_csv_path = f'scalesplus/csv_file/output_{category_name}.csv'
    json_file_path = f'scalesplus/json/output_{category_name}.json'
    failed_file_path = f'scalesplus/failed_file_path/failed_{category_name}.txt'
    urls_path:str = f'scalesplus/product links/product links {category_name.capitalize()}.txt'
    discontinued_path = f'scalesplus/discontinued/discontinued_{category_name}.txt'
    exception_path = f'scalesplus/exception/exception_{category_name}.txt'

    await return_df_multiple_test(give_url, urls_path, json_file_path, discontinued_path, exception_path, failed_file_path)
    json_to_csv(json_file_path, save_csv_path)

if __name__=='__main__':
    asyncio.run(main())
