import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def single_test(func, df_store_path, urls_path):
    urls = get_urls(urls_path)
    df = func(urls[1])
    # if df != None:
    if not df.empty:
        df.to_csv(df_store_path, index=False)

def get_urls(urls_path):
    with open(urls_path) as f:
        data = [line.strip() for line in f]
    return data

def return_df_multiple_test(func, df_store_path, urls_path):
    urls = get_urls(urls_path)
    df = pd.DataFrame()
    with ThreadPoolExecutor(max_workers = 8) as executor:
        result = executor.map(func, urls)
        for new_df in result:
            df = pd.concat([df, new_df])
    df.to_csv(df_store_path, index=False)
print(__name__)