from abc import ABC, abstractmethod
from datetime import date


class ScraperSource(ABC):

    @abstractmethod
    def _get_product_links(self, url):
        pass


class ScraperSink(ABC):
    @abstractmethod
    def write_to_s3(self, execution_date: date):
        pass
