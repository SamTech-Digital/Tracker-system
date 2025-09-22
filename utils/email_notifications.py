from models import db, Teacher, Attendance
from datetime import date, datetime, time
import smtplib
import ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from typing import Dict, Any, Optional

def send_missed_signin_notifications():
    today = date.today()
    # Teachers who have not checked in today
    teachers = Teacher.query.filter_by(is_active=True).all()
    for teacher in teachers:
        attendance = Attendance.query.filter_by(teacher_id=teacher.id, date=today).first()
        if not attendance and teacher.email:
            # Send missed sign-in email
            send_notification_email(
                teacher.email,
                teacher.name,
                "You missed signing in today",
                f"Dear {teacher.name},\n\nOur records show you did not sign in today. Please contact your admin if this is an error.\n\nBest regards,\nAttendance System"
            )

def send_missed_signout_notifications():
    
    today = date.today()
    now = datetime.now().time()
    # Only run after sign-out window closes
    if now < time(18, 0):
        return
    teachers = Teacher.query.filter_by(is_active=True).all()
    for teacher in teachers:
        attendance = Attendance.query.filter_by(teacher_id=teacher.id, date=today).first()
        if attendance and attendance.check_in_time and not attendance.check_out_time and teacher.email:
            # Send missed sign-out email
            send_notification_email(
                teacher.email,
                teacher.name,
                "You missed signing out today",
                f"Dear {teacher.name},\n\nOur records show you did not sign out today. Please remember to check out next time.\n\nBest regards,\nAttendance System"
            )

def send_notification_email(to_email, teacher_name, subject, body):
    """Legacy function for backward compatibility"""
    # Use the new email service
    return email_service.send_attendance_notification(
        to_email, 
        teacher_name, 
        'notification', 
        datetime.now().strftime('%Y-%m-%d %I:%M %p')
    )

class EmailNotifications:
    """Email notification utility for sending QR codes and notifications"""
    
    def __init__(self):
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', 587))
        self.smtp_user = os.environ.get('SMTP_USER')
        self.smtp_pass = os.environ.get('SMTP_PASS')
        self.from_email = os.environ.get('FROM_EMAIL', self.smtp_user)
        self.from_name = os.environ.get('FROM_NAME', 'Teachers Attendance System')
        
    def send_qr_code_email(self, to_email: str, teacher_name: str, qr_path: str, 
                          teacher_unique_id: str) -> Dict[str, Any]:
        """
        Send welcome email with QR code attachment to newly added teacher
        
        Args:
            to_email: Teacher's email address
            teacher_name: Teacher's name
            qr_path: Path to the QR code image file
            teacher_unique_id: Teacher's unique ID
            
        Returns:
            Dict containing success status and response details
        """
        if not all([self.smtp_user, self.smtp_pass]):
            return {
                'success': False,
                'error': 'SMTP credentials not configured in environment variables'
            }
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'Welcome to Teachers Attendance System - Your QR Code'
            msg['From'] = f'{self.from_name} <{self.from_email}>'
            msg['To'] = to_email
            
            # Create HTML content
            html_content = self._create_welcome_html(teacher_name, teacher_unique_id)
            msg.attach(MIMEText(html_content, 'html'))
            
            # Attach QR code image
            if os.path.exists(qr_path):
                with open(qr_path, 'rb') as f:
                    img_data = f.read()
                    image = MIMEImage(img_data)
                    image.add_header('Content-ID', '<qr_code>')
                    image.add_header('Content-Disposition', 'attachment', 
                                   filename=f'qr_code_{teacher_unique_id}.png')
                    msg.attach(image)
            
            # Send email
            context = ssl.create_default_context()
            
            if self.smtp_port == 465:
                # Use SMTP_SSL for port 465
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                    server.login(self.smtp_user, self.smtp_pass)
                    server.send_message(msg)
            else:
                # Use SMTP with STARTTLS for other ports
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls(context=context)
                    server.login(self.smtp_user, self.smtp_pass)
                    server.send_message(msg)
            
            return {
                'success': True,
                'message': f'Welcome email sent successfully to {to_email}',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to send email to {to_email}: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def send_attendance_notification(self, to_email: str, teacher_name: str, 
                                   attendance_type: str, timestamp: str) -> Dict[str, Any]:
        """
        Send attendance confirmation email
        
        Args:
            to_email: Teacher's email address
            teacher_name: Teacher's name
            attendance_type: Type of attendance ("check_in" or "check_out")
            timestamp: Timestamp of the attendance action
            
        Returns:
            Dict containing success status and response details
        """
        if not all([self.smtp_user, self.smtp_pass]):
            return {
                'success': False,
                'error': 'SMTP credentials not configured in environment variables'
            }
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'Attendance {attendance_type.replace("_", " ").title()} Confirmation'
            msg['From'] = f'{self.from_name} <{self.from_email}>'
            msg['To'] = to_email
            
            html_content = self._create_attendance_html(teacher_name, attendance_type, timestamp)
            msg.attach(MIMEText(html_content, 'html'))
            
            context = ssl.create_default_context()
            
            if self.smtp_port == 465:
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                    server.login(self.smtp_user, self.smtp_pass)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls(context=context)
                    server.login(self.smtp_user, self.smtp_pass)
                    server.send_message(msg)
            
            return {
                'success': True,
                'message': f'Attendance notification sent to {to_email}',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to send attendance notification to {to_email}: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def _create_welcome_html(self, teacher_name: str, teacher_unique_id: str) -> str:
        """Create HTML content for welcome email"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                         color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .qr-section {{ text-align: center; margin: 30px 0; padding: 20px; background: white; border-radius: 8px; }}
                .qr-code {{ max-width: 200px; border: 2px solid #ddd; border-radius: 8px; }}
                .highlight {{ background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎓 Welcome to Teachers Attendance System</h1>
                    <p>Your digital attendance tracking solution</p>
                </div>
                
                <div class="content">
                    <h2>Hello {teacher_name}!</h2>
                    
                    <p>Welcome to the Teachers Attendance System! You have been successfully added to our digital attendance tracking platform.</p>
                    
                    <div class="highlight">
                        <strong>Your Unique ID:</strong> <code>{teacher_unique_id}</code><br>
                        <small>Keep this ID safe - you'll need it for manual entry if needed.</small>
                    </div>
                    
                    <div class="qr-section">
                        <h3>📱 Your QR Code</h3>
                        <p>Your unique QR code is attached to this email. Use it to:</p>
                        <ul style="text-align: left; display: inline-block;">
                            <li>Check in when you arrive at work</li>
                            <li>Check out when you leave</li>
                            <li>Track your attendance automatically</li>
                        </ul>
                        <br><br>
                        <img src="cid:qr_code" alt="Your QR Code" class="qr-code">
                    </div>
                    
                    <h3>🚀 How to Use Your QR Code</h3>
                    <ol>
                        <li>Save the QR code image to your phone</li>
                        <li>When arriving at work, scan the QR code at the attendance station</li>
                        <li>When leaving, scan the QR code again to check out</li>
                        <li>Your attendance will be automatically recorded</li>
                    </ol>
                    
                    <div class="highlight">
                        <strong>Important:</strong> Always scan your QR code for accurate attendance tracking. 
                        If you forget your QR code, you can use your unique ID for manual entry.
                    </div>
                    
                    <p>If you have any questions or need assistance, please contact your administrator.</p>
                    
                    <p>Best regards,<br>
                    <strong>SamTeck Digital Hub Team</strong></p>
                </div>
                
                <div class="footer">
                    <p>This is an automated message from the Teachers Attendance System.<br>
                    Please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_attendance_html(self, teacher_name: str, attendance_type: str, timestamp: str) -> str:
        """Create HTML content for attendance notification"""
        action_text = "checked in" if attendance_type == "check_in" else "checked out"
        icon = "✅" if attendance_type == "check_in" else "🏠"
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
                         color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .confirmation {{ text-align: center; margin: 30px 0; padding: 20px; background: white; border-radius: 8px; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{icon} Attendance Confirmation</h1>
                    <p>Your attendance has been recorded</p>
                </div>
                
                <div class="content">
                    <h2>Hello {teacher_name}!</h2>
                    
                    <div class="confirmation">
                        <h3>Attendance Recorded Successfully</h3>
                        <p>You have successfully <strong>{action_text}</strong> at:</p>
                        <h2 style="color: #4CAF50;">{timestamp}</h2>
                    </div>
                    
                    <p>Thank you for using the Teachers Attendance System!</p>
                    
                    <p>Best regards,<br>
                    <strong>SamTeck Digital Hub Team</strong></p>
                </div>
                
                <div class="footer">
                    <p>This is an automated message from the Teachers Attendance System.<br>
                    Please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """

# Global instance
email_service = EmailNotifications()
