from flask import render_template, Blueprint, redirect, url_for
from app import db
from app.forms.bookingForm import BookingForm
from app.models.Booking import Booking

booking_details_bp = Blueprint('booking_details', __name__, url_prefix='/booking_details')

@booking_details_bp.route('/booking/<int:booking_id>')
def booking_details(booking_id):
    # Fetch booking details from the database using booking_id
    booking= Booking.query.get_or_404(booking_id)
    form = BookingForm(obj=booking) # Populate form with existing booking data if editing

    if form.validate_on_submit():
        # Update booking object with form data
        form.populate_obj(booking)

        db.session.commit()
        return redirect(url_for('booking_details.booking_details', booking_id=booking.id))
    return render_template('booking_details.html', booking=booking, form=form)