import json
import os
import psycopg2
from datetime import datetime

sub_delta = []
previous_count = 0

def lambda_handler(event, context):
    get_count_and_delta()

def get_from_all_countries(query):
    countries = os.environ.get('COUNTRIES').split(',')
    results = {}
    for country in countries:
        host = os.environ.get('COUNTRY_HOST') .replace(
            "ZZZ", country
        )
        user = os.environ.get('COUNTRY_USER') 
        password = os.environ.get('COUNTRY_PASSWORD') 
        conn = psycopg2.connect(
            host=host, database=country, user=user, password=password
        )

        cursor = conn.cursor()
        query = query
        cursor.execute(query)
        results[country] = cursor.fetchall()

        cursor.close()
        conn.close()

    return results

def get_count_and_delta():
    query = "SELECT COUNT(*) FROM responses"
    results = get_from_all_countries(query)
    row_count = sum(results.values())

    # calc and record submission count delta
    row_count_delta = row_count - previous_count
    previous_count = row_count

    sub_delta.append({"x": datetime.now(), "y": row_count_delta})

    if len(sub_delta) > 86400: # one day, in seconds
        sub_delta = sub_delta[1:]

    # build and return json structure
    result = {
        "count": row_count,
        "datasets": [
            {
                "id": "Submissions",
                "data": sub_delta
            }
        ]
        }
    print(f"This is the total no of submissions: {result}")
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
