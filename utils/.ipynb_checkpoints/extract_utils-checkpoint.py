import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def single_test(func, df_store_path, urls_path, link_index = 0):
    urls = get_urls(urls_path)
    df = func(urls[link_index])
    # if df != None:
    if not df.empty:
        df.to_csv(df_store_path, index=False)

def get_urls(urls_path):
    with open(urls_path) as f:
        data = [line.strip() for line in f]
    return data

def return_df_multiple_test(func, df_store_path, urls_path):
    urls = get_urls(urls_path)
    list = []
    with ThreadPoolExecutor(max_workers = 8) as executor:
        result = executor.map(func, urls)
        for dict in result:
            list.append(dict)
            # print('list : ', list)
            # print('\n\n')
    print(list)
    df = pd.DataFrame(list)
    df = df.fillna('')
    df.to_csv(df_store_path, index=False)