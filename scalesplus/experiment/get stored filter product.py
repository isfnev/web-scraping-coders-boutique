import json

with open('scalesplus/textfiles/filter product.txt') as f:
    dict = json.loads(f.read())

for key in dict:
    print(key)