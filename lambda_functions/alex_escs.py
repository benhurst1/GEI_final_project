import json
import os
import psycopg2
# from dotenv import load_dotenv


# load_dotenv()

def lambda_handler(event, context):
    return(get_escs())

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
        results[country] = cursor.fetchone()[0]

        cursor.close()
        conn.close()

    return results

def get_escs():
    query_1 = """
    SELECT
        AVG(CAST(escs AS float))
    FROM
        responses
    WHERE
        escs != 'NA';
"""
    avg_standardized = get_from_all_countries(query_1)

    datasets = []

    for key, value in avg_standardized.items():
        datasets.append({
            "id": key.upper(),
            "value": round(value, 4)
        })

    result = {"datasets": datasets}
    print(result)
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }