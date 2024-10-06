from flask import Flask, render_template
from models import login_manager
from routes import bcrypt


# Initialize the Flask application
"""def create_app():
    app = Flask(__name__)
    return app
"""
app = Flask(__name__)

# Load configuration
from config import Config
app.config.from_object(Config)

#db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)



# Import blueprints
from routes.auth import auth_bp as auth_bp

# Register the blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)