from flask import Blueprint

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
def index():
    return "Welcome to the Royalty Travel App"
