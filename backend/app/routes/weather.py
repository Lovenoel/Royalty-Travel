from flask import Blueprint, request, jsonify
import requests

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/weather', methods=['GET'], strict_slashes=False)
def get_weather():
    """
    Endpoint to fetch weather data for a specified city using OpenWeatherMap API.

    Query Parameters:
    - city (str): Name of the city for which weather data is requested.

    Returns:
    - JSON response with weather data if successful.
    - Error message with status code 400 if city parameter is missing.
    - Error message with status code 500 if weather data retrieval fails.
    """
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    api_key = 'your_openweather_api_key'  # Replace with your actual OpenWeatherMap API key
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Could not retrieve weather data'}), 500

