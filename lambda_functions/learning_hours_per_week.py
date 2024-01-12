import json
import psycopg2
import os
# from dotenv import load_dotenv
# load_dotenv()

def lambda_handler(event, context):
    return calculate_tmins()

def calculate_tmins():
    countries = os.environ.get('COUNTRIES').split(',')
    result = {
        "datasets": []
        }
    for country in countries:
        host = os.environ.get('COUNTRY_HOST').replace(
            "ZZZ", country
        )
        user = os.environ.get('COUNTRY_USER') 
        password = os.environ.get('COUNTRY_PASSWORD') 
        conn = psycopg2.connect(
            host=host, database=country, user=user, password=password
        )
        cursor = conn.cursor()
        query = "SELECT ROUND(AVG(CAST(TMINS AS NUMERIC))/60) FROM responses WHERE TMINS != 'NA'"
        cursor.execute(query)
        learning_hours_per_week = int(cursor.fetchone()[0])
        country_code = country.upper()
        country_dict = {
            "country": country_code,
            "hours": learning_hours_per_week
        }
        # print(f"Here's the country dict: {country_dict}")
        result["datasets"].append(country_dict)
        cursor.close()
        conn.close()

    print(f"Here's the returned output: {result}")
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }

# calculate_tmins()