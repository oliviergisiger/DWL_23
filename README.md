# Contextualizing CO2 emissions to strengthen compensation transparency and to derive appropriate actions

This project represents the main repository for the semester project of the moduel *Data Warehouse and Data Lake* at the Lucerne University of Applied Sciences and Arts (HSLU). It represents an ETL process that extracts product emissions by scraping and weather information by API calls and stores it in a data lake. This The data is then loaded into a data warehouse. The orchestration of the pipelines is done with Airflow. This repository builds the data engineering part to reach the goal of creating a platform that helps users to translate the emissions caused by a specific product by providing them with transparent, actionable compensation methods that show for how much, with what and how long it would take to compensate the emission. 

## Project structure

``````
.
|-- app
|   |-- api_sync
|   |   |-- __init__.py
|   |   |-- adapters
|   |   |   |-- __init__.py
|   |   |   |-- sync_api_sink.py
|   |   |   `-- sync_api_source.py
|   |   |-- ports
|   |   |   |-- __init__.py
|   |   |   `-- sync_api.py
|   |   `-- usecases
|   |       |-- __init__.py
|   |       `-- sync_api_usecase.py
|   |-- base
|   |   `-- configurations
|   |       `-- db_config.py
|   |-- configurations
|   |   `-- configs.py
|   |-- hydro_data
|   |   |-- adapters
|   |   |   |-- __init__.py
|   |   |   |-- hydro_data_sink.py
|   |   |   `-- hydro_data_source.py
|   |   |-- capabilities
|   |   |   |-- __init__.py
|   |   |   `-- database_orm.py
|   |   |-- configurations
|   |   |   `-- configs.py
|   |   |-- ports
|   |   |   |-- __init__.py
|   |   |   `-- hydro_data.py
|   |   `-- usecases
|   |       |-- __init__.py
|   |       `-- deliver_hydro_data.py
|   |-- product_scraper
|   |   |-- adapters
|   |   |   |-- digitec_deal_of_day_scraper_selenium.py
|   |   |   |-- galaxus_deal_of_day_scraper_selenium.py
|   |   |   `-- scraper_data_sink.py
|   |   |-- chromedriver
|   |   |-- domain.py
|   |   |-- port
|   |   |   `-- sources.py
|   |   `-- usecases
|   |       `-- scraper_usecase.py
|   |-- scraper_data_db_pipeline
|   |   |-- adapters
|   |   |   |-- scraper_data_db_sink.py
|   |   |   `-- scraper_data_db_source.py
|   |   |-- capabilities
|   |   |-- configurations
|   |   |-- ports
|   |   |   `-- sources.py
|   |   `-- usecases
|   |       `-- deliver_scraper_data.py
|   `-- weather_data
|       |-- adapters
|       |   |-- __init__.py
|       |   |-- weather_data_sink.py
|       |   `-- weather_data_source.py
|       |-- capabilities
|       |   |-- __init__.py
|       |   `-- database_orm.py
|       |-- configurations
|       |   `-- configs.py
|       |-- ports
|       |   |-- __init__.py
|       |   `-- weather_data.py
|       `-- usecases
|           |-- __init__.py
|           `-- deliver_weather_data.py
|-- dags
|   |-- dag_deliver_hydro_data.py
|   |-- dag_deliver_scraper_data.py
|   |-- dag_deliver_weather_data.py
|   |-- dag_digitec_scraper.py
|   |-- dag_galaxus_scraper.py
|   |-- dag_sync_hydro_data.py
|   |-- dag_sync_weather_data.py
|   `-- dag_utils.py
|-- BYPASS_SESSION_LIMIT.md
|-- README.md
|-- Pipfile
|-- Pipfile.lock
|-- Dockerfile
`-- docker-compose.yaml
``````

## Installation

The following section describes the local installation of the project. This setup can then be used for further development or debugging.

1. **Clone the project repository to your local machine:**

```
git clone https://YOURGITHUBUSERNAME@github.com/oliviergisiger/DWL_23.git
pw: GITHUBTOKEN
cd DWL_23
```

* You will be asked for a password which is your personal access token. To generate your personal access token, do the following: From your GitHub account, go to **Settings** → **Developer Settings** → **Personal Access Token** → **Generate New Token** (Give your password) → **Fillup the form** → click **Generate token** → **Copy the generated Token**, it will be something like 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. (:exclamation:save your token as you won't be able to access it anymore after generation)

2. **Install/Run Docker:**

   1. If you do not have docker installed yet, Install Docker on your machine by following the instructions for [Mac](https://docs.docker.com/docker-for-mac/install/) or [Windows](https://docs.docker.com/docker-for-windows/install/). 

   2. Check that Docker deamon (Docker Desktop) is running

   3. Build the Docker image for the `DWL_23` by running the following command from the project root directory:

      `docker build -t DWL_23 .`

   4. Start the docker containers by running the following command from the directory where `docker-compose.yaml` is located.

      ```docker compose up```

   (To stop and removes containers run ```docker compose down```)

3. **Access local Airflow Webserver**

   1. As soon as the airflow-webserver has been started you can access it at `http://localhost:8080`

      * Username: `airflow`

      * Password: `airflow`

   * Check if airflow-websever has started with the command `docker ps`. You should see an image with the name `dwl_23-airflow-webserver`

4. **Configure local PostgresDB**

To run the web scraper and Airflow locally, we need a database to store the scraped data. For this a separate PostgreSQL is included in the project as a Docker container.

* **Configure local PostgresDB in Airflow:**

  1. In Airflow go to Admin (top panel) > Variables.

  2. Click on blue "+", "Add a new record".

  3. Create the following variable:

     1. **Key:** `DATABASE_CONFIG`

     2. **Val:**

        `{
        "hostname": "dwl-postgres",
        "port": "5432",
        "user": "postgres",
        "password": "postgres",
        "database_name": "postgres"
        }`

* **Configure local PostgresDB in your DBTool:**

  1. Create a new connection with:
     * Host: `localhost`
     * Database: `postgres`
     * Port: `5433` (Note that port for Airflow variable is `5432`)
     * Username: `postgres`
     * Password: `postgres`

5. **Configure local bucket (Minio)**

   1. Minio can be accessed under `http://localhost:9090` as soon as the docker container has started successfully.

      * Username: `root`

      * Password: `password`

   2. Create Object in minio:

      * buckets > create new bucket with name `s3-raw-data-dwl23.1`(Name needs to be `BUCKET` variable in related DAG scripts)

   3. Create minio access Key:

      * Got to Access keys > Click on *Create*
      * Save credentials locally to have them ready for later

   4. Create the following variable:

      * In Airflow go to Admin (top panel) > Variables.
      * Click on blue "+", "Add a new record".
      * Create the following variable:
        1. **Key:** `ENVIRONMENT`
        2. **Val:** `LOCAL_DEV`

   5. Create connection in Airflow:

      * In Airflow go to Admin > Connections

      * Click on blue "+", "Add a new record".

      * Create the following Connection:

        1. **Connection Id:** `S3_DEVELOPMENT`

        2. **Connection Type:** `Amazon Web Services`

        3. **Extra (credentials from step 3. needed):**

           `{`

           `"aws_access_key_id": MINIOACCESSKEYID, "aws_secret_access_key": MINIOACCESSKEYSECRET, "endpoint_url": "http://minio:9000"`

           `}`

        4. Make sure that the fields `AWS AccessKey ID` & `AWS Secret Access Key` are empty fields.

## Airflow: DAG Visualization and Log Access

To verify that the following steps have worked and the pipelines arerunning as DAG, follow these steps in the Airflow UI:

1. Click on the "DAGs" option in the top menu to see the list of available DAGs.
2. Select a DAG e.g. `sync_hydro_data` from the list to view its details by clicking on the name.
3. You should now see a light green bar. Click on the light green point that corresponds to e.g. `sync_hydro_data`.
4. Next to the Details section you can see the `Logs`. Click on it and you should see the logs of the scraper.

### **Debugging and Rerunning scraper inside Airflow:**

**Colors:**

In Apache Airflow, the colors are used to represent the status of a DAG in the Airflow Web UI Here are the different colors used for DAG representation:

* *Green (Dark Green)* - dark green color represents a DAG that has successfully completed all of its tasks in the most recent run. This color indicates a successful and completed run of the DAG without any task failures.

* *Green (Light Green)* - light green is used to indicate that a DAG or a specific task is currently running or in progress. 

* *Red* - If a DAG or any of its tasks are displayed in red, it indicates that at least one task within the DAG has failed during the most recent run.

**Basic Debugging Comands**

* **Run DAG (if it has not started):** 
  * Click on the Play button on the top right of the DAG. 
* **Rerun DAG:**
  * You do not need to start a new DAG-run always for debugging.
  * You can also clear an existing DAG-run by going to the detail page of it and clicking on the blue button *"Clear"*. 
