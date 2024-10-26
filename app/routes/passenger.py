from flask import Blueprint, render_template
from flask_login import login_required

passenger_bp = Blueprint('passenger', __name__, url_prefix='/passenger')

@passenger_bp.route('/handle_passengers', methods=['GET', 'POST'])
@login_required
def handle_passengers():
    """Endpoint that handles passengers. """
    return render_template('passenger.html')