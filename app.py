from dotenv import load_dotenv
load_dotenv()
from flask import Flask, redirect, url_for, session, jsonify
import os
from datetime import datetime
from models import db, User

# Initialize Flask app

app = Flask(__name__)
# Configuration

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Default admin credentials (for demo; change in production)
app.config['ADMIN_USERNAME'] = os.environ.get('ADMIN_USERNAME', 'admin')
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'admin123')

db.init_app(app)

# Import routes after db initialization to avoid circular imports
from Tracker.routes import admin_routes, attendance_routes, auth_routes

# Register blueprints

app.register_blueprint(admin_routes.bp)
app.register_blueprint(attendance_routes.bp)
app.register_blueprint(auth_routes.bp)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('auth.login'))


# Utility route to remove all users (for admin/debug only)
@app.route('/remove_all_users')
def remove_all_users():
    with app.app_context():
        num_deleted = User.query.delete()
        db.session.commit()
    return jsonify({'message': f'All users removed. Deleted: {num_deleted}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)