from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import time

edge_options = Options()
edge_options.binary_location = "/usr/bin/microsoft-edge-stable"

base_url = 'https://www.scalesplus.com'

driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)
url = 'https://www.scalesplus.com/cultivation-scales/?Brand=A_AMP_D__Weighing||Adam__Equipment||OHAUS||Rice__Lake__Weighing__Systems'

driver.get(url)

for _ in range(5):
    time.sleep(2)
    bottom = driver.find_element(By.CSS_SELECTOR, 'body > footer > div:nth-child(2)')
    ActionChains(driver).scroll_to_element(bottom).perform()

soup = BeautifulSoup(driver.page_source, 'lxml')
with open('scalesplus/textfiles/product links.txt', 'w') as f:
    for tag in soup.select('.productGrid>.product'):
        f.write(base_url + tag.a.get('href') + '\n')

driver.quit()
