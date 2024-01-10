from datetime import datetime, timedelta, date
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import psycopg2
import json
import logging


def calculate_escs():
    countries = Variable.get("COUNTRIES").split(',')

    for country in countries:
        host = Variable.get("COUNTRY_HOST").replace(
            "ZZZ", country
        )
        user = Variable.get("COUNTRY_USER")
        password = Variable.get("COUNTRY_PASSWORD")
        conn = psycopg2.connect(
            host=host, database=country, user=user, password=password
        )
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM responses"
        cursor.execute(query)

        cursor.close()
        conn.close()

    logging.info(result)
    return json.dumps(result)