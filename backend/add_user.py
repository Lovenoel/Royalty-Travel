# add_user.py

from app import create_app, db  # Adjust imports based on your project structure
from app.models.User import User  # Import your User model

def main():
    app = create_app()
    app.app_context().push()

    # Create a new user
    new_user = User(username='john', email='john@example.com')

    # Add the user to the session
    db.session.add(new_user)

    # Commit the transaction to the database
    db.session.commit()

    print("User added successfully.")

if __name__ == '__main__':
    main()
