import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Initialize the database instance
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'login'


def create_app():
    # Create a Flask instance
    app = Flask(__name__, static_folder='static')
    csrf = CSRFProtect(app)

    # Load environment variables from .env file
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '..', '.env'))

    # Set configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Load configuration
    from config import Config
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)


    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    
    # Register blueprints
    from app.routes.Booking import bp as booking_bp
    from app.routes.Bus_status import bp as bus_status_bp
    from app.routes.Notification import notification_bp as notification_bp
    from app.routes.Passenger import bp as passenger_bp
    from app.routes.Receipts import receipts_bp as receipt_bp
    from app.routes.traffic import traffic_bp as traffic_bp
    from app.routes.weather import weather_bp as weather_bp
    from app.routes.login import authorize_bp as authorize_bp
    from app.routes.profile import profile_bp as profile_bp
    from app.routes.loginform import login_bp as login_bp
    from app.routes.register import register_bp as register_bp
    from app.routes.booking_details import booking_details_bp as booking_details_bp

    app.register_blueprint(booking_bp, url_prefix='/booking')
    app.register_blueprint(bus_status_bp, url_prefix='/bus_status')
    app.register_blueprint(notification_bp, url_prefix='/notification')
    app.register_blueprint(passenger_bp, url_prefix='/passenger')
    app.register_blueprint(receipt_bp, url_prefix='/receipt')
    app.register_blueprint(traffic_bp, url_prefix='/traffic')
    app.register_blueprint(weather_bp, url_prefix='/weather')
    app.register_blueprint(authorize_bp, url_prefix='/authorize')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(register_bp, url_prefix='/register')
    app.register_blueprint(booking_details_bp, url_prefix='/booking_details')
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("Starting the Flask development server on http://127.0.0.1:5000/")
    app.run(debug=True)
