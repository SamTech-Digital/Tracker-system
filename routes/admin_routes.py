from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from models import db, Teacher, Attendance
from utils.qrcode_utils import qr_generator
from utils.attendance_logic import AttendanceLogic
from utils.sms_utils import sms_service
from utils.email_notifications import email_service
from datetime import datetime, date
import uuid
import os

bp = Blueprint('admin', __name__, url_prefix='/admin')



@bp.route('/')
def dashboard():
    """Admin dashboard with attendance summary"""
    # If not logged in, redirect to login or register
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))
    today = date.today()
    # Get today's attendance summary
    summary = AttendanceLogic.get_attendance_summary(date_filter=today.strftime('%Y-%m-%d'))
    # Get recent attendance records
    recent_records = Attendance.query.join(Teacher).order_by(
        Attendance.date.desc(), 
        Attendance.check_in_time.desc()
    ).limit(10).all()
    from models import User
    user = User.query.get(session.get('user_id'))
    username = user.username if user else None
    first_name = user.first_name if user else None
    return render_template('admin/dashboard.html', 
                         summary=summary, 
                         recent_records=recent_records,
                         username=username,
                         first_name=first_name)

@bp.route('/teachers')
def teachers_list():
    """List all teachers"""
    user_id = session.get('user_id')
    teachers = Teacher.query.filter_by(is_active=True, user_id=user_id).order_by(Teacher.name).all()
    from models import User
    user = User.query.get(user_id)
    username = user.username if user else None
    first_name = user.first_name if user else None
    return render_template('admin/teachers_list.html', teachers=teachers, username=username, first_name=first_name)

@bp.route('/teachers/add', methods=['GET', 'POST'])
def add_teacher():
    """Add new teacher and generate QR code"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            department = request.form.get('department', '').strip()
            phone_number = request.form.get('phone_number', '').strip()
            
            if not name:
                flash('Teacher name is required', 'error')
                return render_template('admin/add_teacher.html')
            
            # Check if teacher with same name already exists
            existing_teacher = Teacher.query.filter_by(name=name).first()
            if existing_teacher:
                flash('Teacher with this name already exists', 'error')
                return render_template('admin/add_teacher.html')
            
            # Create new teacher
            teacher = Teacher(
                name=name,
                email=email if email else None,
                department=department if department else None,
                phone_number=phone_number if phone_number else None,
                unique_id=str(uuid.uuid4())[:8],
                user_id=session.get('user_id')
            )
            
            db.session.add(teacher)
            db.session.commit()
            
            # Generate QR code
            qr_filename, qr_data_url = qr_generator.generate_qr_code(
                teacher.unique_id,
                teacher.name
            )

            # Send welcome email with QR code if email is provided
            email_result = None
            if teacher.email:
                qr_path = qr_generator.get_qr_code_path(teacher.unique_id)
                email_result = email_service.send_qr_code_email(
                    to_email=teacher.email,
                    teacher_name=teacher.name,
                    qr_path=qr_path,
                    teacher_unique_id=teacher.unique_id
                )
            
            # Prepare success message
            success_message = f'Teacher {name} added successfully!'
            flash(success_message, 'success')
            return render_template('admin/teacher_created.html', 
                                 teacher=teacher, 
                                 qr_data_url=qr_data_url,
                                 email_result=email_result)
                                 
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding teacher: {str(e)}', 'error')
            return render_template('admin/add_teacher.html')
    
    return render_template('admin/add_teacher.html')

@bp.route('/teachers/<int:teacher_id>')
def teacher_detail(teacher_id):
    """View teacher details and attendance history"""
    teacher = Teacher.query.get_or_404(teacher_id)
    
    # Get teacher's attendance records
    attendance_records = Attendance.query.filter_by(teacher_id=teacher_id).order_by(
        Attendance.date.desc()
    ).limit(30).all()
    
    return render_template('admin/teacher_detail.html', 
                         teacher=teacher, 
                         attendance_records=attendance_records)

@bp.route('/teachers/delete/<int:teacher_id>', methods=['POST'])
def delete_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    try:
        # Delete all attendance records for this teacher
        Attendance.query.filter_by(teacher_id=teacher.id).delete()
        db.session.delete(teacher)
        db.session.commit()
        flash(f'Teacher {teacher.name} has been deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting teacher: {str(e)}', 'error')
    return redirect(url_for('admin.teachers_list'))

@bp.route('/attendance')
def attendance_reports():
    """Attendance reports with filters"""
    # Get filter parameters
    date_filter = request.args.get('date')
    teacher_filter = request.args.get('teacher')
    status_filter = request.args.get('status')
    
    # Get attendance summary
    summary = AttendanceLogic.get_attendance_summary(
        date_filter=date_filter,
        teacher_filter=teacher_filter,
        status_filter=status_filter
    )
    
    # Get all teachers for filter dropdown
    teachers = Teacher.query.filter_by(is_active=True).order_by(Teacher.name).all()
    
    return render_template('admin/attendance_reports.html',
                         summary=summary,
                         teachers=teachers,
                         filters={
                             'date': date_filter,
                             'teacher': teacher_filter,
                             'status': status_filter
                         })

@bp.route('/api/attendance/summary')
def api_attendance_summary():
    """API endpoint for attendance summary"""
    date_filter = request.args.get('date')
    teacher_filter = request.args.get('teacher')
    status_filter = request.args.get('status')
    
    summary = AttendanceLogic.get_attendance_summary(
        date_filter=date_filter,
        teacher_filter=teacher_filter,
        status_filter=status_filter
    )
    
    return jsonify(summary)

@bp.route('/manual-entry', methods=['GET', 'POST'])
def manual_entry():
    """Manual entry for check-in/check-out when QR fails"""
    if request.method == 'POST':
        teacher_unique_id = request.form.get('teacher_unique_id', '').strip()
        action = request.form.get('action')  # 'check_in' or 'check_out'
        
        if not teacher_unique_id:
            flash('Teacher ID is required', 'error')
            return render_template('admin/manual_entry.html')
        
        # Process the action
        if action == 'check_in':
            result = AttendanceLogic.process_check_in(teacher_unique_id)
        elif action == 'check_out':
            result = AttendanceLogic.process_check_out(teacher_unique_id)
        else:
            flash('Invalid action', 'error')
            return render_template('admin/manual_entry.html')
        
        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
        
        return render_template('admin/manual_entry.html', result=result)
    
    return render_template('admin/manual_entry.html') 