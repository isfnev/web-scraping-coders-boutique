import pandas as pd
from typing import List
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def single_test(session, func, df_store_path, urls_path, link_index = 0)->None:
    urls = get_urls(urls_path)
    dict = func(session, urls[link_index])
    print(urls[link_index])
    # if df != None:
    # if not df.empty:
    if dict:
        df = pd.DataFrame([dict])
        df.to_csv(df_store_path, index=False)

def get_urls(give_urls, urls_path)->List:
    print("start getting urls")
    with open(urls_path) as f:
        urls:List = [url.strip() for url in f]
    packed_urls = [(give_urls, urls[i:i+89]) for i in range(0, len(urls), 89)]
    print("return urls")
    return packed_urls

def process_task(give_urls, urls):
    list = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(give_urls, urls, range(1, len(urls)+1))
        for dt in results:
            if dt:
                list.append(dt)
    return list

def return_df_multiple_test(give_urls, df_store_path, urls_path)->None:

    packed_urls = get_urls(give_urls, urls_path)
    list = []
    # list.append(give_urls(urls, 1))
    with ProcessPoolExecutor(max_workers=8) as executor:
        results = executor.map(process_task, packed_urls)
        for dt in results:
            list.extend(dt)

    df:pd.DataFrame = pd.DataFrame(list)
    df.to_csv(df_store_path, index=False)
