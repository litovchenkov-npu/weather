from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "API_KEY" # API ключ OpenWeatherMap

# Клас Model відповідає за взаємодію з API для отримання погодових даних.
class Model:
    # Метод для отримання поточних погодових даних для вказаного міста.
    def get_weather_data(self, city):
        try:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
            response = requests.get(url)

            if response.status_code == 200:
                weather_data = response.json()
                return weather_data
            else:
                return {"error": f"Помилка під час отримання даних про погоду. Код стану: {response.status_code}"}
        except Exception as e:
            return {"error": f"Трапилася помилка: {e}"}

    # Метод для отримання тижневого прогнозу погоди для вказаного міста.
    def get_weekly_forecast(self, city):
        try:
            url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
            response = requests.get(url)

            if response.status_code == 200:
                forecast_data = response.json()
                return forecast_data
            else:
                return {"error": f"Помилка під час отримання даних про погоду. Код стану: {response.status_code}"}
        except Exception as e:
            return {"error": f"Виникла помилка: {e}"}

model = Model()

# Маршрут для отримання поточних погодових даних через HTTP GET-запит.
@app.route('/get_weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if city:
        weather_data = model.get_weather_data(city)
        return jsonify(weather_data)
    else:
        return jsonify({"error": "Будь ласка, введіть назву міста"})

# Маршрут для отримання тижневого прогнозу погоди через HTTP GET-запит.
@app.route('/get_weekly_forecast', methods=['GET'])
def get_weekly_forecast():
    city = request.args.get('city')
    if city:
        weekly_forecast_data = model.get_weekly_forecast(city)
        return jsonify(weekly_forecast_data)
    else:
        return jsonify({"error": "Будь ласка, введіть назву міста"})

if __name__ == '__main__':
    app.run(debug=True)