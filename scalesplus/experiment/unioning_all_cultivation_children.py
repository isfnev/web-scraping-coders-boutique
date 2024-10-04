import os
import json
dir = os.getcwd()+'/scalesplus/json/'

s = set()

for i in os.listdir(dir):
    if i.startswith('Data') and i != 'Data_for_cultivation_scales.json':
        print(i)
        with open(dir+i) as f:
            temp = json.loads(f.read())
        for v in temp.values():
            for i in v:
                s.add(i)
order_set = set()
with open(dir+'Data_for_cultivation_scales.json') as f:
    for w in json.loads(f.read()).values():
        for v in w:
            order_set.add(v)
print('A :', len(order_set))
# for i in s:
#     print(i)
print('B :', len(s))
print('A-B :', len(order_set.difference(s)))
print('B-A :', len(s.difference(order_set)))
print(len(order_set))
print(len(s))
