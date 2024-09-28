# This is my Flask app entry file
from flask import Flask, render_template, g, jsonify
from flask_login import current_user, login_required
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv
import os
import json
from flask_apscheduler import APScheduler
from flask_wtf.csrf import generate_csrf
from flask_login import LoginManager

# Load environment variables
load_dotenv()

# Initialize the extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
cors = CORS()

# Initialize the Flask application
def create_app():
    app = Flask(__name__, static_folder='static')
    csrf.init_app(app)
    cors.init_app(app)  # Enable CORS for all routes
    mail.init_app(app)

    # The UPLOAD_FOLDER configuration
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')

    # Load configuration
    from config import Config
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'authorize.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from .routes.Booking import bp as booking_bp
    from .routes.Bus_status import bp as bus_status
    from .routes.Notification import notification_bp as notification_bp
    from .routes.Passenger import bp as passenger_bp
    from .routes.Receipts import receipts_bp as receipt_bp
    from .routes.traffic import traffic_bp as traffic_bp
    from .routes.weather import weather_bp as weather_bp
    from .routes.login import authorize_bp as authorize_bp
    from .routes.profile import profile_bp as profile_bp
    from .routes.booking_details import booking_details_bp as booking_details_bp
    from .routes.Users import users_bp as user_bp
    from .routes.payment import payment_bp as payment_bp
    from .routes.posts import post_bp as post_bp

    app.register_blueprint(booking_bp, url_prefix='/booking')
    app.register_blueprint(bus_status, url_prefix='/bus_status')
    app.register_blueprint(notification_bp, url_prefix='/notification')
    app.register_blueprint(passenger_bp, url_prefix='/passenger')
    app.register_blueprint(receipt_bp, url_prefix='/receipt')
    app.register_blueprint(traffic_bp, url_prefix='/traffic')
    app.register_blueprint(weather_bp, url_prefix='/weather')
    app.register_blueprint(authorize_bp, url_prefix='/authorize')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(booking_details_bp, url_prefix='/booking_details')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(payment_bp, url_prefix='/payment')
    app.register_blueprint(post_bp, url_prefix='/post')

    return app

# Flask application instance
app = create_app()

# Initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)

@scheduler.task('interval', id='check_notifications', seconds=3600)
def scheduled_task():
    from .utils.notifications import check_and_send_notifications
    with app.app_context():
        check_and_send_notifications()

scheduler.start()

# Adds headers to every request 
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=3600'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

# Closing all the resources used by the request
@app.teardown_request
def teardown_request(exception):
    if exception:
        print(f"Exception occurred: {exception}")
    # Close any database connections if needed
    if hasattr(g, 'db'):
        print("Closing the database connection")
        g.db.close()

# Generates the CSRF token
@app.route('/api/csrf-token', methods=['GET'], strict_slashes=False)
def get_csrf_token():
    token = generate_csrf()
    return jsonify({'csrf_token': token})

# Landing page route
@app.route('/', strict_slashes=False)
def landing():
    return render_template('landing.html')

# Home route
@app.route('/home', methods=['GET'], strict_slashes=False)
def index():
    from .forms.passengerForm import PassengerForm
    form = PassengerForm()
    from .models.Post import Post
    post = Post.query.all()
    is_admin = json.dumps(current_user.is_admin) if current_user.is_authenticated else 'false'
    return render_template('index.html', posts=post, form=form, is_admin=is_admin)

@app.route('/new', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def new_post():
    from .forms.posts import PostForm
    form = PostForm()
    from .models.Post import Post
    posts = Post.query.all()
    return render_template('index.html', posts=posts, form=form)

@app.route('/react', strict_slashes=False)
def react_index():
    return render_template('react_index.html')

@app.route('/account', strict_slashes=False)
@login_required
def account():
    from .forms.passengerForm import PassengerForm
    form = PassengerForm()
    return render_template('account.html', title='Account', form=form)

# Booking routes
@app.route('/booking', methods=['GET', 'POST'], strict_slashes=False)
def booking():
    from .forms.bookingForm import BookingForm
    form = BookingForm()
    return render_template('book.html', form=form)

@app.route('/booking/user_booking_details/<int:booking_id>', strict_slashes=False)
def user_booking_details(booking_id):
    return render_template('user_booking_details.html', booking_id=booking_id)

@app.route('/booking/passenger_booking_details/<int:booking_id>', strict_slashes=False)
def passenger_booking_details(booking_id):
    return render_template('passenger_booking_details.html', booking_id=booking_id)

# Promotions route
@app.route('/promotions', strict_slashes=False)
def promotions():
    promotions = [
        {
            'title': 'Special Discount!',
            'description': 'Get 20% off on all bookings this month.'
        },
        {
            'title': 'Summer Sale!',
            'description': 'Book now and enjoy discounted rates on selected routes.'
        }
    ]
    return render_template('promotions.html', promotions=promotions)

# Bus status routes
@app.route('/bus_status', methods=['GET', 'POST'], strict_slashes=False)
def bus_status():
    return render_template('bus_status.html')

@app.route('/add_bus', methods=['GET', 'POST'], strict_slashes=False)
def add_bus():
    from .forms.BusStatusForm import BusStatusForm
    form = BusStatusForm()
    return render_template('addBus.html', form=form)

@app.route('/bus_status/success', strict_slashes=False)
def success():
    return render_template('success.html')

# Notification route
@app.route('/notification', methods=['GET', 'POST'], strict_slashes=False)
def notification():
    return render_template('notification.html')

# Receipt route
@app.route('/receipt', strict_slashes=False)
def receipt():
    return render_template('receipt.html')

# Profile route
@app.route('/profile', methods=['GET', 'POST'], strict_slashes=False)
def profile():
    from .forms.forms import RegistrationForm
    form = RegistrationForm()
    return render_template('profile.html', user=current_user, form=form)

# Registration route
@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    from .forms.forms import RegistrationForm
    form = RegistrationForm()
    return render_template('register.html', user=current_user, form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    from .forms.forms import LoginForm
    form = LoginForm()
    return render_template('login.html', User=current_user, form=form)

# Password change route
@app.route('/change_password', strict_slashes=False)
def change_password():
    return render_template('profile.html')

@app.route('/user/users', strict_slashes=False)
def get_users():
    return render_template('get_users.html')

# User loader function for Flask-Login
from .models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
