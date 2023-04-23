import sqlalchemy
from peewee import Model, Proxy, DateField, IntegerField, FloatField, CharField


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
