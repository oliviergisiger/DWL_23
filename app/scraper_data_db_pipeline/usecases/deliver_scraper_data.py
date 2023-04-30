from scraper_data_db_pipeline.adapters.scraper_data_db_source import ScraperDataSourceAdapter
from scraper_data_db_pipeline.adapters.scraper_data_db_sink import ScraperDataSinkAdapter


class DeliverScraperData:
    """
    Builds usecase wrapper for scraper data delivery.
    """
    def __init__(self, source: ScraperDataSourceAdapter, sink: ScraperDataSinkAdapter):
        self._source = source
        self._sink = sink

    def execute_usecase(self, execution_date):
        data = self._source.read_source()
        self._sink.export(data, execution_date)


if __name__ == '__main__':
    pass
