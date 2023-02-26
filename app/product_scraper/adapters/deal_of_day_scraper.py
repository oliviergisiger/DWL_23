import requests
import pandas as pd
from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
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
            href = article.find('a', class_='sc-qlvix8-0 dgECEw')['href']
            urls.append(f"https://www.digitec.ch{href}")

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
            price = soup.find('div', class_='sc-18ppxou-1 gwNBaL').text.split('.')[0]

            # scrape emission. use selenium to expand section
            firefox_options = Options()
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
            firefox_options.add_argument(('user-agent={0}').format(user_agent))
            firefox_options.add_argument("--headless")

            driver = webdriver.Firefox(options=firefox_options)
            driver.get(url)

            try:
                button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="sustainability"]/button')))
                button.click()

                section = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        '#pageContent > div > div.sc-c3y39x-0.bAaSKU > section:nth-child(3) > div.sc-l19rvt-2.gpTNdM.sc-1wsbwny-0.EvAlG.fade-enter-done')))
                sustainability_soup = BeautifulSoup(section.get_attribute('innerHTML'), 'lxml')
                driver.close()

                emission = sustainability_soup.find('td', class_='sc-12uqqiy-4 hLZuEg').nextSibling.text

            # Catch exception if sustainability section does not exist
            except TimeoutException as ex:
                print(f"Exception raised: {ex}")
                driver.close()
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
