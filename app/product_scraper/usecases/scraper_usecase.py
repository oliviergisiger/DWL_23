from product_scraper.port.sources import ScraperSource
from product_scraper.port.sources import ScraperSink


class ScrapeProducts:

    def __init__(self, source: ScraperSource, sink: ScraperSink):
        self._source = source
        self._sink = sink

    def execute_usecase(self, execution_date):
        data = self._source.get_product_info_df()
        self._sink.write_to_s3(data=data, execution_date=execution_date)
