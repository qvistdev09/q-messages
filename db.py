import psycopg2
from os import environ as env


def create_connection():
    return psycopg2.connect(
        f'dbname={env.get("DB_DATABASE")} user={env.get("DB_USER")} password={env.get("DB_PASSWORD")} host={env.get("DB_HOST")} port={env.get("DB_PORT")}')
