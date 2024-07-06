from flask import Blueprint, request, jsonify
import requests

traffic_bp = Blueprint('traffic', __name__, url_prefix='/traffic')

@traffic_bp.route('/traffic', methods=['GET'])
def get_traffic():
    # Retrieve origin and destination parameters from the request query string
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    
    # Validate that origin and destination parameters are provided
    if not origin or not destination:
        return jsonify({'error': 'Origin and destination parameters are required'}), 400

    # Replace 'your_traffic_api_key' with your actual TomTom API key
    api_key = 'your_traffic_api_key'
    
    # Construct the URL for the TomTom API request
    url = f'https://api.tomtom.com/routing/1/calculateRoute/{origin}:{destination}/json?key={api_key}'
    
    # Send a GET request to the TomTom API
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        return jsonify(response.json())  # Return the JSON response from the API
    else:
        return jsonify({'error': 'Could not retrieve traffic data'}), 500
        # Return an error message if the request was not successful (status code != 200)
