from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Always show login page, even if already logged in
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['first_name'] = user.first_name
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('auth/login.html')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        first_name = request.form.get('first_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('auth/register.html')
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('auth/register.html')
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('auth/register.html')
        user = User(
            username=username,
            first_name=first_name,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        session['first_name'] = user.first_name

        # Send verification email
        from utils.email_notifications import EmailNotifications
        email_service = EmailNotifications()
        verification_result = email_service.send_attendance_notification(
            to_email=email,
            teacher_name=username,
            attendance_type='verify_email',
            timestamp=''
        )
        if verification_result.get('success'):
            flash('Registration successful! Please check your email to verify your account.', 'success')
        else:
            flash('Registration successful, but failed to send verification email.', 'warning')
        return redirect(url_for('auth.verify_email'))
    return render_template('auth/register.html')
# Add a simple verify_email route
@bp.route('/verify_email')
def verify_email():
    # Simulate email verification and log in the user
    # In a real app, you would verify a token here
    user = User.query.order_by(User.id.desc()).first()  # Get the most recently registered user
    if user:
        session['user_id'] = user.id
        flash('Email verified! You are now logged in.', 'success')
        return redirect(url_for('admin.dashboard'))
    else:
        flash('Verification failed. Please try again.', 'error')
        return redirect(url_for('auth.login'))

@bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
