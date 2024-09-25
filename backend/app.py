""" This is my flask app entry file """
from flask import render_template, g, jsonify
from flask_login import current_user, login_required
from app import create_app
from app.forms.forms import RegistrationForm, LoginForm
from app.utils.notifications import check_and_send_notifications
from flask_apscheduler import APScheduler
from app.forms.bookingForm import BookingForm
from app.forms.passengerForm import PassengerForm
from app.forms.BusStatusForm import BusStatusForm
from app.forms.posts import PostForm
from app.models.Post import Post
from flask_wtf.csrf import generate_csrf
import json

# Flask application instance
app = create_app()

"""posts = [
    {
        "name": "John Peter",
        "email": "peterjohn12@gmail.com",
        "phone": "0787625864",
    },

    {
        "name": "Mary Jane",
        "email": "janeMary@gmail.com",
        "phone": "0707836901"
    }
]
"""

promotions = [
        {
            'title': 'Special Discount!',
            'description': 'Get 20"%" off on all bookings this month.'
        },
        {
            'title': 'Summer Sale!',
            'description': 'Book now and enjoy discounted rates on selected routes.'
        }
    ]

scheduler = APScheduler()
scheduler.init_app(app)

@scheduler.task('interval', id='check_notifications', seconds=3600)
def scheduled_task():
    with app.app_context():
        check_and_send_notifications()

scheduler.start()

# Adds headers to every request 
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=3600'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

# Closing all the resources used by the request
@app.teardown_request
def teardown_request(exception):
    if exception:
        print(f"Exception occurred: {exception}")
    # Close any database connections if needed (for example)
    if hasattr(g, 'db'):
        print("Closing the database connection")
        g.db.close()

# Generates the csrf token
@app.route('/api/csrf-token', methods=['GET'])
def get_csrf_token():
    token = generate_csrf()
    return jsonify({'csrf_token': token})


@app.route('/')
def landing():
    return render_template('landing.html')

# The index or home route of the app
#@app.route('/')
@app.route('/home', methods=['GET'])
def index():
    form = PassengerForm()
    post = Post.query.all()
    is_admin = json.dumps(current_user.is_admin) if current_user.is_authenticated else 'false'
    return render_template('index.html', posts=post, form=form, is_admin=is_admin)
@app.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm
    posts = Post.query.all()
    return render_template('index.html', posts=posts, form=form)

@app.route('/react')
def react_index():
    return render_template('react_index.html')


@app.route('/account')
@login_required
def account():
    form = PassengerForm()
    return render_template('account.html', title='Account', form=form)

# The routes indexing booking
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    form = BookingForm()
    return render_template('book.html', form=form)

@app.route('/booking/user_booking_details/<int:booking_id>')
def user_booking_details(booking_id):
    # Here you would fetch the booking details from the database
    # For simplicity, let's just pass the booking_id to the template
    return render_template('user_booking_details.html', booking_id=booking_id)

@app.route('/booking/passenger_booking_details/<int:booking_id>')
def passenger_booking_details(booking_id):
    # Here you would fetch the booking details from the database
    # For simplicity, let's just pass the booking_id to the template
    return render_template('passenger_booking_details.html', booking_id=booking_id)


@app.route('/promotions')
def promotions():
    return render_template('promotions.html', promotions=promotions)


# the route that calls bus_status
@app.route('/bus_status', methods=['GET', 'POST'])
def bus_status():
    return render_template('bus_status.html')

@app.route('/add_bus', methods=['GET', 'POST'])
def add_bus():
    form = BusStatusForm()
    return render_template('addBus.html', form=form)

@app.route('/bus_status/success')
def success():
    """
    Route to display a success message or details of the added bus.
    """
    # You can pass any relevant data to the template if needed
    return render_template('success.html')

# the route that calls the notification
@app.route('/notification', methods=['GET', 'POST'])
def notification():
    return render_template('notification.html')

# the route that calls the recipts
@app.route('/receipt')
def receipt():
    return render_template('receipt.html')

# Route for the profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = RegistrationForm()
    return render_template('profile.html', user=current_user, form=form)

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', user=current_user, form=form)

# Login route
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('login.html', User=current_user, form=form)

# Password change route
@app.route('/change_password')
def change_password():
    return render_template('profile.html')

@app.route('/user/users')
def get_users():
    return render_template('get_users.html')