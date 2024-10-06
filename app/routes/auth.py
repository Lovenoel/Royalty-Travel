from flask import Blueprint, url_for, redirect, flash, render_template
from flask_login import current_user
from forms.auth_forms import RegistrationForm
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
            db.commit()
            flash('Your account has been created', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('That email exists, choose another email', 'danger')
    return render_template('register.html', title='Register', form=form)

@auth_bp.route('/login')
def login():
    return 'You are now logged in.'