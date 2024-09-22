import json

def store_url_from_json(file, path):
    with open(path) as f:
        data = json.loads(f.read())

    base_url = 'https://www.scalesplus.com'

    with open(file, 'a') as f:
        for i in data['product']:
            f.write(base_url+i['custom_url']+'\n')

def main():
    paths = [
        'scalesplus/textfiles/filter product.json',
        'scalesplus/textfiles/setfilterproduct1.json',
        'scalesplus/textfiles/setfilterproduct2.json',
        'scalesplus/textfiles/setfilterproduct3.json',
    ]

    file = 'scalesplus/textfiles/111 links.txt'
    for path in paths:
        store_url_from_json(file, path)

if __name__=='__main__':
    main()