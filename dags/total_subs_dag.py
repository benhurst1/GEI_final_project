from datetime import datetime, timedelta, date
from airflow import DAG
from airflow.operators.python import PythonOperator

from airflow.models import Variable
import psycopg2, json

# import os
import logging

# from dotenv import load_dotenv

# load_dotenv()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "total_subs",
    default_args=default_args,
    description="calculate total subs",
    schedule_interval=timedelta(minutes=5),
    start_date=datetime(2024, 1, 3),
    catchup=False,
)


def calculate_subs():
    countries = Variable.get("COUNTRIES").split(',')

    row_count = 0
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

        row_count += cursor.fetchone()[0]

        cursor.close()
        conn.close()
    result = {"count": row_count}
    logging.info(result)
    return json.dumps(result)


calculate_subs_task = PythonOperator(
    task_id="calculate_subs", python_callable=calculate_subs, dag=dag
)

calculate_subs_task
