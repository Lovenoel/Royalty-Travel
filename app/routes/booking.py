from flask import Blueprint, render_template, flash, redirect, url_for
from models import db
from models.booking import UserBooking, PassengerBooking
from forms.bookingForm import BookingForm
from models.passenger import Passenger
from flask_login import current_user
from models.users import User
from typing import Union

booking_bp = Blueprint('booking', __name__, url_prefix='/booking')

@booking_bp.route('/book', methods=['GET', 'POST'])
def book() -> Union[str]:
    """ A route that handles a booking. """

    form = BookingForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            booking = UserBooking(
                username = form.username.data,
                user_id = current_user.id,
                departure_place = form.departure_place.data,
                destination = form.departure.data,
                date_time = form.date_time.data,
                is_guest = False
            )

            # Handles the passenger(Not registered user)
        else:
            booking = PassengerBooking(
                username = form.username.data,
                passenger_id = Passenger.id,
                departure_place = form.departure_place.data,
                destination = form.destination.data,
                departure_date_time = form.departure_date_time.data,
                is_guest = True
            )

        db.session.add(booking)
        db.session.commit()
        flash('Your booking has been succeessfully made', 'success')
        return redirect(url_for('payment.pay'))
    return render_template('book.html', form=form)