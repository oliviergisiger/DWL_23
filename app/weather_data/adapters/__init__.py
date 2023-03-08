

SRG_METEO_API_CONFIGS = {
    'level': [['forecast'],['hour']],
    'index_column': 'local_date_time',
    'columns': [
        'local_date_time',
        'TTT_C',
        'TTL_C',
        'TTH_C',
        'TTTFEEL_C',
        'DEWPOINT_C',
        'PROBPCP_PERCENT',
        'RRR_MM',
        'RELHUM_PERCENT',
        'FF_KMH',
        'FX_KMH',
        'DD_DEG',
        'SUN_MIN',
        'IRRADIANCE_WM2',
        'FRESHSNOW_CM',
        'PRESSURE_HPA'
    ]
}