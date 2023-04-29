from sqlalchemy.types import Integer, DateTime, Numeric, String

weather_data_table = {
    'local_date_time': DateTime,
    'TTT_C': Numeric,
    'TTL_C': Numeric,
    'TTH_C': Numeric,
    'TTTFEEL_C': Numeric,
    'DEWPOINT_C': Numeric,
    'PROBPCP_PERCENT': Numeric,
    'RRR_MM': Numeric,
    'RELHUM_PERCENT': Numeric,
    'FF_KMH': Numeric,
    'FX_KMH': Numeric,
    'DD_DEG': Numeric,
    'SUN_MIN': Numeric,
    'IRRADIANCE_WM2': Numeric,
    'FRESHSNOW_CM': Numeric,
    'PRESSURE_HPA': Numeric,
    'SYMBOL24_CODE': Integer,
    'IRRADIANCE_WM2': Numeric,
    'geo': String,
    'SYMBOL_CODE': Integer,
    'type': String,
    'ExecutionDate': DateTime
}
