from abc import ABC, abstractmethod


class ScraperDataSource(ABC):

    @abstractmethod
    def read_source(self, execution_date):
        pass


class ScraperDataSink(ABC):

    @abstractmethod
    def export(self, data):
        pass
