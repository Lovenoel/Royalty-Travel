from flask import Blueprint, render_template
from app.forms.forms import LoginForm

login_bp = Blueprint('/logins', __name__, url_prefix='/login')

@login_bp.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    return render_template('loginform.html', title='Loginform', form=form)