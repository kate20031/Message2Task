from flask import Blueprint, session, render_template, redirect, url_for, flash
from ..models import Message


dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('auth.login'))


    messages = Message.query.filter_by(user_id=session['user_id']).order_by(Message.date.desc()).limit(10).all()

    message_list = [{
        'from': msg.from_user,
        'ai_task': msg.ai_task,
        'date': msg.date
    } for msg in messages]

    return render_template('dashboard.html', username=session['user'], messages=message_list)
