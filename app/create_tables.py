from app import app
from models import db

try:
    # Create the tables
    with app.app_context():
        db.create_all()  # This will create all tables defined by SQLAlchemy models
    print("Tables created successfully!")

except Exception as e:
    print(f"An error occurred while creating tables: {e}")
