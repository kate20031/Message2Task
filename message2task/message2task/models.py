# from message2task import db
#
# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     sid = db.Column(db.String(255), nullable=False)
#     from_user = db.Column(db.String(255), nullable=False)
#     ai_task = db.Column(db.Text, nullable=True)
#     date = db.Column(db.DateTime, nullable=False)
#     processed = db.Column(db.Boolean, default=False)
