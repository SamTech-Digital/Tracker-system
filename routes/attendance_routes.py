from flask import Blueprint, render_template, request, jsonify, flash
from models import db, Teacher, Attendance
from utils.attendance_logic import AttendanceLogic
from utils.qrcode_utils import qr_generator
import re

bp = Blueprint('attendance', __name__, url_prefix='/attendance')

@bp.route('/')
def attendance_home():
    """Main attendance page for QR scanning"""
    return render_template('attendance/home.html')

@bp.route('/scan')
def scan_qr():
    """QR code scanning interface"""
    return render_template('attendance/scan.html')

@bp.route('/process-qr', methods=['POST'])
def process_qr():
    """Process QR code scan for check-in/check-out"""
    try:
        qr_data = request.form.get('qr_data', '').strip()
        action = request.form.get('action', 'check_in')  # 'check_in' or 'check_out'
        
        if not qr_data:
            return jsonify({
                'success': False,
                'message': 'No QR data received'
            })
        
        # Extract teacher unique ID from QR data
        # Expected format: "TEACHER:unique_id"
        match = re.match(r'TEACHER:([A-Za-z0-9]+)', qr_data)
        if not match:
            return jsonify({
                'success': False,
                'message': 'Invalid QR code format'
            })
        
        teacher_unique_id = match.group(1)
        
        # Process the action
        if action == 'check_in':
            result = AttendanceLogic.process_check_in(teacher_unique_id)
        elif action == 'check_out':
            result = AttendanceLogic.process_check_out(teacher_unique_id)
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid action'
            })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing QR code: {str(e)}'
        })

@bp.route('/manual')
def manual_entry():
    """Manual entry interface for when QR scanning fails"""
    return render_template('attendance/manual_entry.html')

@bp.route('/manual/process', methods=['POST'])
def process_manual():
    """Process manual entry for check-in/check-out"""
    try:
        teacher_unique_id = request.form.get('teacher_unique_id', '').strip()
        action = request.form.get('action')  # 'check_in' or 'check_out'
        
        if not teacher_unique_id:
            flash('Teacher ID is required', 'error')
            return render_template('attendance/manual_entry.html')
        
        # Process the action
        if action == 'check_in':
            result = AttendanceLogic.process_check_in(teacher_unique_id)
        elif action == 'check_out':
            result = AttendanceLogic.process_check_out(teacher_unique_id)
        else:
            flash('Invalid action', 'error')
            return render_template('attendance/manual_entry.html')
        
        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
        
        return render_template('attendance/manual_entry.html', result=result)
        
    except Exception as e:
        flash(f'Error processing manual entry: {str(e)}', 'error')
        return render_template('attendance/manual_entry.html')

@bp.route('/success')
def success():
    """Success page after successful check-in/check-out"""
    message = request.args.get('message', 'Operation completed successfully!')
    return render_template('attendance/success.html', message=message)

@bp.route('/error')
def error():
    """Error page for failed operations"""
    message = request.args.get('message', 'An error occurred!')
    return render_template('attendance/error.html', message=message)

@bp.route('/api/teacher/<teacher_unique_id>')
def get_teacher_info(teacher_unique_id):
    """API endpoint to get teacher information"""
    try:
        teacher = Teacher.query.filter_by(unique_id=teacher_unique_id, is_active=True).first()
        
        if not teacher:
            return jsonify({
                'success': False,
                'message': 'Teacher not found'
            })
        
        return jsonify({
            'success': True,
            'teacher': teacher.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving teacher info: {str(e)}'
        })

@bp.route('/api/attendance/today/<teacher_unique_id>')
def get_today_attendance(teacher_unique_id):
    """API endpoint to get today's attendance for a teacher"""
    try:
        teacher = Teacher.query.filter_by(unique_id=teacher_unique_id, is_active=True).first()
        
        if not teacher:
            return jsonify({
                'success': False,
                'message': 'Teacher not found'
            })
        
        from datetime import date
        today = date.today()
        
        attendance = Attendance.query.filter_by(
            teacher_id=teacher.id,
            date=today
        ).first()
        
        if attendance:
            return jsonify({
                'success': True,
                'attendance': attendance.to_dict()
            })
        else:
            return jsonify({
                'success': True,
                'attendance': None
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving attendance: {str(e)}'
        }) 