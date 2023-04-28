from dataclasses import dataclass




@dataclass
class DatabaseConfig:
    hostname: str
    port: str
    user: str
    password: str
    db_name: str

    def connection_string(self):
        return f'postgresql+psycopg2://{self.user}:{self.password}@{self.hostname}:{self.port}/{self.db_name}'
