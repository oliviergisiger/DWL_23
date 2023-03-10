from weather_data.adapters.weather_data_source import WeatherDataSource
from weather_data.adapters.weather_data_sink import WeatherDataSink


class SyncWeatherData:

    def __init__(self, source: WeatherDataSource, sink: WeatherDataSink):
        self.source = source
        self.sink = sink

    def invoke_workflow(self, execution_date):
        data = self.source._get_dummy_json() #change to get_weather_data
        self.sink.write_to_s3(data, execution_date)


if __name__ == '__main__':
    pass