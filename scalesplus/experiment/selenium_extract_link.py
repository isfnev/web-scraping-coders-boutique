from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import asyncio
import sys
sys.path.append('/home/abhishek/Desktop/web-scraping-coders-boutique/scalesplus')
from get_product_info import main

edge_options = Options()
edge_options.binary_location = "/usr/bin/microsoft-edge-stable"

base_url = 'https://www.scalesplus.com'
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)

urls = [
    ('https://www.scalesplus.com/cultivation-scales/?Brand=A_AMP_D__Weighing||Adam__Equipment||OHAUS||Rice__Lake__Weighing__Systems','cultivation_scales')
]

for url, category_name in urls:
    driver.get(url)

    # for _ in range(5):
    #     time.sleep(2)
    # bottom = driver.find_element(By.CSS_SELECTOR, 'body > footer > div:nth-child(2)')
    # ActionChains(driver).scroll_to_element(bottom).perform()
    # time.sleep(50)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    i = 0

    with open(f'scalesplus/product links/product links {category_name.capitalize()}.txt', 'w') as f:
        for tag in soup.select('.productGrid>.product'):
            f.write(base_url + tag.a.get('href') + '\n')
            i += 1
    print('Total number of product links', i)
    asyncio.run(main(category_name))

driver.quit()
