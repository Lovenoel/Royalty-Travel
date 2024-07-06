from app import db  # Import the db instance from the app
from flask import Blueprint, request, jsonify  # Import necessary Flask components
from app.services.receipt_service import ReceiptService  # Import the ReceiptService from services

# Create a Blueprint named 'receipts' with URL prefix '/receipt'
receipts_bp = Blueprint('receipts', __name__, url_prefix='/receipt')

# Example in-memory database (you may replace this with SQLAlchemy or another database)
db = {
    "receipts": []
}

# Initialize the ReceiptService with the db instance
receipt_service = ReceiptService(db)

# Route to fetch all receipts via GET request
@receipts_bp.route('/receipts', methods=['GET'])
def get_receipts():
    """
    GET method to fetch all receipts.

    Returns:
        JSON response with all receipts and HTTP status 200.
    """
    receipts = receipt_service.get_receipts()  # Call the ReceiptService to fetch all receipts
    return jsonify(receipts), 200  # Return JSON response with receipts data and HTTP status 200

# Route to create a new receipt via POST request
@receipts_bp.route('/receipts', methods=['POST'])
def create_receipt():
    """
    POST method to create a new receipt.

    JSON Payload:
        {
            "booking_id": <int>,
            "amount": <float>,
            "payment_method": <str>
        }

    Returns:
        JSON response with the newly created receipt and HTTP status 201.
    """
    data = request.get_json()  # Parse JSON data from the request body
    new_receipt = receipt_service.create_receipt(
        data['booking_id'],  # Extract booking_id from JSON data
        data['amount'],  # Extract amount from JSON data
        data['payment_method']  # Extract payment_method from JSON data
    )
    return jsonify(new_receipt), 201  # Return JSON response with new receipt data and HTTP status 201

# Route to fetch a specific receipt by its ID via GET request
@receipts_bp.route('/receipts/<int:receipt_id>', methods=['GET'])
def get_receipt_by_id(receipt_id):
    """
    GET method to fetch a specific receipt by its ID.

    Args:
        receipt_id (int): ID of the receipt to fetch.

    Returns:
        JSON response with the receipt data and HTTP status 200 if found,
        or JSON response with error message and HTTP status 404 if not found.
    """
    receipt = receipt_service.get_receipt_by_id(receipt_id)  # Call the ReceiptService to fetch receipt by ID
    if receipt:
        return jsonify(receipt), 200  # Return JSON response with receipt data and HTTP status 200 if found
    else:
        return jsonify({"error": "Receipt not found"}), 404  # Return JSON response with error message and HTTP status 404 if not found
