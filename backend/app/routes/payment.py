from flask import Blueprint, request, redirect, render_template


payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

@payment_bp.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        # Extract payment details from the form submission
        passenger_name = request.form.get('passenger_name')
        departure_place = request.form.get('departure_place')
        destination = request.form.get('destination')


        
@payment_bp.route('/success')
def success_page():
    return render_template('success.html')
