from sqlalchemy.types import DateTime, Numeric

hydro_data_table = {
    'local_date_time': DateTime,
    'aare_temp': Numeric,
    'aare_flow': Numeric
}
