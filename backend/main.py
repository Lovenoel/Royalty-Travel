""" This is my flask app entry file """

from flask import render_template, flash
from flask_login import current_user
from app import create_app
from app.forms.forms import RegistrationForm, LoginForm
from app.utils.notifications import check_and_send_notifications
from flask_apscheduler import APScheduler
from app.forms.bookingForm import BookingForm


app = create_app()

posts = [
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

promotions = [
        {
            'title': 'Special Discount!',
            'description': 'Get 20% off on all bookings this month.'
        },
        {
            'title': 'Summer Sale!',
            'description': 'Book now and enjoy discounted rates on selected routes.'
        }
    ]

scheduler = APScheduler()
scheduler.init_app(app)

@scheduler.task('interval', id='check_notifications', seconds=60)
def scheduled_task():
    with app.app_context():
        check_and_send_notifications()

scheduler.start()

# The index or home route of the app
@app.route('/')
@app.route('/home', methods=['GET'])
def index():
    return render_template('index.html', posts=posts)

# The routes indexing booking
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    form = BookingForm()
    return render_template('book.html', form=form)

@app.route('/booking/<int:booking_id>')
def booking_detail(booking_id):
    # Here you would fetch the booking details from the database
    # For simplicity, let's just pass the booking_id to the template
    return render_template('booking_detail.html', booking_id=booking_id)

@app.route('/promotions')
def promotions():
    return render_template('promotions.html', promotions=promotions)


# the route that calls bus_status
@app.route('/bus_status', methods=['GET', 'POST'])
def bus_status():
    return render_template('bus_status.html')

# the route that calls the notification
@app.route('/notification', methods=['GET', 'POST'])
def notification():
    return render_template('notification.html')

# the route that calls the recipts
@app.route('/receipt')
def receipt():
    return render_template('receipt.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = RegistrationForm()
    return render_template('profile.html', user=current_user, form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', user=current_user, form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('login.html', User=current_user, form=form)

@app.route('/logout')
def logout():
    return render_template('login.html')

@app.route('/change_password')
def change_password():
    return render_template('profile.html')

if __name__ == '__main__':
    # Starts the app when run directly and not import
    print("Starting the Flask development server on http://127.0.0.1:5000/")
    app.run(debug=True)
