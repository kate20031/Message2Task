from models import Message, db

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
