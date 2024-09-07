import requests
from bs4 import BeautifulSoup

def get_visible_text_from_url(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        h1_tag = soup.find('h1')

        for span in h1_tag.find_all('span'):
            span.unwrap()
        h1_content = h1_tag.get_text(separator=' ', strip=True)
        h1_tag.string = h1_content

        for script in soup(['script', 'style', 'meta', 'noscript', 'iframe']):
            script.decompose()
        
        visible_text = soup.get_text(separator='\n', strip=True)
        return visible_text
    else:
        return f"Failed to retrieve content. Status code: {response.status_code}"

url = 'https://keyzarjewelry.com/products/the-lisa-setting-round-14k-white-gold-2-carat-lab-diamond'
visible_text = get_visible_text_from_url(url)

with open('textfiles/keyzar_all_text.txt','w') as file:
    file.write(visible_text)
