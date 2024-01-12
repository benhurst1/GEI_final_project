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
        # get avg duration of a class (mins) and number of classes per week for each student
        query = "SELECT ROUND(AVG(CAST(TMINS AS NUMERIC))/60) FROM responses WHERE TMINS != 'NA'"
        # query = "SELECT ST061Q01NA, ST060Q01NA FROM responses"
        cursor.execute(query)
        learning_hours_per_week = int(cursor.fetchone()[0])
        # students = cursor.fetchall()
        # student_count = 0
        # country_total_mins = 0
        # for student in students:
        #     avg_mins_per_class = student[0]
        #     # print(f"Average minutes: {avg_mins_per_class}")
        #     total_classes_per_week = student[1]
        #     # print(f"Total classes: {total_classes_per_week}")
        #     # filter out NA for avg mins and total classes
        #     if avg_mins_per_class != "NA" and total_classes_per_week != "NA":
        #         student_count += 1
        #         student_total_mins = int(avg_mins_per_class) * int(total_classes_per_week)
        #         country_total_mins += student_total_mins
        # learning_mins_per_week = round(country_total_mins/student_count)
        # learning_hours_per_week = round(learning_mins_per_week/60)
        country_code = country.upper()
        # print(f"Country code: {country_code}'s tmins per week is {learning_mins_per_week}")
        country_dict = {
            "country": country_code,
            "hours": learning_hours_per_week
        }
        # print(f"Here's the country dict: {country_dict}")
        result["datasets"].append(country_dict)
        # fetch st061 (ST061Q01NA) value (avg duration of a class in mins)
        # fetch st060 (ST060Q01NA) value (total number of class periods attended per week)
        # formula to calculate tmins
        # TMINS = ST061 × ST060
        cursor.close()
        conn.close()

    print(f"Here's the returned output: {result}")
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }

calculate_tmins()