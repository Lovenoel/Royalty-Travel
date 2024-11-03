# import os
# from app import app
# from models import db
# from flask_migrate import Migrate, upgrade
# from models.users import User


# # Initialize Flask-Migrate
# migrate = Migrate(app, db)


# def create_database_tables():
#     """Create database tables based on the defined models."""
#     try:
#         # Create the tables
#         with app.app_context():
#             db.create_all()  # This will create all tables defined by SQLAlchemy models
#         print("Tables created successfully!")

#     except Exception as e:
#         print(f"An error occurred while creating tables: {e}")


# def migrate_database():
#     """Runs migrations on the database"""
#     with app.app_context():
#         # Check if migrations folder exists, if not, initialize it
#         if not os.path.exists('migrations'):
#             print("Initializing migrations' folder...")
#             # from flask_migrate import init
#             # init(app)
#             migrate.init_app(app, db)
#             print('Migration folder created')

#         upgrade()
#         print('Database migrations applied')


# def seed_database():
#     """Seed the database with initial data."""
#     with app.app_context():
#         # Example: Adding a user
#         if not User.query.filter_by(username='admin').first():  # Check if user already exists
#             new_user = User(username='admin', email='admin@example.com', password='password')  # Adjust as necessary
#             db.session.add(new_user)
#             db.session.commit()
#             print("Database seeded with initial data.")
#         else:
#             print("Admin user already exists.")


# if __name__ == "__main__":
#     create_database_tables()  # Create tables
#     migrate_database()         # Run migrations
#     seed_database()            # Seed database


import os
from models import db
from app import app
from flask_migrate import Migrate, upgrade
from models.users import User  # Import your User model here

# Initialize Flask-Migrate
migrate = Migrate(app, db)

def create_database_tables():
    """Create database tables based on the defined models."""
    with app.app_context():
        db.create_all()  # Create all tables in the database
        print("Database tables created.")

# def migrate_database():
#     """Run database migrations."""
#     with app.app_context():
#         # Check if migrations folder exists, if not, initialize it
#         if not os.path.exists('migrations'):
#             print("Initializing migrations folder...")
#             from flask_migrate import init
#             init(app)
#             print("Migrations folder created.")

#         upgrade()  # Apply any pending migrations
#         print("Database migrations applied.")

# def seed_database():
#     """Seed the database with initial data."""
#     with app.app_context():
#         # Example: Adding a user
#         if not User.query.filter_by(username='admin').first():  # Check if user already exists
#             new_user = User(name='admin_1', username='admin', email='admin@example.com', phone='0789657895', password='password')  # Adjust as necessary
#             db.session.add(new_user)
#             db.session.commit()
#             print("Database seeded with initial data.")
#         else:
#             print("Admin user already exists.")

if __name__ == "__main__":
    create_database_tables()  # Create tables
    # migrate_database()         # Run migrations
    #seed_database()            # Seed database
