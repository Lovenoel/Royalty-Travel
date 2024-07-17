import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Initialize the database instance
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    # Create a Flask instance
    app = Flask(__name__, static_folder='static')
    csrf.init_app(app)
    CORS(app)  # This will enable CORS for all routes

    # Load environment variables from .env file
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '..', '.env'))

    # Set configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['DEBUG'] = True
    app.secret_key='1acbf156e7c5a3dfe0f5cb6e3e8377156e1e2c2400b585ce8d1abe26645b47e8'
    
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
    from app.routes.home import main_bp  as main_bp
    from app.routes.Booking import bp as booking_bp
    from app.routes.Bus_status import bp as bus_status_bp
    from app.routes.Notification import notification_bp as notification_bp
    from app.routes.Passenger import bp as passenger_bp
    from app.routes.Receipts import receipts_bp as receipt_bp
    from app.routes.traffic import traffic_bp as traffic_bp
    from app.routes.weather import weather_bp as weather_bp
    from app.routes.login import authorize_bp as authorize_bp
    from app.routes.profile import profile_bp as profile_bp
    from app.routes.booking_details import booking_details_bp as booking_details_bp
    from app.routes.Users import users_bp as user_bp

    app.register_blueprint(main_bp, url_prefix='/main')
    app.register_blueprint(booking_bp, url_prefix='/booking')
    app.register_blueprint(bus_status_bp, url_prefix='/bus_status')
    app.register_blueprint(notification_bp, url_prefix='/notification')
    app.register_blueprint(passenger_bp, url_prefix='/passenger')
    app.register_blueprint(receipt_bp, url_prefix='/receipt')
    app.register_blueprint(traffic_bp, url_prefix='/traffic')
    app.register_blueprint(weather_bp, url_prefix='/weather')
    app.register_blueprint(authorize_bp, url_prefix='/authorize')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(booking_details_bp, url_prefix='/booking_details')
    app.register_blueprint(user_bp, url_prefix='/user')
    
    return app

from app.models.User import User

# Define the user loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app = create_app()
    print("Starting the Flask development server on http://127.0.0.1:5000/")
    app.run(debug=True)
