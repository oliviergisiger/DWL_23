from weather_data.adapters.weather_data_source import WeatherDataSource
from weather_data.adapters.weather_data_sink import WeatherDataSink


class SyncWeatherData:

    def __init__(self, source: WeatherDataSource, sink: WeatherDataSink):
        self.source = source
        self.sink = sink

    def invoke_workflow(self):
        df = self.source.get_weather_df()
        self.sink.write_to_file(df)


if __name__ == '__main__':
    pass