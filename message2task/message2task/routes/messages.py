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
    ...
    
@messages_bp.route("/update_task/<sid>", methods=['POST'])
def update_task(sid):
    ...
    
@messages_bp.route('/delete_message/<messageSid>', methods=['DELETE'])
def delete_message(messageSid):
    ...

@messages_bp.route("/webhook", methods=['POST'])
def webhook():
    ...
