import os
import time
import requests
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
client = MongoClient("mongodb://mongodb:27017/")
db = client["weather_db_v4"]
collection = db["weather_data"]

# Weather API settings
API_KEY = os.environ.get("WEATHER_API_KEY")
CITY = "Bangkok"
API_URL = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}"

def fetch_and_save_weather_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        # Add a timestamp before saving to MongoDB
        data["timestamp"] = datetime.utcnow()
        collection.insert_one(data)
        print(f"Data saved to MongoDB at {data['timestamp']}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
    except Exception as e:
        print(f"Error saving data to MongoDB: {e}")

if __name__ == "__main__":
    while True:
        fetch_and_save_weather_data()
        time.sleep(300) # Update every 5 minutes