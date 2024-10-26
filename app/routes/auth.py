from flask import Blueprint, url_for, redirect, flash, render_template, request
from flask_login import current_user, login_user, logout_user, login_required
from forms.auth_forms import RegistrationForm, LoginForm
from models.users import User
from . import bcrypt
from models import db
from typing import Optional, Union


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register() -> Union[str]:
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user: Optional[User] = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            hashed_password: str = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(name=form.name.data,
                        username=form.username.data,
                        email=form.email.data,
                        password=hashed_password,
                        phone=form.phone.data,
                        is_admin=form.is_admin.data)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('That email exists, choose another email', 'danger')
    return render_template('register.html', title='Register', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login() -> Union[str]:
    """ Endpoint for registered user login """
    print('----------login hit-----------')
    if current_user.is_authenticated:
        print('User is authenticated')
        return redirect(url_for('home'))
    
    form = LoginForm()
    print(f"{form.email.data}---------------")

    if form.validate_on_submit():
        user: Optional[User] = User.query.filter_by(email=form.email.data).first()
        if user:
            print(f"User found: {user}")
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                print('Password check passed')
                login_user(user, remember=form.remember.data)
                next_page: Optional[str] = request.args.get('next')
                print(f"Next page: {next_page}")  # Debug statement
                # Only allow redirection to internal URLs to avoid open redirects
                # if next_page and URL(next_page).netloc == '':
                #     return redirect(next_page)
                # return redirect(url_for('user.dashboard'))
                # Ensure the next_page is an internal URL
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                return redirect(url_for('user.dashboard'))

                # return redirect(next_page) if next_page else redirect(url_for('user.dashboard'))
            print("Login unsuccessful. Invalid email or password.")  # Debug statement
            flash('Login Unsuccessful. Please check email and password', 'danger')
        else:
            flash('Login to access this page... Thank you')
    else:
        print("Form validation failed.")  # Debug statement
    
    next_page: Optional[str] = request.args.get('next')
            
    return render_template('login.html',
                           title='Login',
                           form=form,
                           next_page=next_page
                           )

@auth_bp.route('/logout', strict_slashes=False)
@login_required
def logout():
    """ Logs the current user out"""
    logout_user()
    flash("You Have Been Logged Out!  Thanks For Stopping By...")
    return redirect(url_for('home'))