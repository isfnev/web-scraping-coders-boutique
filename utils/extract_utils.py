import pandas as pd
from typing import List, Dict
from playwright.sync_api import sync_playwright
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

def get_urls(urls_path)->List:
    print("start getting urls")
    with open(urls_path) as f:
        urls:List = [url.strip() for url in f]
    print("return urls")
    return urls

def return_df_multiple_test(give_urls, df_store_path, urls_path)->None:

    urls = get_urls(urls_path)
    list = []
    # list.append(give_urls(urls, 1))
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(give_urls, urls, range(1, len(urls)+1))
        for dt in results:
            if dt:
                list.append(dt)

    df:pd.DataFrame = pd.DataFrame(list)
    df.to_csv(df_store_path, index=False)
