from flask import Flask, render_template, request, jsonify
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

app = Flask(__name__)

API_KEY = "75170f1aa2017d548f6a8c49c66c0aa9"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)

        if not location:
            return jsonify({"error": "City not found"}), 404

        obj = TimezoneFinder()
        timezone = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        home = pytz.timezone(timezone)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
            # https://api.openweathermap.org/data/3.0/onecall?lat={location.latitude}&lon={location.longitude}&exclude={part}&appid={API key}
        # Weather API
        # api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={API_KEY}"
        api_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={location.latitude}&lon={location.longitude}&appid={API_KEY}"
        response = requests.get(api_url)
        weather_data = response.json()

        if weather_data.get("cod") != 200:
            return jsonify({"error": weather_data.get("message", "Invalid response")}), 400

        condition = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temp = int(weather_data['main']['temp'] - 273.15)
        pressure = weather_data['main']['pressure']
        humidity = weather_data['main']['humidity']
        wind = weather_data['wind']['speed']

        return jsonify({
            "time": current_time,
            "condition": condition,
            "description": description,
            "temperature": temp,
            "pressure": pressure,
            "humidity": humidity,
            "wind": wind,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
