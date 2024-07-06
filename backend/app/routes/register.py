from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from app import db
from app.forms.forms import RegistrationForm
from app.models import User

register_bp = Blueprint('register', __name__, url_prefix='/register')

# Registration route
@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect to profile if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('profile.profile'))
    
    form = RegistrationForm()  # Create an instance of RegistrationForm
    if form.validate_on_submit():  # If form is submitted and validated
        # Create a new User instance with form data
        user = User(name=form.username.data, email=form.email.data, phone=form.phone.data)
        user.set_password(form.password.data)  # Set user password
        db.session.add(user)  # Add user to the database session
        db.session.commit()  # Commit changes to the database
        flash('Congratulations, you are welcome to Royalty Travel')  # Flash success message
        return redirect(url_for('login'))  # Redirect to login page after successful registration
    
    # Render registration template with form data
    return render_template('register.html', title='Register', form=form)
