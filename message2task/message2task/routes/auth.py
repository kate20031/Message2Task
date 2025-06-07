from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=['GET', 'POST'])
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
            # return redirect(url_for('login'))
            return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user'] = user.username
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard.dashboard'))  # Assuming /dashboard route is in dashboard_bp
            # return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('login.html')


@auth_bp.route("/logout")
def logout():
    session.pop('user', None)
    session.pop('tasks', None)  # Clear tasks when logging out
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
    # return redirect(url_for('login'))
