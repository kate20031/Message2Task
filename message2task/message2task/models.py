from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
