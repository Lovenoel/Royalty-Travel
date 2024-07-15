from flask import Blueprint, render_template
from app import db
from flask_login import login_required

account_bp = Blueprint('/account', __name__, url_prefix='/account')

@account_bp.route('/')
def account():
    return render_template('account.html')