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
            # Narrow down navigation section to get category
            navigation = soup.find('ol', class_='sc-4cfuhz-2 ipoVcw')
            navigation_parts = navigation.find_all('li', class_='sc-4cfuhz-3 iIgemP')
            category = [subcategory.text for subcategory in navigation_parts][-2]

            time.sleep(random.randint(2, 4))
            # Use Playwright to scrape emission information
            try:
                with sync_playwright() as pw:
                    agent = 'userMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                            'Chrome/83.0.4103.116 Safari/537.36'
                    browser = pw.chromium.launch(headless=True)
                    context = browser.new_context(user_agent=agent)
                    page = context.new_page()
                    page.goto(url)

                    # Find sustainability section and open it
                    page.locator("[data-test=\"sustainability\"]").click()
                    compensation_price = page.get_by_role("row", name="Compensation amount").text_content()
                    compensation_price = compensation_price.split("CHF ")[1].replace("’", "")
                    compensation_price = float(compensation_price)
                    emission = page.get_by_role("row", name="CO₂-Emission").text_content()
                    emission = emission.split("Emission")[1].split("kg")[0].replace("’", "")
                    emission = float(emission)

                    context.close()
                    browser.close()

            except PlaywrightTimeoutError:
                print(f"{url} has no sustainability section")
                continue

            product = ProductItem(name=name,
                                  price=price,
                                  category=category,
                                  emission=emission,
                                  compensation_price=compensation_price)
            products.append(asdict(product))

            print(asdict(product))

        products_df = pd.DataFrame(products)
        print(products_df)

        return products_df



if __name__ == '__main__':

    url = 'https://www.digitec.ch/en/daily-deal'
    day_deals = DayDealScraper(url)
    day_deals._get_product_info()
