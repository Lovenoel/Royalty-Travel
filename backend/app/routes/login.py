from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import current_user, login_user, logout_user, login_required
from app import db, bcrypt
from app.forms.forms import RegistrationForm, LoginForm  # Import your forms
from app.models import User

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
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data,
                        password=hashed_password,
                        email=form.email.data,
                        phone=form.phone.data)
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
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            print("Login unsuccessful. Invalid email or password.")  # Debug statement
            flash('Login Unsuccessful. Please check email and password', 'danger')
    else:
        print("Form validation failed.")  # Debug statement
            
    return render_template('login.html', title='Login', form=form)

@authorize_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('authorize.login')

            








        