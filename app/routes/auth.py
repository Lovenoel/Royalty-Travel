from flask import Blueprint, url_for, redirect, flash, render_template, request
from flask_login import current_user, login_user
from forms.auth_forms import RegistrationForm, LoginForm
from models.users import User
from . import bcrypt
from models import db


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data,
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

@auth_bp.route('/login')
def login():
    print('----------login hit-----------')
    if current_user.is_authenticated:
        print('User is authenticated')
        return redirect(url_for('home'))
    
    form = LoginForm
    print(f"{form.email.data}---------------")

    if form.validate_on_submit:
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print(f"User found: {user}")
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                print('Password check passed')
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
            print(f"Next page: {next_page}")  # Debug statement
            return redirect(next_page) if next_page else redirect(url_for('home'))
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
