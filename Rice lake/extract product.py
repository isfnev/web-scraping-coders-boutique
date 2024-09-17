import requests
from bs4 import BeautifulSoup

def give_url(url):
    r = requests.get(url)

    try:
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')

            base_url = 'https://www.ricelake.com'
            first_container = soup.find(class_='col-xs-12 col-sm-6 col-md-5 page-content-section')
            list_title = []
            list_title.append(first_container.find('h1').text)
            list_content = []
            for li in first_container.find_all('li'):
                list_content.append(li.text)
            
            list_images = []
            for button in soup.find(id='product-thumbnails').find_all('button'):
                list_images.append(base_url+button.get('data-src'))

            print(list_title)
            print(list_content)
            print(len(list_content))
            print(list_images)
        else:
            print("Failed to get the url :", url)
    except Exception as e:
        print(e,':',url)

def get_urls():
    with open('Rice lake/textfiles/extract agri link.txt') as f:
        data = [line.strip() for line in f]
    return data

def main():
    urls = get_urls()
    give_url(urls[0])

if __name__=='__main__':
    main()