from models import Message, db
from flask import session
from strategy.strategy_gemini import GeminiExtractionStrategy
from strategy.extractor_context import TaskExtractorContext
from utils.time_utils import normalize_time
from sqlite3 import IntegrityError


def get_or_create_ai_task(msg):
    existing = Message.query.filter_by(sid=msg.sid).first()
    if existing:
        print(f"Using cached AI task for sid={msg.sid}")
        return existing.ai_task

    from .strategy_gemini import GeminiExtractionStrategy
    from .extractor_context import TaskExtractorContext

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


def generate_ai_tasks():
    tasks = [
        {"task": "Explain the concept of the sun", "status": "pending"},
        {"task": "Describe the sun's impact on Earth's climate", "status": "pending"}
    ]
    return tasks
