import requests
import datetime as dt
import os
from dotenv import load_dotenv
load_dotenv()

# ------ ENV VARIABLES -------- #
# Nutrition
APP_ID = os.environ.get('APP_ID')
APP_KEY = os.environ.get('APP_KEY')

# Sheety
APP_TOKEN_SHEETY = os.environ.get('APP_TOKEN_SHEETY')
SHEETY_ENDPOINT = os.environ.get('SHEETY_ENDPOINT')

# --------- POST TO NUTRITIONIX ---------- #
# NUTRITIONIX ENDPOINT
workout_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'

headers_nutritionix = {
    'x-app-id': APP_ID,
    'x-app-key': APP_KEY
}

# User input query
workout_config = {
    'query': input('Tell me which exercise you did: ')
}

response = requests.post(url=workout_endpoint, json=workout_config, headers=headers_nutritionix)
exercises_data = response.json()['exercises']

# --------- POST SHEETY -------------- #
# Format current date and time
now = dt.datetime.now()
date = now.strftime('%d/%m/%Y')
time = now.strftime('%H:%M:%S')

# Go through each exercise and add a row
for exercise in exercises_data:
    workout_config = {
        'workout': {
            'date': date,
            'time': time,
            'exercise': exercise['name'].title(),
            'duration': exercise['duration_min'],
            'calories': exercise['nf_calories']
        }
    }
    headers_sheety = {
        'Authorization': f'Bearer {APP_TOKEN_SHEETY}'
    }
    response = requests.post(url=SHEETY_ENDPOINT, json=workout_config, headers=headers_sheety)
    # print(response.text)
