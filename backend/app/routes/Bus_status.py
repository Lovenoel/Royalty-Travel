from flask import Blueprint, request, jsonify
from app.models import Bus, BusStatus, db

# Create a Blueprint for bus-related routes under '/bus_status'
bp = Blueprint('bus_routes', __name__, url_prefix='/bus_status')

@bp.route('/enter_bus/<int:bus_id>', methods=['POST'])
def enter_bus(bus_id):
    """
    Endpoint for a passenger entering a bus.

    Args:
    - bus_id (int): The ID of the bus to enter.

    Returns:
    - JSON response with updated passenger count if successful.
    - JSON response indicating bus is full if capacity reached.
    - JSON response indicating bus not found if bus with given ID doesn't exist.
    """
    bus = Bus.query.get(bus_id)  # Retrieve the bus from the database by ID
    if bus and bus.current_passenger_count < bus.capacity:
        # Increment passenger count if there's capacity
        bus.current_passenger_count += 1
        db.session.commit()  # Commit changes to the database
        return jsonify({
            "message": "Passenger count updated",
            "current_passenger_count": bus.current_passenger_count
        }), 200
    elif bus:
        # Return error message if bus is full
        return jsonify({"message": "Bus is full"}), 400
    return jsonify({"message": "Bus not found"}), 404  # Return error message if bus not found

@bp.route('/buses_in_area', methods=['GET'])
def buses_in_area():
    """
    Endpoint for retrieving buses in a specific area.

    Returns:
    - JSON response with number of buses and their details in the specified area.
    """
    area = request.args.get('area')  # Get 'area' parameter from query string
    buses = Bus.query.filter_by(location=area).all()  # Query buses in the specified area
    return jsonify({
        "number_of_buses": len(buses),  # Number of buses found in the area
        "buses": [{"id": bus.id,
                   "number_plate": bus.number_plate} for bus in buses]
        # List of buses in the area with their IDs and number plates
    }), 200

@bp.route('/bus-status', methods=['GET'])
def get_bus_status():
    """
    Endpoint for retrieving status of all buses.

    Returns:
    - JSON response with status details of all buses.
    """
    # Retrieve all bus statuses from the database
    buses = BusStatus.query.all()

    # Convert bus status objects to dictionaries and return as JSON
    return jsonify([bus.to_dict() for bus in buses])
