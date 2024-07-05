# auto_migrate.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Adjust as per your database URI
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-Migrate
migrate.init_app(app, db)

# Upgrade database schema
def upgrade_database():
    with app.app_context():
        migrate.upgrade()

if __name__ == '__main__':
    upgrade_database()
