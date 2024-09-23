from bs4 import BeautifulSoup

with open('index.html') as f:
    soup = BeautifulSoup(f.read(), 'lxml')

print(soup.find(style'font-size')))