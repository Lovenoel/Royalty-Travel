import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail

# Initialize the database instance
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
cors = CORS()


def create_app():
    # Create a Flask instance
    app = Flask(__name__, static_folder='static')
    csrf.init_app(app)
    cors.init_app(app)  # This will enable CORS for all routes
    mail.init_app(app)

    # The UPLOAD_FOLDER configuration
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')

    # Load configuration
    from backend.config import Config
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'authorize.login'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    # from .routes.home import main_bp  as main_bp
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

    # app.register_blueprint(main_bp, url_prefix='/main')
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

from .models import User

# Define the user loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))