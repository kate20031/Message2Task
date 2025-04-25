import json
from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from twilio.rest import Client
from ai_task_extractor import extract_task_from_message
# from models import Message
# from __init__ import create_app, db  # Correct import

# app = create_app()
# @app.before_first_request
# def create_tables():
#     db.create_all()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Gala11maga11!'
db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# db.init_app(app)
#
users_db = {}
# db.init_app(app)

# Create the tables (this should only be done once, preferably on app startup)
# @app.before_first_request
# def create_tables():
#     db.create_all()
# import models

# Twilio credentials
TWILIO_ACCOUNT_SID = 'AC658536469a94b2b487211163ae13182d'
TWILIO_AUTH_TOKEN = '0568e48d26312f6f5d90131880f3e593'
TWILIO_PHONE_NUMBER = '+380933200762'


# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
# db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(100), unique=True, nullable=False)  # Twilio SID
    from_user = db.Column(db.String(100), nullable=False)
    ai_task = db.Column(db.JSON, nullable=True)
    date = db.Column(db.String(100), nullable=False)
    processed = db.Column(db.Boolean, default=False)  # Track processing status

    def __repr__(self):
        return f"<Message {self.from_user}>"


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

        # Check if tasks are already generated
        if 'tasks' not in session:
            # If tasks not in session, generate tasks using AI
            session['tasks'] = generate_ai_tasks()

        return render_template('dashboard.html', username=session['user'], messages=message_list, tasks=session['tasks'])
    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.pop('user', None)
    session.pop('tasks', None)  # Clear tasks when logging out
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route("/", methods=['GET'])
def home():
    return render_template('home.html')

def generate_ai_tasks():
    # Example function to simulate AI task generation
    # This could be a function that interacts with the Gemini API
    tasks = [
        {"task": "Explain the concept of the sun", "status": "pending"},
        {"task": "Describe the sun's impact on Earth's climate", "status": "pending"}
    ]
    return tasks
#
@app.route("/get_messages", methods=['GET'])
def get_messages():
    if 'user' in session:
        try:
            messages = client.messages.list(limit=5)  # Get last 5 messages

            processed_messages = []
            for msg in messages:
                ai_result = extract_task_from_message(msg.body)  # Process message with AI

                print(f"Raw AI result: {ai_result}")  # Log the raw AI result

                if ai_result:
                    try:
                        # If the AI result is a dictionary, directly use it
                        if isinstance(ai_result, dict):
                            ai_task = ai_result
                            processed_messages.append({
                                'id': msg.sid,
                                'from': msg.from_,
                                'ai_task': ai_task,
                                'date': msg.date_sent.strftime('%Y-%m-%d %H:%M:%S')
                            })

                            # Save the message to the database
                            message = Message(
                                from_user=msg.from_,
                                ai_task=ai_task,  # Store AI task as JSON
                                date=msg.date_sent.strftime('%Y-%m-%d %H:%M:%S')
                            )
                            db.session.add(message)
                            db.session.commit()

                            # Flash a success message
                            flash(f"Message from {msg.from_} saved successfully!", 'success')

                        else:
                            print("Unexpected structure in AI result.")
                    except Exception as e:
                        print(f"Unexpected error during AI task extraction: {e}")
                        # Flash an error message
                        flash(f"Error processing message: {e}", 'danger')

            print(f"Processed messages: {processed_messages}")  # Log the processed messages
            return {"messages": processed_messages}, 200

        except Exception as e:
            print(f"Error: {str(e)}")  # Log any other errors
            # Flash an error message if there was an issue fetching messages
            flash(f"Error fetching messages from Twilio: {str(e)}", 'danger')
            return {"error": str(e)}, 500
    else:
        return {"error": "Unauthorized"}, 401

# @app.route("/get_messages", methods=['GET'])
# def get_messages():
#     if 'user' in session:
#         try:
#             # Fetch last 5 messages from Twilio
#             messages = client.messages.list(limit=5)
#             unprocessed_messages = []
#
#             for msg in messages:
#                 # Check if the message has already been processed by looking for its SID in the database
#                 existing_message = Message.query.filter_by(sid=msg.sid).first()
#
#                 if not existing_message or not existing_message.processed:
#                     # Process the message with AI if it's unprocessed
#                     ai_result = extract_task_from_message(msg.body)
#                     print(f"Raw AI result: {ai_result}")
#
#                     if ai_result:
#                         try:
#                             if isinstance(ai_result, dict):
#                                 ai_task = ai_result
#                                 unprocessed_messages.append({
#                                     'id': msg.sid,
#                                     'from': msg.from_,
#                                     'ai_task': ai_task,
#                                     'date': msg.date_sent.strftime('%Y-%m-%d %H:%M:%S')
#                                 })
#
#                                 # Save the message to the database and mark it as processed
#                                 if not existing_message:
#                                     existing_message = Message(
#                                         sid=msg.sid,  # Use SID as unique identifier
#                                         from_user=msg.from_,
#                                         ai_task=ai_task,
#                                         date=msg.date_sent.strftime('%Y-%m-%d %H:%M:%S'),
#                                         processed=True  # Mark as processed
#                                     )
#                                     db.session.add(existing_message)
#                                 else:
#                                     existing_message.processed = True
#                                 db.session.commit()
#
#                                 flash(f"Message from {msg.from_} saved successfully!", 'success')
#                             else:
#                                 print("Unexpected structure in AI result.")
#                         except Exception as e:
#                             print(f"Unexpected error during AI task extraction: {e}")
#                             flash(f"Error processing message: {e}", 'danger')
#
#             print(f"Processed messages: {unprocessed_messages}")  # Log the processed messages
#             return {"messages": unprocessed_messages}, 200
#
#         except Exception as e:
#             print(f"Error: {str(e)}")
#             flash(f"Error fetching messages from Twilio: {str(e)}", 'danger')
#             return {"error": str(e)}, 500
#     else:
#         return {"error": "Unauthorized"}, 401

# Configure the database URI (example with SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database

# # Define the Message model
# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     from_user = db.Column(db.String(100), nullable=False)
#     ai_task = db.Column(db.JSON, nullable=True)
#     date = db.Column(db.String(100), nullable=False)

# def __repr__(self):
#     return f"<Message {self.from_user}>"

@app.route("/webhook", methods=['POST'])
def webhook():
    # Print headers for debugging
    print(f"Headers: {request.headers}")

    if request.content_type == 'application/json':
        data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form.to_dict()
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
