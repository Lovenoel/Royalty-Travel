from flask import Blueprint, jsonify, flash, redirect, render_template, url_for
from datetime import datetime, timezone
from typing import Union
from forms.bus import BusForm, TransportStatusForm
from models.bus import Bus, Taxi
from models import db


bus_bp = Blueprint('bus', __name__, url_prefix='/bus')

@bus_bp.route('/add_bus', methods=['GET', 'POST'])
def add_bus() -> Union[str]:
    """
    Endpoint for adding a new bus
    Returns
    -A new bus is created and saved to the database
    """
    form = BusForm()
    if form.validate_on_submit():
        if form.validate_on_submit():
            print('Form validated successfully')
        else:
            print('Form validation failed:', form.errors)


        # Check if the bus already exists
        existing_bus = Bus.query.filter_by(number_plate=form.number_plate.data).first()
        if existing_bus:
            print('Bus exists.')
            flash('Bus with this number plate already exists.', 'danger')
            return redirect(url_for('bus.add_bus'))

        new_bus = Bus(
            number_plate=form.number_plate.data,
            capacity=form.capacity.data,
            # updated_at=datetime.now(timezone.utc)
            location = form.location.data,
            model = form.model.data
            )
        print('The bus has been added')
        print(form.errors)
        db.session.add(new_bus)
        db.session.commit()
        flash('Bus added successfully.', 'success')
        return redirect(url_for('bus.view_buses')) 
    return render_template('add_Bus.html', form=form)

@bus_bp.route('/transport_status', methods=['GET', 'POST'])
def transport_status():
    form = TransportStatusForm()
    results = None
    if form.validate_on_submit():
        # Extract data from the form
        location = form.location.data
        destination = form.destination.data
        transport_mode = form.transport_mode.data

        # Fetch transport status data based on the inputs (stubbed here for example)
        # In reality, this would query a database or external API
        results = fetch_transport_status(location, destination, transport_mode)

    return render_template('transport_status.html', form=form, results=results)

def fetch_transport_status(location, destination, transport_mode):
    """Fetches the transport status of bus, taxis or other means"""
    if transport_mode == 'bus':
        return Bus.query.filter_by(location=location,destination=destination).all()
    elif transport_mode == 'taxi':
        return Taxi.query.filter_by(location=location, destination=destination)
    else:
        return []  # Or handle other modes
    # return [
    #     {"name": "Bus 101", "status": "On Time", "availability": "5 seats"},
    #     {"name": "Taxi Service", "status": "Available", "availability": "4 seats"},
    #     {"name": "Bus 202", "status": "Delayed", "availability": "2 seats"},
    # ]


@bus_bp.route('/view_buses', methods=['GET'])
def view_buses():
    # Query all bus records
    buses = Bus.query.all()
    return render_template('view_buses.html', buses=buses)