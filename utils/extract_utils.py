import pandas as pd
from typing import List
from playwright.async_api import async_playwright
import asyncio
import json
import aiofiles

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

async def get_urls_async(give_url, urls_path, browser, json_file_path, discontinued_path, exception_path, failed_file_path, categories_checker)->List:
    print("start getting urls")
    tasks:List = []
    async with aiofiles.open(urls_path) as f:
        j = 1
        async for url in f:
            tasks.append(asyncio.create_task(give_url(url.strip(), j, browser, json_file_path, discontinued_path, exception_path, failed_file_path, categories_checker)))
            j += 1
    print("return urls")
    return tasks

async def return_df_multiple_test(give_url, urls_path, json_file_path, discontinued_path, exception_path, failed_file_path)->None:
    async with aiofiles.open('scalesplus/json/puting_scales.json') as f:
        categories_checker = json.loads(await f.read())
    async with async_playwright() as ap:
        browser = await ap.chromium.launch(headless=False)
        tasks = await get_urls_async(give_url, urls_path, browser, json_file_path, discontinued_path, exception_path, failed_file_path, categories_checker)

        await asyncio.gather(*tasks)
        await browser.close()
