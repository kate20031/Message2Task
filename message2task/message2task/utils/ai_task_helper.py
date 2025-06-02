from models import Message, db
from flask import session
from strategy.strategy_gemini import GeminiExtractionStrategy
from strategy.extractor_context import TaskExtractorContext
from utils.time_utils import normalize_time
from sqlite3 import IntegrityError

def get_or_create_ai_task(msg):
    existing = Message.query.filter_by(sid=msg.sid).first()
    if existing:
        return existing.ai_task

    context = TaskExtractorContext(GeminiExtractionStrategy())
    ai_result = context.extract_task(msg.body)

    if not isinstance(ai_result, dict):
        return None

    if 'Time' in ai_result:
        ai_result['Time'] = normalize_time(ai_result['Time'])

    try:
        user_id = session.get('user_id')
        if not user_id:
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
        return ai_result
    except IntegrityError:
        db.session.rollback()
        return None
