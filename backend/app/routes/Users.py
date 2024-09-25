from flask import Blueprint, jsonify
from flask_login import current_user, login_required
from ..models import User

users_bp = Blueprint('users', __name__, url_prefix='/user')

# The get_user route 
@users_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    # Queries the database to get the current users
    # Then posts users as a list
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    else:
        users = User.query.all()
        user_list = []
        for user in users:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone': user.phone
            }
            user_list.append(user_data)
        return jsonify(user_list)
