import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

def make_len_equal(list, m):
    while len(list) < m:
        list.append('')

def generator():
    for i in range(1000):
        yield i

def give_url(url):
        r = requests.get(url)

    # try:
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')
            list_url = [url]
            gen = generator()
            base_url = 'https://www.ricelake.com'
            max_length = 0
            first_container = soup.find(class_='col-xs-12 col-sm-6 col-md-5 page-content-section')
            list_title = []
            list_title.append(first_container.find('h1').text)
            max_length = max( max_length, len(list_title))

            try:
                list_content = []
                for li in first_container.find_all('li'):
                    list_content.append(li.text)
                max_length = max( max_length, len(list_content))
                print(next(fan))
            except Exception as e:
                print(f"Block {next(gen)} :", e)
            try:
                list_images = []
                for button in soup.find(id='product-thumbnails').find_all('button'):
                    list_images.append(base_url+button.get('data-src'))
                max_length = max( max_length, len(list_images))
                print(next(fan))
            except Exception as e:
                print(f"Block {next(gen)} :", e)
            try:
                list_description = []
                list_iframe = []
                for tag in soup.find(id='product-description').children:
                    if tag.name == 'div':
                        for iframe in tag.find_all('iframe'):
                            list_iframe.append(iframe.get('src'))
                    else:
                        list_description.append(tag.text)
                list_description = [i.strip() for i in list_description if i.strip()]
                max_length = max( max_length, len(list_description))
                max_length = max( max_length, len(list_iframe))
                print(next(fan))
            except Exception as e:
                print(f"Block {next(gen)} :", e)
            try:
                list_specification_p_value = []
                list_specification_p_key = []
                list_specification_heading = []

                for spec in soup.find_all(class_='specification-block product-table'):
                    list_specification_heading.append(spec.find_previous_sibling().get_text(strip=True))
                    for p in spec.find_all('p'):
                        strong = p.find('strong')
                        if strong:
                            list_specification_heading.append('')
                            list_specification_p_key.append(strong.text)
                            p.find('strong').decompose()
                            list_specification_p_value.append(p.get_text(separator=' ', strip=True))
                max_length = max( max_length, len(list_specification_p_key))
                max_length = max( max_length, len(list_specification_p_value))
                max_length = max( max_length, len(list_specification_heading))

            # print(list_title)
            # print(list_content)
            # print(list_images)
            # print(list_description)
            # print(list_iframe)
            # print(list_specification_p_value)
            # print(list_specification_p_key)
            # print(list_specification_heading)
            # print(len(list_title))
            # print(len(list_content))
            # print(len(list_images))
            # print(len(list_description))
            # print(len(list_iframe))
            # print(len(list_specification_p_value))
            # print(len(list_specification_p_key))
            # print(len(list_specification_heading))
            except Exception as e:
                print(f"Block {next(gen)} :", e)
            try:
                make_len_equal(list_title, max_length)
                make_len_equal(list_content, max_length)
                make_len_equal(list_images, max_length)
                make_len_equal(list_description, max_length)
                make_len_equal(list_iframe, max_length)
                make_len_equal(list_url, max_length)
                make_len_equal(list_specification_p_value, max_length)
                make_len_equal(list_specification_p_key, max_length)
                make_len_equal(list_specification_heading, max_length)

                df = pd.DataFrame({
                    'title' : list_title,
                    'content' : list_content,
                    'images' : list_images,
                    'description' : list_description,
                    'video link' : list_iframe,
                    'specification_heading':list_specification_heading,
                    'specification_key' : list_specification_p_key,
                    'specification_value' : list_specification_p_value,
                    'Url' : list_url
                })
                return df
            except Exception as e:
                print(f"Block {next(gen)} :", e)
    #     else:
    #         print("Failed to get the url :", url)
    #         with open('Rice lake/textfiles/failed.txt','a') as f:
    #             f.write(url+'\n')
    # except Exception as e:
    #     print('Exception :', e)
    #     with open('Rice lake/textfiles/exception1.txt','a') as f:
    #         f.write(url+'\n')

url = 'https://www.ricelake.com/products/mas-p-portable-animal-scale'
give_url(url)

# def get_urls():
#     with open('Rice lake/textfiles/extract agri link.txt') as f:
#         data = [line.strip() for line in f]
#     return data

# def main():
#     urls = get_urls()
#     df = pd.DataFrame()
#     with ThreadPoolExecutor(max_workers = 8) as executor:
#         result = executor.map(give_url, urls)
#         for new_df in result:
#             df = pd.concat([df, new_df])
#     df.to_csv('Rice lake/textfiles/new_output.csv', index=False)

# if __name__=='__main__':
#     main()