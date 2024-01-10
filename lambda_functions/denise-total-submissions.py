import json
import os
import psycopg2

def lambda_handler(event, context):
    countries = os.environ.get('COUNTRIES').split(',')
    row_count = 0
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
        query = "SELECT COUNT(*) FROM responses"
        cursor.execute(query)
        row_count += cursor.fetchone()[0]

        cursor.close()
        conn.close()
    result = {"count": row_count}
    print(f"This is the total no of submissions: {result}")
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
