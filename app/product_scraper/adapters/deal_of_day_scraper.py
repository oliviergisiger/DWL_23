import requests
from typing import List
from bs4 import BeautifulSoup
from product_scraper.port.sources import Scraper
from product_scraper.domain import ProductItem


class DayDealScraper(Scraper):

    def __init__(self, url):
        self.url = url
        self.urls = self._get_product_links(self.url)


    def get_product_info(self):
        """
        Return pd.DataFrame with product information from deals of the day.
        """
        pass


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

        for url in urls:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'lxml')

            name = soup.find('h1', class_='sc-12r9jwk-0 hcjJEJ').text
            price = soup.find('div', class_='sc-18ppxou-1 gwNBaL').text.split('.')[0]

            # scrape emission. narrow down to sustainability section first
            sustainability_section = soup.find('h3', {'id': 'sustainability'})
            print(sustainability_section)
            break





if __name__ == '__main__':

    url = 'https://www.digitec.ch/en/daily-deal'
    day_deals = DayDealScraper(url)
    day_deals._get_product_info()
