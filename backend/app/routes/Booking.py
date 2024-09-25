"""A module that handles all the booking processes for both a
registered user and a guest passenger."""

from flask import Blueprint, render_template, redirect, url_for, flash
from . import db
from ..forms.bookingForm import BookingForm
from ..models.Booking import UserBooking, PassengerBooking
from ..models.Passenger import Passenger
from ..models.Promotions import Promotion
from flask_login import current_user

bp = Blueprint('booking', __name__, url_prefix='/booking')


@bp.route('/book', methods=['GET', 'POST'], strict_slashes=False)
def book():
    """Handles the booking process"""
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

@bp.route('/user_booking_details/<int:booking_id>', methods=['GET', 'POST'], strict_slashes=False)
def user_booking_details(booking_id):
    """Fetch user booking details from the database"""
    booking = UserBooking.query.get_or_404(booking_id)
    
    if booking:
        form = BookingForm(obj=booking)
        if form.validate_on_submit():
            form.populate_obj(booking)
            db.session.commit()
            flash('Booking updated successfully!', 'success')
            return redirect(url_for('booking.user_booking_details',
                                    booking_id=booking_id))
        return render_template('user_booking_details.html',
                               booking=booking, form=form)
    
@bp.route('/passenger_booking_details/<int:booking_id>', methods=['GET', 'POST'], strict_slashes=False)
def passenger_booking_details(booking_id):
    """Fetch passenger booking details from the database"""
    booking = PassengerBooking.query.get_or_404(booking_id)
    form = BookingForm(obj=booking)
    
    if form.validate_on_submit():
        form.populate_obj(booking)
        db.session.commit()
        flash('Booking updated successfully!', 'success')
        return redirect(url_for('booking.passenger_booking_details',
                                booking_id=booking_id))
    
    return render_template('passenger_booking_details.html',
                           booking=booking, form=form)

@bp.route('/promotions', strict_slashes=False)
def promotions():
    """Fetch promotions from the database"""
    promotions = Promotion.query.all()  # Retrieve all promotions from the database

    return render_template('promotions.html',
                           promotions=promotions)
