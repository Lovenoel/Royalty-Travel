# Initializes the whole application
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from dotenv import load_dotenv

# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Initialize the database instance
db = SQLAlchemy()

def create_app():
    # Create a Flask instance
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)

    with app.app_context():

        # Imports bp from the routes of the app
        from routes.register import register_bp as register_bp
        from routes.Booking import bp as booking_bp
        from routes.Bus_status import bp as bus_status_bp
        from routes.Notification import bp as notification_bp
        from routes.Passenger import bp as passenger_bp
        from routes.Receipts import bp as receipt_bp
        from routes.traffic import traffic_bp as traffic_bp
        from routes.weather import weather_bp as weather_bp

        # Register blueprints and their url_prefix
        app.register_blueprint(register_bp, url_prefix='/auth')
        app.register_blueprint(booking_bp, url_prefix='/booking')
        app.register_blueprint(bus_status_bp, url_prefix='/bus_status')
        app.register_blueprint(notification_bp, url_prefix='/notification')
        app.register_blueprint(passenger_bp, url_prefix='/passenger')
        app.register_blueprint(receipt_bp, url_prefix='/receipt')
        app.register_blueprint(traffic_bp, url_prefix='/traffic')
        app.register_blueprint(weather_bp, url_prefix='/weather')
        
        return app

if __name__ == '__main__':
    # Runs the application when executed directly only
    app = create_app()
    print("Starting the Flask development server on http://127.0.0.1:5000/")
    app.run(debug=True)

