from datetime import datetime, time, date
from models import db, Teacher, Attendance
from utils.email_notifications import email_service

class AttendanceLogic:
    """Core business logic for attendance management"""
    
    # Attendance time windows
    ON_TIME_START = time(6, 0)  # 6:00 AM
    ON_TIME_END = time(7, 0)    # 7:00 AM
    LATE_END = time(10, 0)      # 10:00 AM
    ABSENT_DEADLINE = time(11, 0)  # 11:00 AM
    CHECKOUT_START = time(14, 0)   # 2:00 PM
    CHECKOUT_END = time(18, 0)     # 6:00 PM
    
    @staticmethod
    def get_current_time():
        """Get current time in local timezone"""
        return datetime.now()
    
    @staticmethod
    def determine_attendance_status(check_in_time):
        """
        Determine attendance status based on check-in time
        
        Args:
            check_in_time (datetime): Teacher's check-in time
            
        Returns:
            str: 'On Time', 'Late', or 'Absent'
        """
        check_in_time_only = check_in_time.time()
        
        if AttendanceLogic.ON_TIME_START <= check_in_time_only <= AttendanceLogic.ON_TIME_END:
            return 'On Time'
        elif AttendanceLogic.ON_TIME_END < check_in_time_only <= AttendanceLogic.LATE_END:
            return 'Late'
        else:
            return 'Absent'
    
    @staticmethod
    def can_check_out(check_out_time):
        """
        Check if teacher can check out at the given time
        
        Args:
            check_out_time (datetime): Proposed check-out time
            
        Returns:
            bool: True if check-out is allowed
        """
        check_out_time_only = check_out_time.time()
        return AttendanceLogic.CHECKOUT_START <= check_out_time_only <= AttendanceLogic.CHECKOUT_END
    
    @staticmethod
    def process_check_in(teacher_unique_id):
        """
        Process teacher check-in
        
        Args:
            teacher_unique_id (str): Teacher's unique identifier
            
        Returns:
            dict: Result with status, message, and attendance data
        """
        try:
            # Find teacher
            teacher = Teacher.query.filter_by(unique_id=teacher_unique_id, is_active=True).first()
            if not teacher:
                return {
                    'success': False,
                    'message': 'Teacher not found or inactive',
                    'data': None
                }
            
            current_time = AttendanceLogic.get_current_time()
            current_date = current_time.date()
            
            # Check if attendance record already exists for today
            existing_attendance = Attendance.query.filter_by(
                teacher_id=teacher.id,
                date=current_date
            ).first()
            
            if existing_attendance and existing_attendance.check_in_time:
                return {
                    'success': False,
                    'message': f'Already checked in at {existing_attendance.check_in_time.strftime("%I:%M %p")}',
                    'data': existing_attendance.to_dict()
                }
            
            # Determine attendance status
            status = AttendanceLogic.determine_attendance_status(current_time)
            
            # Create or update attendance record
            if existing_attendance:
                existing_attendance.check_in_time = current_time
                existing_attendance.status = status
                attendance = existing_attendance
            else:
                attendance = Attendance(
                    teacher_id=teacher.id,
                    date=current_date,
                    check_in_time=current_time,
                    status=status
                )
                db.session.add(attendance)
            
            db.session.commit()
            
            # Send email notification if teacher has email
            email_result = None
            if teacher.email:
                email_result = email_service.send_attendance_notification(
                    teacher.email,
                    teacher.name,
                    'check_in',
                    current_time.strftime('%Y-%m-%d %I:%M %p')
                )
            
            # Generate appropriate message
            if status == 'On Time':
                message = f'Welcome, {teacher.name}! Have a great day!'
            elif status == 'Late':
                message = f'Welcome, {teacher.name}! You are marked as late.'
            else:
                message = f'Welcome, {teacher.name}! You are marked as absent.'
            
            return {
                'success': True,
                'message': message,
                'data': attendance.to_dict(),
                'status': status,
                'email_result': email_result
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error processing check-in: {str(e)}',
                'data': None
            }
    
    @staticmethod
    def process_check_out(teacher_unique_id):
        """
        Process teacher check-out
        
        Args:
            teacher_unique_id (str): Teacher's unique identifier
            
        Returns:
            dict: Result with status, message, and attendance data
        """
        try:
            # Find teacher
            teacher = Teacher.query.filter_by(unique_id=teacher_unique_id, is_active=True).first()
            if not teacher:
                return {
                    'success': False,
                    'message': 'Teacher not found or inactive',
                    'data': None
                }
            
            current_time = AttendanceLogic.get_current_time()
            current_date = current_time.date()
            
            # Check if attendance record exists for today
            attendance = Attendance.query.filter_by(
                teacher_id=teacher.id,
                date=current_date
            ).first()
            
            if not attendance:
                return {
                    'success': False,
                    'message': 'No check-in record found for today',
                    'data': None
                }
            
            if not attendance.check_in_time:
                return {
                    'success': False,
                    'message': 'Must check in before checking out',
                    'data': None
                }
            
            if attendance.check_out_time:
                return {
                    'success': False,
                    'message': f'Already checked out at {attendance.check_out_time.strftime("%I:%M %p")}',
                    'data': attendance.to_dict()
                }
            
            # Check if check-out is allowed at this time
            if not AttendanceLogic.can_check_out(current_time):
                return {
                    'success': False,
                    'message': 'Check-out is only allowed between 2:00 PM and 6:00 PM',
                    'data': None
                }
            
            # Update check-out time
            attendance.check_out_time = current_time
            db.session.commit()
            
            # Send email notification if teacher has email
            email_result = None
            if teacher.email:
                email_result = email_service.send_attendance_notification(
                    teacher.email,
                    teacher.name,
                    'check_out',
                    current_time.strftime('%Y-%m-%d %I:%M %p')
                )
            
            message = f'Thanks for your wonderful work today, {teacher.name}! See you tomorrow. Byeee!'
            
            return {
                'success': True,
                'message': message,
                'data': attendance.to_dict(),
                'email_result': email_result
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error processing check-out: {str(e)}',
                'data': None
            }
    
    @staticmethod
    def get_attendance_summary(date_filter=None, teacher_filter=None, status_filter=None):
        """
        Get attendance summary with optional filters
        Args:
            date_filter (str): Date filter (YYYY-MM-DD)
            teacher_filter (str): Teacher name or ID filter
            status_filter (str): Status filter (On Time, Late, Absent)
        Returns:
            dict: Summary statistics and filtered records
        """
        from flask import session
        user_id = session.get('user_id')
        query = Attendance.query.join(Teacher).filter(Teacher.user_id == user_id)

        # Apply filters
        if date_filter:
            try:
                filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                query = query.filter(Attendance.date == filter_date)
            except ValueError:
                pass

        if teacher_filter:
            query = query.filter(
                (Teacher.name.ilike(f'%{teacher_filter}%')) |
                (Teacher.unique_id.ilike(f'%{teacher_filter}%'))
            )

        if status_filter:
            query = query.filter(Attendance.status == status_filter)

        # Get records
        records = query.order_by(Attendance.date.desc(), Attendance.check_in_time.desc()).all()

        # Calculate summary
        total_records = len(records)
        on_time_count = sum(1 for r in records if r.status == 'On Time')
        late_count = sum(1 for r in records if r.status == 'Late')
        absent_count = sum(1 for r in records if r.status == 'Absent')

        return {
            'total_records': total_records,
            'on_time_count': on_time_count,
            'late_count': late_count,
            'absent_count': absent_count,
            'records': [record.to_dict() for record in records]
        }