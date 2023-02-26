# CO_2 Emissions by Purchasing Electronic Consumer Goods
## Converted to Energysources...

Project Repository for Data Lakes and Datawarehouse Systems. The application should sync files from different 
datasources, namely: 
- digitec.ch
- weather.xy (dummy ds)

And convert actual weather information into information about energy production and compare this to scraped products. 




## Structure

The is tried to be written in a hexagonal architectural pattern (ports - adapters). The repo structure is therefore (UPDATE) 

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






## Development information
Python Verison used: 3.10
Docker is used for deployment
pipenv is used for packaging. (https://pipenv.pypa.io/en/latest/)