FROM apache/airflow:2.4.1-python3.10
FROM mcr.microsoft.com/playwright:focal
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/app"

COPY Pipfile .
COPY Pipfile.lock .

RUN apt-get update && apt-get install -y python3-pip
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile