from flask import Blueprint, request, session, jsonify
from models import Message, User, db
from utils.time_utils import normalize_time
from strategy_gemini import GeminiExtractionStrategy
from extractor_context import TaskExtractorContext
from twilio.rest import Client
from sqlite3 import IntegrityError

messages_bp = Blueprint('messages', __name__)

@messages_bp.route("/get_messages", methods=['GET'])
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


    
@messages_bp.route("/update_task/<sid>", methods=['POST'])
def update_task(sid):
    updated_data = request.json 
    message = Message.query.filter_by(sid=sid).first()
    if not message:
        return jsonify({'error': 'Message not found'}), 404

    message.ai_task = updated_data  
    db.session.commit()

    return jsonify({'success': True})
  
  
@messages_bp.route('/delete_message/<messageSid>', methods=['DELETE'])
def delete_message(messageSid):
    print(f"Received DELETE request for messageSid={messageSid}")
    success = delete_from_db(messageSid)
    if success:
        print(f"Message {messageSid} deleted successfully")
        return jsonify({'status': 'deleted'}), 200
    else:
        print(f"Message {messageSid} not found")
        return jsonify({'error': 'Message not found'}), 404


@messages_bp.route("/webhook", methods=['POST'])
def webhook():
    if request.content_type == 'application/json':
        data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form.to_dict()
    else:
        return "Unsupported Media Type", 415


    if data:
        return "Webhook received", 200
    else:
        return "No data received", 400

@messages_bp.route('/add_message', methods=['POST'])
def add_message():
    data = request.json
    new_message = Message(content=data['content'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message saved successfully!'})

