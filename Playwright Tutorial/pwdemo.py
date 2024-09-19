from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def get_dynamic_html():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_default_timeout(120000)
        page.goto('https://keyzarjewelry.com/collections/engagement-ring-settings', timeout=120000)
        page.click('#onetrust-accept-btn-handler')

        for _ in range(4):
            page.click('button:has-text("Load More")')

        # page.is_visible('#mainContent > div.mb-3.px-5.md\\:p-5.md\\:pb-10 > div')
        # page.wait_for_selector('#mainContent > div.mb-3.px-5.md\\:p-5.md\\:pb-10 > div')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        # html_content = page.inner_html('#mainContent > div.mb-3.px-5.md\\:p-5.md\\:pb-10 > div')
        html_content = page.content()
        print(html_content)

        # urls = []
        # base_url = 'https://keyzarjewelry.com/'
        # try:
        #     print(soup.find(class_='CustomGridContainer max-w-8xl mx-auto grid tangiblee-grid grid-cols-2 gap-4 md:gap-2.5 md:grid-cols-2 xl:gap-4 xl:grid-cols-4 items-start'))
        # except Exception as e:
        #     print("Exception :", e)
        # for a_tag in soup.find('div', class_='CustomGridContainer max-w-8xl mx-auto grid tangiblee-grid grid-cols-2 gap-4 md:gap-2.5 md:grid-cols-2 xl:gap-4 xl:grid-cols-4 items-start').find_all('a').get('href'):
        #     urls.append(base_url+a_tag)
        # for idx, i in enumerate(urls, 1):
        #     print(idx, i)
        # browser.close()
        return html_content

def store_html_content(html_content):
    with open('Playwright Tutorial/textfiles/dynamic_content.html','w', encoding='utf-8') as f:
        f.write(html_content)

def read_dynamic_content():
    with open('Playwright Tutorial/textfiles/dynamic_content.html','r', encoding='utf-8') as f:
        return f.read()

if __name__=='__main__':
    # html_content = get_dynamic_html()
    # store_html_content(html_content)
    html_content = read_dynamic_content()
    soup = BeautifulSoup(html_content, 'lxml')

    print(len(soup.find_all(class_='SettingProductCard relative group')))