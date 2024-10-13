from flask import Blueprint, redirect

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

@payment_bp.route('/pay', methods=['GET', 'POST'])
def pay():
    """ Handles the payment for a booking"""
    return "I am paying now."