# CO_2 Emissions by Purchasing Electronic Consumer Goods
## Converted to Energysources...

Project Repository for Data Lakes and Datawarehouse Systems. The application should sync files from different 
datasources, namely: 
- digitec.ch
- weather.xy (dummy ds)

And convert actual weather information into information about energy production and compare this to scraped products. 


## Minio Local Dev Setup

- Create Object in minio (buckets > create new bucket with name `s3-raw-data-dwl23`)
- Create minio access Key (save credentials locally to have them ready for later)
- In Airflow:
  - Variables (new variable): 
    - Key=`ENVIRONMENT`
    - Value=`LOCAL_DEV`
  - Conections (new connection): 
    - Connection Id: `S3_DEVELOPMENT`
    - Connection Type: `Amazon Web Services`
    - AWS Access Key ID: empty field (delete airflow out of it)
    - AWS Secret Access Key: empty field (delete airflow out of it)
    - Extra: dict("aws_access_key_id": minio access key , "aws_secret_access_key": minio secret key, "endpoint_url": "http://minio:9000")
  - In DAG
  ```
    from airflow.models import Variable
  
    # dynamic environment settings
    ENVIRONMENT_VAR = "ENVIRONMENT"
    ENVIRONMENT = Variable.get(ENVIRONMENT_VAR, default_var='LOCAL_DEV')
    
    # runtime configs
    RUNTIME_CONFIG_VAR = "scrape_digitec_data_runtime_config"
    RUNTIME_CONFIG = Variable.get(RUNTIME_CONFIG_VAR,
                                  deserialize_json=True,
                                  default_var={})
    
    S3_CONNECTION = 'S3_DEVELOPMENT' if ENVIRONMENT == 'LOCAL_DEV' else 'S3_PRODUCTION'
  ```


## Structure

The is tried to be written in a hexagonal architectural pattern (ports - adapters). The repo structure is therefore (UPDATE) 
```
DWL_23
├── app
│   ├── scrape_products
│   │   ├── adapters
│   │   │   ├── sources
│   │   │   │   ├── scrape_digitec.py
│   │   │   ├── sinks
│   │   ├── ports
│   │   │   ├── sources.py
│   │   │   ├── sinks.py
│   │   ├── capabilities
│   │   ├── configuration
│   │   ├── usecases
│   │   ├── domain.py
│   │   ├── __init__.py
├── dags
│   ├── dag_sync_api.py
│   ├── dag_sync_digitec.py
├── docker-compose.yaml
├── Pipfile
├── Pipfile.lock
├── .env
└── .gitignore
```






## Development information
Python Verison used: 3.10
Docker is used for deployment
pipenv is used for packaging. (https://pipenv.pypa.io/en/latest/)