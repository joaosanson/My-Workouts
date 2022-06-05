import requests
from datetime import datetime
import os

TODAY = datetime.now().strftime("%d/%m/%Y")
TIME = datetime.now().strftime("%H:%M:%S")

APP_ID = os.environ.get("SHEETY_ID")
API_KEY = os.environ.get("SHEETY_API_KEY")

sheety_endpoint = os.environ.get("SHEETY_ENDPOINT")
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"


exercise_input = str(input("What did you do today? "))
exercise_config = {
    "query": exercise_input,
    "gender": "male",
    "weight_kg": 75,
    "height_cm": 170,
    "age": 17
}

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

response = requests.post(url=exercise_endpoint,
                         json=exercise_config,
                         headers=headers)
result = response.json()

#####################

for exercise in result["exercises"]:
    sheety_parameters = {
        "workout": {
            "date": TODAY,
            "time": TIME,
            "exercise": exercise['name'].title(),
            "duration(min)": round(exercise["duration_min"]),
            "calories": exercise["nf_calories"]
        }
    }

headers = (
    os.environ.get("USERNAME"),
    os.environ.get("PASSWORD")
)

sheet_response = requests.post(url=sheety_endpoint, json=sheety_parameters, auth=headers)
print(sheet_response.raise_for_status())
