import requests
import json

headers = {
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

data = 'old_filter=\
&filter%5BPrice%5D%5Bmin%5D=0\
&filter%5BPrice%5D%5Bmax%5D=9985\
&filter%5BBrand%5D%5B%5D=44\
&filter%5BBrand%5D%5B%5D=40\
&filter%5BBrand%5D%5B%5D=38\
&filter%5BBrand%5D%5B%5D=41\
&filter%5BCapacity_BO_g_BC__CF%5D%5Bname%5D=Capacity+(g)\
&filter%5BCapacity_BO_g_BC__CF%5D%5Bdbname%5D=Capacity+(g)\
&filter%5BCapacity_BO_g_BC__CF%5D%5Bmin%5D=52\
&filter%5BCapacity_BO_g_BC__CF%5D%5Bmax%5D=35000\
&filter%5BCapacity_BO_lb_BC__CF%5D%5Bname%5D=Capacity+(lb)\
&filter%5BCapacity_BO_lb_BC__CF%5D%5Bdbname%5D=Capacity+(lb)\
&filter%5BCapacity_BO_lb_BC__CF%5D%5Bmin%5D=5\
&filter%5BCapacity_BO_lb_BC__CF%5D%5Bmax%5D=1200\
&filter%5BCapacity_BO_kg_BC__CF%5D%5Bname%5D=Capacity+(kg)\
&filter%5BCapacity_BO_kg_BC__CF%5D%5Bdbname%5D=Capacity+(kg)\
&filter%5BCapacity_BO_kg_BC__CF%5D%5Bmin%5D=8\
&filter%5BCapacity_BO_kg_BC__CF%5D%5Bmax%5D=100\
&id=594\
&site=errhy7umuu\
&currency=\
&customer_group=\
&filter_type=category\
&searchQuery=undefined\
&bulkQty=undefined\
&sort_order=priceasc\
&searched_text=\
&channel_id=2\
&staff_cookie='

response = requests.post('https://filter.freshclick.co.uk/Category_filter/filter_product', headers=headers, data=data)

file_path = 'scalesplus/textfiles/filter product1.json'

with open(file_path,'w') as f:
    f.write(json.dumps(response.json(), indent=4))
