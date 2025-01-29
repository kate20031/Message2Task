from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users_db = {}

# Twilio credentials
TWILIO_ACCOUNT_SID = 'US92b48ceee09bfb40b079286503061dc3'
TWILIO_AUTH_TOKEN = '0568e48d26312f6f5d90131880f3e593'
TWILIO_PHONE_NUMBER = '+380933200762'

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users_db:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            users_db[username] = generate_password_hash(password)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users_db:
            if check_password_hash(users_db[username], password):
                session['user'] = username  # Store the username in the session
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid password. Please try again.', 'danger')
        else:
            flash('Username not found. Please try again.', 'danger')

    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    if 'user' in session:
        # Fetch messages from Twilio
        try:
            messages = client.messages.list(limit=5)  # Get the latest 5 messages
            message_list = [{'from': msg.from_, 'body': msg.body, 'date': msg.date_sent} for msg in messages]
        except Exception as e:
            message_list = []
            flash(f'Failed to fetch messages from Twilio: {str(e)}', 'danger')

        return render_template('dashboard.html', username=session['user'], messages=message_list)
    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route("/", methods=['GET'])
def home():
    return render_template('home.html')


@app.route("/webhook", methods=['POST'])
def webhook():
    # Print headers for debugging
    print(f"Headers: {request.headers}")

    # Check content type and parse accordingly
    if request.content_type == 'application/json':
        data = request.json  # JSON data
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form.to_dict()  # Parse form data
    else:
        return "Unsupported Media Type", 415

    # Debugging output
    print(f"Received webhook data: {data}")

    if data:
        return "Webhook received", 200
    else:
        return "No data received", 400

if __name__ == "__main__":
    app.run(debug=True)
