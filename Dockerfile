FROM apache/airflow:2.4.1-python3.10
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/app"

COPY Pipfile .
COPY Pipfile.lock .