import json
import os
import psycopg2
from datetime import datetime

# import time

# from dotenv import load_dotenv

# load_dotenv()


def lambda_handler(event, context):
    if "detail-type" in event:
        print(f":::: EventBridge called ::::", data)
        get_subs_over_time()

    else:
        print(":::: API called ::::", data)
        return {"statusCode": 200, "body": json.dumps(data)}

total_subs = 0
hours = [
    {'x': "00:00", 'y':0},
    {"x": "01:00", 'y':0},
    {"x": "02:00", 'y':0},
    {"x": "03:00", 'y':0},
    {"x": "04:00", 'y':0},
    {"x": "05:00", 'y':0},
    {"x": "06:00", 'y':0},
    {"x": "07:00", 'y':0},
    {"x": "08:00", 'y':0},
    {"x": "09:00", 'y':0},
    {"x": "10:00", 'y':0},
    {"x": "11:00", 'y':0},
    {"x": "12:00", 'y':0},
    {"x": "13:00", 'y':0},
    {"x": "14:00", 'y':0},
    {"x": "15:00", 'y':0},
    {"x": "16:00", 'y':0},
    {"x": "17:00", 'y':0},
    {"x": "18:00", 'y':0},
    {"x": "19:00", 'y':0},
    {"x": "20:00", 'y':0},
    {"x": "21:00", 'y':0},
    {"x": "22:00", 'y':0},
    {"x": "23:00", 'y':0},
]
data = {"datasets": [{"id": "Submissions", "data": hours}]}
latest_hour = 0


def get_subs_over_time():
    global total_subs
    global latest_hour
    global data

    hour_now = datetime.now().hour
    total_row_count = 0

    countries = os.environ.get("COUNTRIES").split(",")
    for country in countries:
        host = os.environ.get("COUNTRY_HOST").replace("ZZZ", country)
        user = os.environ.get("COUNTRY_USER")
        password = os.environ.get("COUNTRY_PASSWORD")
        conn = psycopg2.connect(
            host=host, database=country, user=user, password=password
        )

        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM responses"
        cursor.execute(query)
        row_count = cursor.fetchone()[0]
        total_row_count += row_count

    cursor.close()
    conn.close()

    if latest_hour != hour_now:
        latest_hour = hour_now
        total_subs = 0

    if total_subs == 0:
        total_subs = total_row_count

    for each in data["datasets"][0]["data"]:
        print(f"processing hour {each}")
        if each['x'] == f'{datetime.now().hour}:00':
            each['y'] = total_row_count - total_subs
    print(":::: Function Data ::::", data)
