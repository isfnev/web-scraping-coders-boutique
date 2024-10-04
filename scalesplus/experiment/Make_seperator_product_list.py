import os
import json
dir = os.getcwd()+'/scalesplus/json/'

order_set = {}
for i in os.listdir(dir):
    if i.endswith('cultivation_scales.json'):
        continue
    elif i.startswith('Data'):
        with open(dir+i) as f:
            for l in json.loads(f.read()).values():
                for v in l:
                    if i[21:-5] in order_set:
                        order_set[i[21:-5]].append(v)
                    else:
                        order_set[i[21:-5]] = [v]

for key in order_set:
    print(key)
print(i)
print(i[21:])

with open(dir+i[21:],'w') as f:
    json.dump(order_set, f)
