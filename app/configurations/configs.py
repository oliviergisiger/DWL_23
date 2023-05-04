from datetime import datetime
from dataclasses import dataclass


@dataclass
class Environment:
    environment: str
    connections: dict
    dag_start_date: datetime
    dag_end_data: datetime = None


LOCAL_DEV = Environment(
    environment='LOCAL_DEV',
    connections={'S3': 'S3_DEVELOPMENT'},
    dag_start_date=datetime(2023, 3, 25),
    dag_end_data=datetime(2023, 3, 31)
)

PRODUCTION = Environment(
    environment='PRODUCTION',
    connections={'S3': 'S3_PRODUCTION'},
    dag_start_date=datetime(2023, 3, 25),
    dag_end_data=None
)




