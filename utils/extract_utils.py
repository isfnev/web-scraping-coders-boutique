import pandas as pd
from typing import List
import requests
import io
from concurrent.futures import ThreadPoolExecutor 

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

def return_df_multiple_test(give_url, urls_path, json_file_path, discontinued_path, exception_path, failed_file_path)->None:
    urls = get_urls(urls_path)

    session = requests.Session()
    # give_urls(urls, 1, session)
    # For multiple runs with threadpoolexecutor
    with ThreadPoolExecutor(max_workers=40) as executor:
        executor.map(lambda url, j: give_url(url, j, session, json_file_path, discontinued_path, exception_path, failed_file_path), urls, range(1, len(urls)))

