from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)



class Teacher(db.Model):
    """Teacher model for storing teacher information and QR codes"""
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(50), unique=True, nullable=False, default=lambda: str(uuid.uuid4())[:8])
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    department = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship with attendance records
    attendance_records = db.relationship('Attendance', backref='teacher', lazy=True)
    
    def __repr__(self):
        return f'<Teacher {self.name} ({self.unique_id}) - {self.department}>'
    
    def to_dict(self):
        """Convert teacher object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'unique_id': self.unique_id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'phone_number': self.phone_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

class Attendance(db.Model):
    """Attendance model for storing check-in/check-out records"""
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in_time = db.Column(db.DateTime, nullable=True)
    check_out_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Absent')  # On Time, Late, Absent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Composite unique constraint to prevent duplicate records per teacher per day
    __table_args__ = (db.UniqueConstraint('teacher_id', 'date', name='_teacher_date_uc'),)
    
    def __repr__(self):
        return f'<Attendance {self.teacher.name} - {self.date} ({self.status})>'
    
    def to_dict(self):
        """Convert attendance object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher.name if self.teacher else None,
            'teacher_unique_id': self.teacher.unique_id if self.teacher else None,
            'date': self.date.isoformat() if self.date else None,
            'check_in_time': self.check_in_time.isoformat() if self.check_in_time else None,
            'check_out_time': self.check_out_time.isoformat() if self.check_out_time else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 