from flask import Flask, render_template, url_for, redirect
from models import login_manager, db
from routes import bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from models.posts import Post

csrf = CSRFProtect()

app = Flask(__name__)
csrf.init_app(app)
migrate = Migrate(app, db)

# Load configuration
from config import Config
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)



# Import blueprints
from routes.auth import auth_bp as auth_bp
from routes.booking import booking_bp as booking_bp
from routes.payment import payment_bp as payment_bp
from routes.user import user_bp as user_bp
from routes.passenger import passenger_bp as passenger_bp
from routes.posts import posts_bp as posts_bp
from routes.addBus import bus_bp as bus_bp


# Register the blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(booking_bp, url_prefix='/booking')
app.register_blueprint(payment_bp, url_prefix='/payment')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(passenger_bp, url_prefix='/passenger')
app.register_blueprint(posts_bp, url_prefix='/post')
app.register_blueprint(bus_bp, url_prefix='/bus')



@app.route('/', methods=['GET', 'POST'])
def landing():
    return render_template('landing.html')

@app.route('/home')
def home():
    from forms.passengerForm import PassengerForm
    form = PassengerForm()
    posts = Post.query.all()  # Fetch posts from the database
    return render_template('index.html', form=form, posts=posts)

@app.route('/booking', methods=['GET', 'POST'], strict_slashes=False)
def booking():
    from forms.bookingForm import BookingForm
    form = BookingForm()
    return render_template('book.html', form=form)

@app.errorhandler(401)
def unauthorized_error(error):
    return redirect(url_for('auth.login'))



if __name__ == '__main__':
    app.run(debug=True)