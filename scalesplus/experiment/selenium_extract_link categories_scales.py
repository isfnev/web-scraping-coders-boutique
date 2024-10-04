from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import json
import time
import re
import sys

sys.path.append('/home/abhishek/Desktop/web-scraping-coders-boutique/scalesplus')

edge_options = Options()
edge_options.binary_location = "/usr/bin/microsoft-edge-stable"

base_url = 'https://www.scalesplus.com'
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)

urls = [
    # ('https://www.scalesplus.com/cultivation-scales/balances/?Brand=A_AMP_D__Weighing||Adam__Equipment||OHAUS||Rice__Lake__Weighing__Systems','cultivation_balances_scales'),
    ('https://www.scalesplus.com/cultivation-scales/ntep-certified-cultivation-processing-scales/bench-scales/?Brand=A_AMP_D__Weighing||OHAUS','cultivation_bench_scales')
    #,('https://www.scalesplus.com/cultivation-scales/personal-use-scales/?Brand=Adam__Equipment||OHAUS','cultivation_personal_use_scales')
]

for url, category_name in urls:
    driver.get(url)

    # for _ in range(5):
    #     time.sleep(2)
    bottom = driver.find_element(By.CSS_SELECTOR, 'body > footer > div:nth-child(2)')
    ActionChains(driver).scroll_to_element(bottom).perform()
    time.sleep(10)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    i = 0
    tags = soup.select('.productGrid>.product')
    # print(tags[0].select_one('.card-title'))
    list_head = {}
    list = {}
    for tag in tags:
        head = tag.select_one('.card-title').text
        heading = [i for i in head.split(',')[0].split() if i]
        i = -1
        for w in reversed(heading):
            if re.search(r'\d', w):
                break
            i -= 1
        i += 1
        str = ' '.join(heading[i:]).strip()
        if str in list:
            list[str] += 1
            list_head[str].append(head)
        else:
            list[str] = 1
            list_head[str] = [head]

    print(len(list))
    sum = 0
    for i in list:
        print(f'/{i}/ : {list[i]}')
    for i in list_head:
        for j in list_head[i]:
            print(f'\t\t/{i}/ : {j}')
            sum += 1
    print(sum)

    with open(f'scalesplus/json/Data_for_{urls[0][1]}.json','w') as f:
        json.dump(list_head, f)

driver.quit()
