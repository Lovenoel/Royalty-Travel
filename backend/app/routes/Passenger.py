from flask import Blueprint, request, jsonify, render_template, flash
from app.models import Passenger
from app import db
from sqlalchemy.exc import IntegrityError

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
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        print('Received data:', data)
        try:
            if not data or 'username' not in data or 'email' not in data or 'phone' not in data:
                return jsonify({'error': 'Invalid data'}), 400
            new_passenger = Passenger(
                username=data['username'],
                email=data['email'],
                phone=data['phone'])  # Create a new Passenger object
            db.session.add(new_passenger)  # Add new passenger to the session
            db.session.commit()  # Commit changes to the database
            flash('Passenger created successfully', 'success')
            # Return newly created passenger details with status code 201
            return jsonify({"Message": "Passenger created successfully"}), 201
            # return jsonify(new_passenger.to_dict()), 201
        except IntegrityError as e:
            db.session.rollback()  # Rollback the session in case of an error
            error_message = str(e.orig)  # Get the original error message from SQLAlchemy
            if 'UNIQUE constraint failed: passenger.username' in error_message:
                return jsonify({'error': 'Username already exists. Please choose a different username.'}), 400
            elif 'UNIQUE constraint failed: passenger.phone' in error_message:
                return jsonify({'error': 'Phone number already exists. Please use a different phone number.'}), 400
            elif 'UNIQUE constraint failed: passenger.email' in error_message:
                return jsonify({'error': 'Email already exists. Please use a different email.'}), 400
            else:
                return jsonify({'error': 'Database integrity error.'}), 400
        except KeyError as e:
            return jsonify({'error': f'Missing required field: {str(e)}'}), 400
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
        'username': passenger.username,
        'email': passenger.email,
        'phone': passenger.phone
    })

@bp.route('/passenger/<int:id>/details', methods=['GET'])
def show_passenger_details(id):
    """
    Endpoint for rendering the passenger details HTML template.

    Args:
    - id (int): ID of the passenger to retrieve and display details for.

    Returns:
    - Rendered HTML template 'passenger.html' with details of the specified passenger.
    """
    passenger = Passenger.query.get_or_404(id)  # Retrieve passenger by ID or return 404 if not found
    return render_template('passenger.html', passenger=passenger)


@bp.route('/add', methods=['GET'])
def add_passenger_page():
    """Endpoint for adding a passenger"""
    return render_template('add_passenger.html')