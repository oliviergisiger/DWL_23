from weather_data.adapters.weather_data_source import WeatherDataSource
from weather_data.adapters.weather_data_sink import WeatherDataSink


class DeliverWeatherData:
    """
    should build a usecas wrapper for weather data delivery.
    should inherit from abstract class "usecase", which is to be defined.
    """

    def __init__(self, source: WeatherDataSource, sink: WeatherDataSink):
        self._source = source
        self._sink = sink

    def execute_usecase(self, execution_date):
        data = self._source.read_source(execution_date)
        self._sink.export(data, execution_date)


if __name__ == '__main__':
    pass
