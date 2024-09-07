from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scrap_keyzar():
    options = webdriver.EdgeOptions()
    options.headless = False
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

    url = 'https://keyzarjewelry.com/collections/preset-lab-diamond-engagement-rings?center_stone_shape=Round'
    driver.get(url)

    # try:
    #     load_more_button = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Load More')]"))
    #     )

    #     load_more_button.click()

    #     # while True:
    #     #     try:
    #     #         load_more_button = WebDriverWait(driver, 10).until(
    #     #             EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Load More')]"))
    #     #         )
    #     #         load_more_button.click()
    #     #     except:
    #     #         break

    # except Exception as e:
    #     print("Error:", e)
    time.sleep(60)

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    tags = soup.find_all('a', class_=['absolute', 'inset-0', 'z-10'])

    s = set()
    for tag in tags:
        s.add(tag.get('href'))

    s.remove('/')
    driver.quit()
    return list(s)

if __name__=='__main__':
    file = scrap_keyzar()
    print(len(file))
    print(type(file))

    with open('textfiles/scraping_keyzar.txt','w') as f:
        for i in file:
            f.write('https://keyzarjewelry.com'+i+'\n')