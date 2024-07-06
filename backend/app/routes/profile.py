from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
from app import db

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.email = request.form.get('email')
        current_user.phone = request.form.get('phone')
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile.profile'))
    return render_template('profile.html', user=current_user)

# Change password route
@profile_bp.route('/change_password', methods=['GET','POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not current_user.check_password(current_password):
        flash('Current password is incorrect', 'danger')
        return redirect(url_for('profile.profile'))

    if new_password != confirm_password:
        flash('New password and confirmation do not match', 'danger')
        return redirect(url_for('profile.profile'))

    current_user.set_password(new_password)
    db.session.commit()
    flash('Your password has been updated!', 'success')
    return redirect(url_for('profile.profile'))

# Route to handle profile picture upload
@profile_bp.route('/upload_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    # Check if the request contains a file part
    if 'profile_picture' not in request.files:
        return jsonify(success=False, message='No file part')
    
    file = request.files['profile_picture']  # Get the file from the request
    
    # Check if a file was selected
    if file.filename == '':
        return jsonify(success=False, message='No selected file')

    # Check if the file is allowed and save it
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)  # Secure the filename
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))  # Save the file to the upload folder
        return jsonify(success=True, message='File successfully uploaded')
    else:
        return jsonify(success=False, message='File type not allowed')

# Helper function to check if the file type is allowed
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Define allowed extensions
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS