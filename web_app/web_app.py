import os
from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime
import pytz # เพิ่มบรรทัดนี้

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://mongodb:27017/")
db = client["weather_db_v4"]
collection = db["weather_data"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/current_data")
def get_current_data():
    try:
        data = collection.find().sort("timestamp", -1).limit(1)
        if data:
            latest_data = data[0]

            # Convert UTC timestamp to Asia/Bangkok timezone
            utc_time = latest_data["timestamp"]
            bangkok_tz = pytz.timezone("Asia/Bangkok")
            bangkok_time = utc_time.astimezone(bangkok_tz)

            current_weather = {
                "location": latest_data["location"]["name"],
                "temperature": latest_data["current"]["temp_c"],
                "humidity": latest_data["current"]["humidity"],
                "description": latest_data["current"]["condition"]["text"],
                "wind_speed": latest_data["current"]["wind_kph"],
                "pressure": latest_data["current"]["pressure_mb"],
                "last_updated_timestamp": bangkok_time.isoformat() # ใช้เวลาที่แปลงแล้ว
            }
            return jsonify(current_weather)
        return jsonify({"error": "No data found."})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/history_data")
def get_history_data():
    try:
        history = list(collection.find().sort("timestamp", -1).limit(12))
        
        # Convert timestamps to Asia/Bangkok timezone before formatting
        bangkok_tz = pytz.timezone("Asia/Bangkok")
        timestamps_thai = [item["timestamp"].astimezone(bangkok_tz).strftime("%H:%M") for item in reversed(history)]
        
        chart_data = {
            "timestamps": timestamps_thai, # ใช้เวลาที่แปลงแล้ว
            "temperatures": [item["current"]["temp_c"] for item in reversed(history)]
        }
        return jsonify(chart_data)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)