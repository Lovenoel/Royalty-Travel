from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.forms.forms import RegistrationForm, LoginForm  # Import your forms
from app.models import User
from sqlalchemy.exc import IntegrityError

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')
authorize_bp = Blueprint('authorize', __name__, url_prefix='/authorize')

# Registration route
@authorize_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile.profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(username=form.username.data, email=form.email.data, phone=form.phone.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created!', 'success')
            return redirect(url_for('authorize.login'))
        else:
            flash('Email already exists. Please use a different email.', 'danger')
    return render_template('register.html', title='Register', form=form)

# Login route
@authorize_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# Logout route
@authorize_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authorize.login'))

