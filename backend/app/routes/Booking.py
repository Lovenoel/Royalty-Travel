from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.forms.bookingForm import BookingForm
from app.models.Booking import Booking
from app.models.Promotions import Promotion

bp = Blueprint('booking', __name__)

@bp.route('/book', methods=['GET', 'POST'])
def book():
    form = BookingForm()
    if form.validate_on_submit():
        booking = Booking(
            passenger_name=form.name.data,
            departure_place=form.departure_place.data,
            destination=form.destination.data,
            date_time=form.date_time.data
        )
        db.session.add(booking)
        db.session.commit()
        flash('Your booking has been successfully made!', 'success')
        return redirect(url_for('booking.book'))
    return render_template('book.html', form=form)


@bp.route('/promotions')
def promotions():
    # Fetch promotions from the database
    promotions = Promotion.query.all()  # Retrieve all promotions from the database

    return render_template('promotions.html', promotions=promotions)
