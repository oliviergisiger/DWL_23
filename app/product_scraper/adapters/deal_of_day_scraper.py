import requests
import time
import random
import pandas as pd
from typing import List
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright, TimeoutError as PlaywrightTimeoutError
from product_scraper.port.sources import Scraper
from product_scraper.domain import ProductItem
from dataclasses import asdict


class DayDealScraper(Scraper):

    def __init__(self, url):
        self.url = url
        self.urls = self._get_product_links(self.url)


    def get_product_info_df(self):
        """
        Return pd.DataFrame with product information from deals of the day.
        """
        return self._get_product_info()


    def _get_product_links(self, url: str) -> List[str]:
        """
        Get href of products on url-page
        """
        urls = []

        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')

        articles = soup.find_all('article')

        for article in articles:

            try:
                href = article.find('a', class_='sc-qlvix8-0 dgECEw')['href']
                urls.append(f"https://www.digitec.ch{href}")
            except TypeError:
                continue

        return urls


    def _get_product_info(self):
        """
        Scrape product info of every subpage
        """
        urls = self._get_product_links(self.url)

        products = []
        for url in urls:
            print(url)

            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'lxml')

            name = soup.find('h1', class_='sc-12r9jwk-0 hcjJEJ').text
            price = float(soup.find('div', class_='sc-18ppxou-1 gwNBaL').text.split('.')[0])

            # Use Playwright to scrape emission information
            try:
                with sync_playwright() as pw:
                    browser = pw.chromium.launch(headless=False)
                    context = browser.new_context()
                    page = context.new_page()
                    page.goto(url)

                    # Find sustainability section and open it
                    page.locator("[data-test=\"sustainability\"]").click()
                    emission = page.get_by_role("row", name="CO₂-Emission").text_content()
                    emission = float(emission.split("Emission")[1].split("kg")[0])

                    context.close()
                    browser.close()
                    time.sleep(random.randint(3, 8))

            except PlaywrightTimeoutError:
                print(f"{url} has no sustainability section")
                continue

            product = ProductItem(name=name, price=price, emission=emission)
            products.append(asdict(product))

            print(asdict(product))

        products_df = pd.DataFrame(products)
        print(products_df)

        return products_df



if __name__ == '__main__':

    url = 'https://www.digitec.ch/en/daily-deal'
    day_deals = DayDealScraper(url)
    day_deals._get_product_info()
