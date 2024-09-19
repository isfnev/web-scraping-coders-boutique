from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os

with sync_playwright() as p:
    browser = p.chromium.launch(timeout=0, headless=False)
    page = browser.new_page()
    base_url = 'https://www.ricelake.com'
    page.goto('https://www.ricelake.com/product-landing-pages/floor-scales/', timeout=0)

    soup = BeautifulSoup(page.inner_html(selector='html', timeout=0), 'html.parser')

    if not os.path.exists('Rice lake/cannabis/textfiles'):
        os.mkdir('Rice lake/cannabis/textfiles')

    with open('Rice lake/cannabis/textfiles/extracted links.txt','a') as f:
        for div in soup.find_all('div', class_='shadow-container'):
            for a in div.find_all('a'):
                f.write(base_url+a.get('href')+'\n')

    for _ in range(3):
        page.click('#next-page', timeout=0)
        page.wait_for_timeout(10000)
        soup = BeautifulSoup(page.inner_html(selector='html', timeout=0), 'lxml')

        with open('Rice lake/cannabis/textfiles/extracted links.txt','a') as f:
            for div in soup.find_all('div', class_='shadow-container'):
                for a in div.find_all('a'):
                    f.write(base_url+a.get('href')+'\n')

    browser.close()