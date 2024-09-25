from flask import Blueprint, render_template
from flask_login import login_required
from ..forms.passengerForm import PassengerForm

main_bp = Blueprint('main', __name__, url_prefix='/main')

# The route that handles the main page
@main_bp.route('/home', strict_slashes=False)
def home():
    """The app home page"""
    form = PassengerForm()
    return render_template('index.html', form=form)

@main_bp.route('/about', strict_slashes=False)
def about():
    """Gives more info about the app"""
    return render_template('about.html')

@main_bp.route('/', strict_slashes=False)
def landing():
    """ Takes one to the landing page """
    return render_template('landing.html')
