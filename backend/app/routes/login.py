"""A module that handles registering a new user, login for
a registered user, user account details and password resetting."""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import current_user, login_user, logout_user, login_required, logout_user
from . import db, bcrypt, mail
from ..forms.forms import RegistrationForm, LoginForm
from ..forms.forms import UpdateAccountForm, ResetPasswordForm, RequestResetForm
from ..models import User
from flask_mail import Message
from ..email_utils import send_reset_email

authorize_bp = Blueprint('authorize', __name__, url_prefix='/authorize')


# Registration route
@authorize_bp.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """
    Endpoint for registering a new user to the database
    Returns:
    - A new user and creates an account for that user
    """
    if current_user.is_authenticated:
        return redirect(url_for('profile.profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data,
                        password=hashed_password,
                        email=form.email.data,
                        phone=form.phone.data,
                        is_admin=form.is_admin.data)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created!', 'success')
            return redirect(url_for('authorize.login'))
        else:
            flash('Email already exists. Please use a different email.', 'danger')
    return render_template('register.html', title='Register', form=form)


# Login route
@authorize_bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """
    Endpoint for login used by a registered user
    Returns:
    - A registered user to the home page
    """
    print("----------login hit--------")
    if current_user.is_authenticated:
        print("User is already authenticated.")
        return redirect(url_for('main.home'))
    form = LoginForm()
    print(f"{form.email.data} ------->form data")
            
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print(f"User found: {user}")  # Debug statement
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print("Password check passed")  # Debug statement
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            print(f"Next page: {next_page}")  # Debug statement
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            print("Login unsuccessful. Invalid email or password.")  # Debug statement
            flash('Login Unsuccessful. Please check email and password', 'danger')
    else:
        print("Form validation failed.")  # Debug statement
    
    next_page = request.args.get('next')
            
    return render_template('login.html',
                           title='Login',
                           form=form,
                           next_page=next_page
                           )


@authorize_bp.route('/logout', strict_slashes=False)
@login_required
def logout():
    """ Logs the current user out"""
    logout_user()
    return redirect(url_for('index'))


@authorize_bp.route('/account', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def account():
    """
    Account for a registered user
    Returns:
    Account page with user profile image, email and username
    """
    print(f"Username: {current_user.username}")
    print(f"Email: {current_user.email}")
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('authorize.accont'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = (url_for('static',
                         filename='images/kln.png' 
                         if current_user.profile_picture is None
                         else 'uploads/' + current_user.profile_picture))
    return render_template('account.html',
                           title='Account',
                           form=form,
                           image_file=image_file)


@authorize_bp.route("/reset_request", methods=['GET', 'POST'], strict_slashes=False)
def reset_request():
    """
    Endpoint for requesting password 
    """
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('authorize.login'))
    return render_template('reset_request.html', form=form)


@authorize_bp.route('/reset_password/<token>', methods=['GET', 'POST'], strict_slashes=False)
def reset_token(token):
    """
    Endpoint for retrieving a  password reset token
    """
    user = User.verify_reset_token(token)

    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('authorize.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated, you can now log in', 'success')
        return redirect(url_for('authorize.login'))
    return render_template('reset_token.html', form=form)