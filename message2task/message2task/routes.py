from flask import Blueprint, request, jsonify
from models import Message
from . import db

bp = Blueprint('main', __name__)

@bp.route('/add_message', methods=['POST'])
def add_message():
    data = request.json
    new_message = Message(content=data['content'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message saved successfully!'})
