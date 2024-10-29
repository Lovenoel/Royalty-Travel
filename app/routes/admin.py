from flask import Blueprint, Response


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin() -> Response:
    """Handles the admin operations"""
    