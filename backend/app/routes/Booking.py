from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.forms.bookingForm import BookingForm
from app.models.Booking import UserBooking, PassengerBooking
from app.models.Passenger import Passenger
from app.models.Promotions import Promotion
from flask_login import current_user

bp = Blueprint('booking', __name__, url_prefix='/booking')

@bp.route('/book', methods=['GET', 'POST'])
def book():
    # Handles the booking process
    form = BookingForm()
    if form.validate_on_submit():
        # Handles registered user booking
        if current_user.is_authenticated:
            booking = UserBooking(
                username=form.username.data,
                user_id =current_user.id,
                departure_place=form.departure_place.data,
                destination=form.destination.data,
                date_time=form.date_time.data,
                is_guest = False
            )
        
        # Handles the passenger(Not registered) booking
        else:
            booking = PassengerBooking(
                username=form.username.data,
                passenger_id=Passenger.id,
                departure_place=form.departure_place.data,
                destination=form.destination.data,
                date_time=form.date_time.data,
                is_guest=True
            )
        db.session.add(booking) # Adds a new booking
        db.session.commit()
        flash('Your booking has been successfully made!', 'success')
        return redirect(url_for('booking.book'))
    return render_template('book.html',
                           form=form)


@bp.route('/promotions')
def promotions():
    # Fetch promotions from the database
    promotions = Promotion.query.all()  # Retrieve all promotions from the database

    return render_template('promotions.html',
                           promotions=promotions)
