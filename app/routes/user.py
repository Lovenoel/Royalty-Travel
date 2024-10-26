from flask import Blueprint, redirect, render_template, flash, url_for, request
from forms.auth_forms import UpdateForm
from models import db
from models.users import User
from flask_login import current_user

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/dashboard')
def dashboard():
    """ Handles all to do with the user dashboard"""
    form = UpdateForm()
    if form.validate_on_submit:
        id = current_user.id
        update_user = User.query.get_or_404(id)
        if update_user is None:
            update_user.username = form.username.data
            update_user.email = form.email.data
            update_user.phone = form.phone.data
            update_user.favorite_color = form.favorite_color.data
            # update_user.profile_picture = form.profile_picture
            update_user.about_author = form.about_author.data

            db.session.commit()
            flash('Your account has been updated', 'success')
            return render_template('dashboard.html',
                                title='Dashboard',
                                form=form)
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html',
                           title='Account',
                           form=form,
                           )