from flask_mail import Message
from app import mail
from flask import url_for, current_app


def send_reset_email(user):
    """ A function responsible for sending a password reset email """
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender  = 'noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the link below:
{url_for('authorize.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email 
and no changes will be made.
'''
    mail.send(msg)