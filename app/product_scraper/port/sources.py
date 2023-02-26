from abc import ABC, abstractmethod


class Scraper(ABC):

    @abstractmethod
    def _get_product_links(self, url):
        pass