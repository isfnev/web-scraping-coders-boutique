import requests
from time import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor#, ProcessPoolExecutor

def get_product_info(url):
        r = requests.get(url)
    # try:
        if r.status_code == 200 :
            soup = BeautifulSoup(r.content, 'lxml')
            # base_url = 'https://weighing.andonline.com'

            title = soup.find(class_='field field--title').text
            
            li_list = []
            for li_tag in soup.find(class_='heading-5').find_all('li'):
                li_list.append(li_tag.string)


            print(title)
            print(li_list)
        # else:
        #     print("Failed", url, "with error code :", r.status_code)
        #     with open('Scrap_A and D/textfiles/failed.txt', 'a') as file:
        #         file.write(url+'\n')
    # except Exception as e:
    #     print(e)
    #     with open('Scrap_A and D/textfiles/exception.txt', 'a') as file:
    #         file.write(url+'\n')

# def process_task(ten_urls):
#     with ThreadPoolExecutor(max_workers=8) as executor:
#         executor.map(get_product_info, ten_urls)


start = time()
url = 'https://weighing.andonline.com/product/pv-series-pocket-scale/pv-200?commerce_product=38'
get_product_info(url)
# with ThreadPoolExecutor(max_workers=8) as executor:
    # executor.submit(get_product_info, url)
#     executor.map(get_product_info, url)

print((time()-start)*1000)
# if __name__=='__main__':
#     with open('Scrap_A and D/textfiles/get_product_link.txt') as file:
#         urls = [line.strip() for line in file]

#     data = [urls[i:i+10] for i in range(0, len(urls), 10)]
#     del urls

#     with ProcessPoolExecutor(max_workers=8) as executor:
#         executor.map(process_task, data)