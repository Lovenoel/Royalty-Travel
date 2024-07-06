from flask import Blueprint, request, jsonify
from app.models import Passenger
from app import db

# Create a Blueprint for passenger-related routes under '/passenger'
bp = Blueprint('passengers', __name__, url_prefix='/passenger')

@bp.route('/passengers', methods=['GET', 'POST'])
def handle_passengers():
    """
    Endpoint for handling multiple passengers.

    GET Method:
    - Retrieves all passengers from the database.
    - Returns JSON response with details of all passengers.

    POST Method:
    - Creates a new passenger based on JSON data in the request body.
    - Adds the new passenger to the database.
    - Returns JSON response with details of the newly created passenger.

    Returns:
    - JSON response with passengers' details or newly created passenger's details.
    """
    if request.method == 'GET':
        # Handle GET request to retrieve all passengers
        passengers = Passenger.query.all()
        return jsonify([passenger.to_dict() for passenger in passengers])
    
    elif request.method == 'POST':
        # Handle POST request to create a new passenger
        data = request.get_json()
        new_passenger = Passenger(name=data['name'])  # Create a new Passenger object
        db.session.add(new_passenger)  # Add new passenger to the session
        db.session.commit()  # Commit changes to the database
        return jsonify(new_passenger.to_dict()), 201  # Return newly created passenger details with status code 201

@bp.route('/passenger/<int:id>', methods=['GET'])
def get_passenger(id):
    """
    Endpoint for retrieving a specific passenger by ID.

    Args:
    - id (int): ID of the passenger to retrieve.

    Returns:
    - JSON response with details of the specified passenger.
    """
    passenger = Passenger.query.get_or_404(id)  # Retrieve passenger by ID or return 404 if not found
    return jsonify({
        'id': passenger.id,
        'name': passenger.name,
        'email': passenger.email,  # Assuming email and phone are attributes of Passenger model
        'phone': passenger.phone
    })
