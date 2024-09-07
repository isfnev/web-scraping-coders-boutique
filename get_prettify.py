from bs4 import BeautifulSoup
import requests

with open('textfiles/scraping_keyzar.txt') as file:
    url = file.readline().strip()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:        
    soup = BeautifulSoup(response.content, 'html.parser')            
   
    with open('keyzar_prettify.txt','w',encoding='utf-8') as file:
        file.write(soup.prettify())

else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")
