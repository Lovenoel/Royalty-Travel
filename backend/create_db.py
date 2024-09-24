import os
from app import create_app, db
from flask_migrate import Migrate, upgrade
from app.models.User import User  # Import your User model here

# Create an instance of the Flask application
app = create_app()

# Initialize Flask-Migrate
migrate = Migrate(app, db)

def create_database_tables():
    """Create database tables based on the defined models."""
    with app.app_context():
        db.create_all()  # Create all tables in the database
        print("Database tables created.")

def migrate_database():
    """Run database migrations."""
    with app.app_context():
        # Check if migrations folder exists, if not, initialize it
        if not os.path.exists('migrations'):
            print("Initializing migrations folder...")
            from flask_migrate import init
            init(app)
            print("Migrations folder created.")

        upgrade()  # Apply any pending migrations
        print("Database migrations applied.")

def seed_database():
    """Seed the database with initial data."""
    with app.app_context():
        # Example: Adding a user
        if not User.query.filter_by(username='admin').first():  # Check if user already exists
            new_user = User(username='admin', email='admin@example.com', password='password')  # Adjust as necessary
            db.session.add(new_user)
            db.session.commit()
            print("Database seeded with initial data.")
        else:
            print("Admin user already exists.")

if __name__ == "__main__":
    create_database_tables()  # Create tables
    migrate_database()         # Run migrations
    seed_database()            # Seed database

