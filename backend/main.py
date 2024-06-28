from flask import render_template
from flask_login import current_user
from app import create_app

app = create_app()

# The index or home route of the app
@app.route('/')
def index():
    return render_template('index.html')

# The routes indexing booking
@app.route('/booking')
def booking():
    return render_template('booking.html')

# the route that calls bus_status
@app.route('/bus_status')
def bus_status():
    return render_template('bus_status.html')

# the route that calls the notification
@app.route('/notification')
def notification():
    return render_template('notification.html')

# the route that calls the recipts
@app.route('/receipt')
def receipt():
    return render_template('receipt.html')

@app.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('login.html')

@app.route('/change_password')
def change_password():
    return render_template('profile.html')

if __name__ == '__main__':
    # Starts the app when run directly and not import
    print("Starting the Flask development server on http://127.0.0.1:5000/")
    app.run(debug=True)
