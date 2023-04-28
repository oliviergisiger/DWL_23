from peewee import Model, Proxy, DateField, IntegerField, FloatField, CharField
from sqlalchemy.types import DATETIME, INTEGER, FLOAT, VARCHAR
from sqlalchemy import MetaData, Column, Table


metadata_obj = MetaData()
WeatherDataTable = Table("weather_data", metadata_obj,
                           Column('local_date_time', DATETIME(), primary_key=True),
                           Column('TTT_C', FLOAT(), primary_key=False),
                           Column('TTT_C', FLOAT(), primary_key=False),
                           Column('TTT_C', FLOAT(), primary_key=False),
                           Column('TTL_C', FLOAT(), primary_key=False),
                           Column('TTH_C', FLOAT(), primary_key=False),
                           Column('TTTFEEL_C', FLOAT(), primary_key=False),
                           Column('DEWPOINT_C', FLOAT(), primary_key=False),
                           Column('PROBPCP_PERCENT', FLOAT(), primary_key=False),
                           Column('RRR_MM', FLOAT(), primary_key=False),
                           Column('RELHUM_PERCENT', FLOAT(), primary_key=False),
                           Column('FF_KMH', FLOAT(), primary_key=False),
                           Column('FX_KMH', FLOAT(), primary_key=False),
                           Column('DD_DEG', FLOAT(), primary_key=False),
                           Column('SUN_MIN', FLOAT(), primary_key=False),
                           Column('FRESHSNOW_CM', FLOAT(), primary_key=False),
                           Column('PRESSURE_HPA', FLOAT(), primary_key=False),
                           Column('SYMBOL24_CODE', FLOAT(), primary_key=False),
                           Column('IRRADIANCE_WM2', FLOAT(), primary_key=False),
                           Column('geo', VARCHAR(), primary_key=False),
                           Column('SYMBOL_CODE', INTEGER(), primary_key=False),
                           Column('type', VARCHAR(), primary_key=False))









database_proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = database_proxy

class WeatherORM(BaseModel):
    local_date_time = DateField,
    TTT_C = FloatField,
    TTL_C = FloatField
    TTH_C = FloatField
    TTTFEEL_C = FloatField
    DEWPOINT_C = FloatField
    PROBPCP_PERCENT = FloatField
    RRR_MM = FloatField
    RELHUM_PERCENT = FloatField
    FF_KMH = FloatField
    FX_KMH = FloatField
    DD_DEG = FloatField
    SUN_MIN = FloatField
    IRRADIANCE_WM2 = FloatField
    FRESHSNOW_CM = FloatField
    PRESSURE_HPA = FloatField


SQL = """CREATE TABLE weather_data (
            local_date_time         date,
            TTT_C                   float8,
            TTL_C                   float8,
            TTH_C                   float8,
            TTTFEEL_C               float8,
            DEWPOINT_C              float8,
            PROBPCP_PERCENT         float8,
            RRR_MM                  float8,
            RELHUM_PERCENT          float8,
            FF_KMH                  float8,
            FX_KMH                  float8,
            DD_DEG                  float8,
            SUN_MIN                 float8,
            IRRADIANCE_WM2          float8,
            FRESHSNOW_CM            float8,
            PRESSURE_HPA            float8, 

        ); """