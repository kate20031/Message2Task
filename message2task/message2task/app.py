import json
import os
from sqlite3 import IntegrityError

from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from twilio.rest import Client
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import render_template
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://messageuser:1234@localhost/message2taskdb'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     sid = db.Column(db.String(64), unique=True, nullable=False)
#     from_user = db.Column(db.String(100), nullable=False)
#     ai_task = db.Column(db.JSON, nullable=True)
#     date = db.Column(db.String(100), nullable=False)
#     processed = db.Column(db.Boolean, default=False)
#     confirmed = db.Column(db.Boolean, default=False)
#
#     def __repr__(self):
#         return f"<Message {self.from_user}>"

# === Модель Message оновлена ===
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(64), unique=True, nullable=False)
    from_user = db.Column(db.String(100), nullable=False)
    ai_task = db.Column(db.JSON, nullable=True)
    date = db.Column(db.String(100), nullable=False)
    processed = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"<Message from={self.from_user}, sid={self.sid}>"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    twilio_sid = db.Column(db.String(100), nullable=True)
    twilio_token = db.Column(db.String(100), nullable=True)
    twilio_number = db.Column(db.String(20), nullable=True)


    messages = db.relationship('Message', backref='user', lazy=True)


@app.before_request
def before_first_request_func():
    if not hasattr(app, 'has_run'):
        # Initialization code here
        app.has_run = True



# users_db = {}




# Initialize Twilio client
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
# db = SQLAlchemy(app)




# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#
#         if User.query.filter_by(username=username).first():
#             flash('Username already exists. Please choose a different one.', 'danger')
#         else:
#             hashed_pw = generate_password_hash(password)
#             new_user = User(username=username, password_hash=hashed_pw)
#             db.session.add(new_user)
#             db.session.commit()
#             flash('Registration successful! Please log in.', 'success')
#             return redirect(url_for('login'))
#
#     return render_template('register.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Нові поля
        twilio_sid = request.form.get('twilio_sid')
        twilio_token = request.form.get('twilio_token')
        twilio_number = request.form.get('twilio_number')

        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            hashed_pw = generate_password_hash(password)
            new_user = User(
                username=username,
                password_hash=hashed_pw,
                twilio_sid=twilio_sid,
                twilio_token=twilio_token,
                twilio_number=twilio_number
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')



# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#
#         if username in users_db:
#             if check_password_hash(users_db[username], password):
#                 session['user'] = username  # Store the username in the session
#                 flash('Login successful!', 'success')
#                 return redirect(url_for('dashboard'))
#             else:
#                 flash('Invalid password. Please try again.', 'danger')
#         else:
#             flash('Username not found. Please try again.', 'danger')
#
#     return render_template('login.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user'] = user.username
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('login.html')


# @app.route("/dashboard")
# def dashboard():
#     if 'user' not in session:
#         flash('You need to log in first.', 'warning')
#         return redirect(url_for('login'))
#
#     # Виводимо тільки збережені повідомлення
#     messages = Message.query.order_by(Message.date.desc()).limit(10).all()
#
#     message_list = [{
#         'from': msg.from_user,
#         'ai_task': msg.ai_task,
#         'date': msg.date
#     } for msg in messages]
#
#     if 'tasks' not in session:
#         session['tasks'] = generate_ai_tasks()
#
#     return render_template('dashboard.html', username=session['user'], messages=message_list, tasks=session['tasks'])
#

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

    messages = Message.query.filter_by(user_id=session['user_id']).order_by(Message.date.desc()).limit(10).all()

    message_list = [{
        'from': msg.from_user,
        'ai_task': msg.ai_task,
        'date': msg.date
    } for msg in messages]

    return render_template('dashboard.html', username=session['user'], messages=message_list)


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
# @app.route("/get_messages", methods=['GET'])
# def get_messages():
#     if 'user' in session:
#         try:
#             messages = client.messages.list(limit=10)
#
#             processed_messages = []
#             for msg in messages:
#                 from strategy_gemini import GeminiExtractionStrategy
#                 from extractor_context import TaskExtractorContext
#
#                 context = TaskExtractorContext(GeminiExtractionStrategy())
#                 ai_result = context.extract_task(msg.body)
#
#                 # ai_result = extract_task_from_message(msg.body)  # Process message with AI
#
#                 print(f"Raw AI result: {ai_result}")  # Log the raw AI result
#
#                 if ai_result:
#                     try:
#                         # If the AI result is a dictionary, directly use it
#                         if isinstance(ai_result, dict):
#                             ai_task = ai_result
#                             processed_messages.append({
#                                 'id': msg.sid,
#                                 'from': msg.from_,
#                                 'ai_task': ai_task,
#                                 'date': msg.date_sent.strftime('%Y-%m-%d %H:%M:%S')
#                             })
#                             existing = Message.query.filter_by(sid=msg.sid).first()
#                             if existing:
#                                 print(f"Message with sid={msg.sid} already exists, skipping insert.")
#                                 continue  # пропускаємо вставку
#
#                             try:
#                                 # Save the message to the database
#                                 message = Message(
#                                     sid=msg.sid,
#                                     from_user=msg.from_,
#                                     ai_task=ai_task,  # Store AI task as JSON
#                                     date=msg.date_sent.strftime('%Y-%m-%d %H:%M:%S')
#                                 )
#
#                                 db.session.add(message)
#                                 db.session.commit()
#
#                                 # Flash a success message
#                                 flash(f"Message from {msg.from_} saved successfully!", 'success')
#
#                             except IntegrityError as e:
#                                 db.session.rollback()
#                                 print(f"Error saving message: {e}")
#                                 flash("Error saving message to DB.", 'danger')
#
#                         else:
#                             print("Unexpected structure in AI result.")
#                     except Exception as e:
#                         print(f"Unexpected error during AI task extraction: {e}")
#                         # Flash an error message
#                         flash(f"Error processing message: {e}", 'danger')
#
#             print(f"Processed messages: {processed_messages}")  # Log the processed messages
#             return {"messages": processed_messages}, 200
#
#         except Exception as e:
#             print(f"Error: {str(e)}")  # Log any other errors
#             # Flash an error message if there was an issue fetching messages
#             flash(f"Error fetching messages from Twilio: {str(e)}", 'danger')
#             return {"error": str(e)}, 500
#     else:
#         return {"error": "Unauthorized"}, 401
# @app.route("/get_messages", methods=['GET'])
# def get_messages():
#     if 'user_id' not in session:
#         return jsonify({"error": "Unauthorized"}), 401
#
#     try:
#         user_id = session['user_id']
#         messages = client.messages.list(limit=10)
#         processed_messages = []
#
#         from strategy_gemini import GeminiExtractionStrategy
#         from extractor_context import TaskExtractorContext
#
#         context = TaskExtractorContext(GeminiExtractionStrategy())
#
#         for msg in messages:
#             existing = Message.query.filter_by(sid=msg.sid).first()
#             if existing:
#                 print(f"Message with sid={msg.sid} already exists, skipping insert.")
#                 continue
#
#             ai_result = context.extract_task(msg.body)
#
#             if isinstance(ai_result, dict):
#                 # Нормалізація часу
#                 if 'Time' in ai_result:
#                     normalized = normalize_time(ai_result['Time'])
#                     ai_result['Time'] = normalized if normalized else None
#
#                 try:
#                     message = Message(
#                         sid=msg.sid,
#                         from_user=msg.from_,
#                         ai_task=ai_result,
#                         date=msg.date_sent.strftime('%Y-%m-%d %H:%M:%S'),
#                         processed=True,
#                         user_id=user_id
#                     )
#                     db.session.add(message)
#                     db.session.commit()
#                     print(f"Saved new message sid={msg.sid} for user_id={user_id}")
#                 except IntegrityError as e:
#                     db.session.rollback()
#                     print(f"Error saving message: {e}")
#                     continue
#             else:
#                 print(f"Invalid AI result for sid={msg.sid}, skipping")
#
#         # Після обробки — повертаємо всі повідомлення з бази тільки для цього користувача
#         user_messages = Message.query.filter_by(user_id=user_id).order_by(Message.date.desc()).limit(10).all()
#
#         for msg in user_messages:
#             processed_messages.append({
#                 'sid': msg.sid,
#                 'from': msg.from_user,
#                 'ai_task': msg.ai_task,
#                 'date': msg.date
#             })
#
#         return jsonify({"messages": processed_messages}), 200
#
#     except Exception as e:
#         print(f"General error in get_messages: {e}")
#         return jsonify({"error": str(e)}), 500


#
#
#     # @app.route("/get_messages", methods=['GET'])
# # def get_messages():
# #     if 'user' not in session:
# #         return jsonify({"error": "Unauthorized"}), 401
# #
# #     try:
# #         messages = client.messages.list(limit=10)
# #         processed_messages = []
# #
# #         for msg in messages:
# #             ai_task = get_or_create_ai_task(msg)
# #             if ai_task is None:
# #                 continue
# #
# #             processed_messages.append({
# #                 'sid': msg.sid,
# #                 'from': msg.from_,
# #                 'ai_task': ai_task,
# #                 'date': msg.date_sent.strftime('%Y-%m-%d %H:%M:%S')
# #             })
# #
# #         return jsonify({"messages": processed_messages}), 200
# #
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500
#
# @app.route("/get_messages", methods=['GET'])
# def get_messages():
#     if 'user_id' not in session:
#         return jsonify({"error": "Unauthorized"}), 401
#
#     user_id = session['user_id']
#
#     try:
#         messages = Message.query.filter_by(user_id=user_id).order_by(Message.date.desc()).limit(10).all()
#
#         processed_messages = []
#         for msg in messages:
#             processed_messages.append({
#                 'sid': msg.sid,
#                 'from': msg.from_user,
#                 'ai_task': msg.ai_task,
#                 'date': msg.date
#             })
#
#         return jsonify({"messages": processed_messages}), 200
#
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#

@app.route("/get_messages", methods=['GET'])
def get_messages():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.get(session['user_id'])
    if not user or not user.twilio_sid or not user.twilio_token:
        return jsonify({"error": "Twilio credentials not configured"}), 400

    try:
        client = Client(user.twilio_sid, user.twilio_token)
        messages = client.messages.list(limit=10)

        processed_messages = []
        from strategy_gemini import GeminiExtractionStrategy
        from extractor_context import TaskExtractorContext

        context = TaskExtractorContext(GeminiExtractionStrategy())

        for msg in messages:
            if Message.query.filter_by(sid=msg.sid).first():
                continue

            ai_result = context.extract_task(msg.body)

            if isinstance(ai_result, dict):
                if 'Time' in ai_result:
                    ai_result['Time'] = normalize_time(ai_result['Time'])

                message = Message(
                    sid=msg.sid,
                    from_user=msg.from_,
                    ai_task=ai_result,
                    date=msg.date_sent.strftime('%Y-%m-%d %H:%M:%S'),
                    processed=True,
                    user_id=user.id
                )
                db.session.add(message)
                db.session.commit()

        # Отримуємо повідомлення з БД для конкретного користувача
        user_messages = Message.query.filter_by(user_id=user.id).order_by(Message.date.desc()).limit(10).all()
        return jsonify({
            "messages": [{
                'sid': m.sid,
                'from': m.from_user,
                'ai_task': m.ai_task,
                'date': m.date
            } for m in user_messages]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



def get_or_create_ai_task(msg):
    existing = Message.query.filter_by(sid=msg.sid).first()
    if existing:
        print(f"Using cached AI task for sid={msg.sid}")
        return existing.ai_task

    from strategy_gemini import GeminiExtractionStrategy
    from extractor_context import TaskExtractorContext

    context = TaskExtractorContext(GeminiExtractionStrategy())
    ai_result = context.extract_task(msg.body)

    if not isinstance(ai_result, dict):
        print(f"AI result for sid={msg.sid} не є словником")
        return None

    if 'Time' in ai_result:
        normalized = normalize_time(ai_result['Time'])
        if normalized:
            ai_result['Time'] = normalized
        else:
            print(f"[WARN] Некоректний час: {ai_result['Time']}, замінено на None")
            ai_result['Time'] = None

    try:
        user_id = session.get('user_id')
        if not user_id:
            print("User ID not found in session. Skipping saving message.")
            return None

        message = Message(
            sid=msg.sid,
            from_user=msg.from_,
            ai_task=ai_result,
            date=msg.date_sent.strftime('%Y-%m-%d %H:%M:%S'),
            processed=True,
            user_id=user_id
        )
        db.session.add(message)
        db.session.commit()
        print(f"Stored new AI task for sid={msg.sid}")
        return ai_result
    except IntegrityError:
        db.session.rollback()
        print(f"Integrity error при збереженні sid={msg.sid}")
        return None




def delete_from_db(message_sid):
    message = Message.query.filter_by(sid=message_sid).first()
    if message:
        try:
            db.session.delete(message)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting message: {e}")
            return False
    return False

@app.route('/delete_message/<messageSid>', methods=['DELETE'])
def delete_message(messageSid):
    print(f"Received DELETE request for messageSid={messageSid}")
    success = delete_from_db(messageSid)
    if success:
        print(f"Message {messageSid} deleted successfully")
        return jsonify({'status': 'deleted'}), 200
    else:
        print(f"Message {messageSid} not found")
        return jsonify({'error': 'Message not found'}), 404

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

@app.route('/confirmed')
def confirmed():
    return render_template('confirmed.html')

import re

def normalize_time(raw_time):
    """
    Приймає raw_time типу '17.20', '7.5', '23:5' і повертає 'HH:MM'
    """
    if not raw_time:
        return None

    # Замінюємо крапку на двокрапку
    fixed_time = raw_time.replace('.', ':')

    # Розбиваємо на години і хвилини
    match = re.match(r'^(\d{1,2}):(\d{1,2})$', fixed_time)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        return f"{hours:02d}:{minutes:02d}"  # Формат: HH:MM
    else:
        return None


from flask import request, jsonify

@app.route('/update_task/<sid>', methods=['POST'])
def update_task(sid):
    updated_data = request.json  # словник з оновленими значеннями
    # Тепер оновіть відповідну задачу в базі даних або іншому сховищі

    # Якщо task у тебе прив’язаний до sid у базі даних:
    message = Message.query.filter_by(sid=sid).first()
    if not message:
        return jsonify({'error': 'Message not found'}), 404

    message.ai_task = updated_data  # Якщо ai_task — це JSONB поле
    db.session.commit()

    return jsonify({'success': True})
    
with app.app_context():
    db.create_all()
    
if __name__ == "__main__":

    app.run(debug=True)
