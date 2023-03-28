import requests
import time
import random
import logging
import pandas as pd
from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium_stealth import stealth
from product_scraper.port.sources import Scraper
from product_scraper.domain import ProductItem
from dataclasses import asdict


class GalaxusDayDealScraper(Scraper):

    def __init__(self, url):
        self.url = url
        self.urls = self._get_product_links(self.url)

    def get_product_info_df(self):
        """
        Return pd.DataFrame with product information from deals of the day.
        """
        product_info_df = self._get_product_info()
        print(product_info_df)
        return product_info_df

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
                href = article.find('a', class_='sc-qlvix8-0 kLVcrw')['href']
                urls.append(f"https://www.galaxus.ch{href}")
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
            navigation_parts = navigation.find_all('li', class_='sc-4cfuhz-3 ftxNPU')
            category = [subcategory.text for subcategory in navigation_parts][-2]
            print(category)

            # Use Selenium to scrape emission information
            options = ChromeOptions()
            # Adding argument to disable the AutomationControlled flag
            options.add_argument("--disable-blink-features=AutomationControlled")
            # Exclude the collection of enable-automation switches
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            # Turn-off userAutomationExtension
            options.add_experimental_option("useAutomationExtension", False)
            options.add_argument("--window-size=640,1280")
            options.add_argument("--headless")
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--disable-extensions")
            options.add_argument('--no-sandbox')

            # Set user agent
            user_agent_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36']
            user_agent = random.choice(user_agent_list)
            options.add_argument(f'user-agent={user_agent}')

            # Launch the browser
            #driver = webdriver.Chrome('chromedriver', options=options)
            # Docker driver
            with webdriver.Remote("http://172.19.0.4:4444/wd/hub", options=options) as driver:

                # Changing the property of the navigator value for webdriver to undefined
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

                # Stealth selenium
                # stealth(driver,
                #         languages=["en-US", "en"],
                #         vendor="Google Inc.",
                #         platform="Win32",
                #         webgl_vendor="Intel Inc.",
                #         renderer="Intel Iris OpenGL Engine",
                #         fix_hairline=True,
                #         )

                # Navigate to the URL
                driver.get(url)
                time.sleep(random.randint(4, 6))

                try:
                    # Find weight under product Specifications > Show more
                    show_more_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="showMoreButton-specifications"]')))
                    show_more_button.click()
                    time.sleep(random.randint(1, 3))
                    weight = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, '//td[text()="Weight"]/following-sibling::td'))).text.strip()

                except TimeoutException:
                    print(f"{url} has no weight section")
                    continue

                try:
                    driver.refresh()
                    time.sleep(random.randint(1, 3))
                    print("Refreshed driver")
                    # Find sustainability section and open it
                    sustainability_section = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="sustainability"]')))
                    sustainability_section.click()

                    compensation_price = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, '//td[contains(text(), "Compensation amount")]/following-sibling::td'))).text.strip()
                    compensation_price = compensation_price.split("CHF ")[1].replace("’", "")
                    compensation_price = float(compensation_price)

                    emission = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//td[contains(text(), "CO₂-Emission")]/following-sibling::td'))).text.strip()
                    emission = emission.split("kg")[0].replace("’", "")
                    emission = float(emission)

                except TimeoutException:
                    print(f"{url} has no sustainability section")
                    continue

                finally:
                    driver.close()

                product = ProductItem(name=name,
                                      price=price,
                                      category=category,
                                      weight=weight,
                                      emission=emission,
                                      compensation_price=compensation_price)
                products.append(asdict(product))

                print(asdict(product))

        products_df = pd.DataFrame(products)

        return products_df


if __name__ == '__main__':
    url = 'https://www.galaxus.ch/en/daily-deal'
    day_deals = GalaxusDayDealScraper(url)
    day_deals.get_product_info_df()