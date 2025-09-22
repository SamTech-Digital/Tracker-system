# Teacher Attendance System

A modern, QR Code-based Teacher Attendance Management System built with Python Flask. This system provides a clean, scalable solution for tracking teacher attendance with real-time status updates, comprehensive reporting, and automated notifications via SMS and email.

## 🚀 Features

### Core Functionality
- **QR Code Generation**: Automatic QR code creation for each teacher
- **Real-time Attendance Tracking**: Check-in/check-out with timestamp recording
- **Smart Status Determination**: Automatic classification (On Time, Late, Absent)
- **Manual Entry Fallback**: Backup option when QR scanning fails
- **Comprehensive Reporting**: Filterable attendance reports and statistics

### Admin Panel
- **Teacher Management**: Add, view, and manage teacher profiles
- **Dashboard**: Real-time attendance statistics and recent records
- **Attendance Reports**: Detailed reports with filtering options
- **QR Code Management**: Generate and manage teacher QR codes

### Notifications & Communication
**QR Code Email**: Professional welcome emails with QR code attachments
**Attendance Confirmations**: Email notifications for check-in/check-out events
**HTML Email Templates**: Beautiful, responsive email designs

### Attendance Rules
- **Check-in Windows**:
  - On Time: 6:00 AM - 7:00 AM
  - Late: 7:01 AM - 10:00 AM
  - Absent: After 11:00 AM
- **Check-out Window**: 2:00 PM - 6:00 PM
- **Real-time Status Updates**: Automatic status determination based on check-in time

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (easily configurable for PostgreSQL/MySQL)
- **ORM**: SQLAlchemy
- **QR Code**: qrcode library
// Removed SMS: RapidAPI SMS services
- **Email**: SMTP with HTML templates
- **Frontend**: Bootstrap 5 + Font Awesome
- **Architecture**: MVC pattern with separation of concerns

## 📁 Project Structure

```
teachers-tracker-system/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── SETUP_SMS_EMAIL.md    # SMS and Email setup guide
├── routes/               # Route blueprints
│   ├── __init__.py
│   ├── admin_routes.py   # Admin panel routes
│   ├── attendance_routes.py # Attendance routes
│   └── auth_routes.py    # Authentication routes
├── utils/                # Utility modules
│   ├── __init__.py
│   ├── qrcode_utils.py   # QR code generation
│   ├── attendance_logic.py # Business logic
│   ├── sms_utils.py      # RapidAPI SMS integration
│   └── email_notifications.py # Email notification system
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── admin/            # Admin templates
│   ├── attendance/       # Attendance templates
│   └── auth/             # Authentication templates
└── static/              # Static files (CSS, JS, QR codes)
    └── qrcodes/         # Generated QR code images
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
// Removed RapidAPI account (for SMS notifications)
- Email account (for email notifications)

### Installation

1. **Clone or download the project**
   ```bash
   # If using git
   git clone <repository-url>
   cd teachers-tracker-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Create .env file with your configuration
   cp .env.example .env
   # Edit .env with your actual values
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the system**
   - Open your browser and go to `http://localhost:5000`
   - The system will automatically create the database and tables

### First Time Setup

1. **Configure Notifications**: Set up email credentials (see SETUP_SMS_EMAIL.md)
2. **Add Teachers**: Go to Admin → Add Teacher to create teacher profiles
3. **Generate QR Codes**: QR codes are automatically generated when teachers are added
4. **Test Notifications**: Verify email notifications are working
5. **Test Attendance**: Use the attendance scanner to test check-in/check-out functionality

## 📖 Usage Guide

### For Administrators

#### Adding Teachers
1. Navigate to Admin → Add Teacher
2. Enter teacher name, email, and phone number
3. System automatically:
   - Generates unique ID and QR code
   - Sends welcome email with QR code attachment
4. View notification status on success page
5. Print or share QR code with the teacher

#### Viewing Reports
1. Go to Admin → Reports
2. Use filters to view specific data:
   - Date range
   - Teacher name/ID
   - Attendance status
3. Export or analyze attendance patterns

#### Dashboard Overview
- Real-time attendance statistics
- Recent check-in/check-out records
- Quick access to common actions

### For Teachers

#### QR Code Check-in/Check-out
1. Navigate to Attendance → QR Scanner
2. Scan your unique QR code
3. System automatically:
   - Determines status and records time
   - Sends confirmation email (if email configured)
4. Receive confirmation message

#### Manual Entry (Backup)
1. Go to Attendance → Manual Entry
2. Enter your unique teacher ID
3. Select check-in or check-out action
4. Submit to record attendance

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:
```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///attendance.db
FLASK_ENV=production

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
FROM_EMAIL=your-email@gmail.com
FROM_NAME=Teachers Attendance System

// Removed RapidAPI SMS Configuration
```

### Database Configuration
The system uses SQLite by default. For production, configure PostgreSQL or MySQL:
```python
# In app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/dbname'
```

### Timezone Configuration
Update timezone in `utils/attendance_logic.py`:
```python
local_tz = pytz.timezone('Your/Timezone')  # e.g., 'America/New_York'
```

## 📧 Notification Features

### Email Notifications
- **Welcome Email**: Professional HTML email with QR code attachment
- **Attendance Confirmations**: Email notifications for check-in/check-out
- **Beautiful Templates**: Responsive HTML email designs
- **Error Handling**: Graceful handling of email failures

### Setup Instructions
For detailed setup instructions, see [SETUP_SMS_EMAIL.md](SETUP_SMS_EMAIL.md)

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Python venv
```bash
python -m venv venv
```

### Activation
```bash
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### To update requirements.txt
```bash
### Railway Deployment

1. **Create a Railway account**: Go to [Railway](https://railway.app/) and sign up.
2. **Import your GitHub repository**: Click 'New Project' → 'Deploy from GitHub repo'.
3. **Configure build and start commands**:
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `gunicorn app:app`
4. **Set environment variables**: Add your secrets and configuration in the Railway dashboard (see `.env` example above).
5. **Deploy**: Railway will automatically build and deploy your app. Access your app via the provided Railway URL.
```

### Production Deployment
1. **Using Gunicorn**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Using Docker**:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

3. **Cloud Platforms**:
   - **Heroku**: Add `Procfile` with `web: gunicorn app:app`
   - **Render**: Configure build command and start command
   - **Railway**: Direct deployment from GitHub

## 🔒 Security Features

- **Unique Teacher IDs**: Secure, randomly generated identifiers
- **Input Validation**: Server-side validation for all inputs
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **CSRF Protection**: Flask-WTF integration (can be added)
- **Secure Notifications**: Environment-based configuration for sensitive data
- **App Passwords**: Support for email app passwords instead of regular passwords

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the [SETUP_SMS_EMAIL.md](SETUP_SMS_EMAIL.md) for notification setup
- Review the troubleshooting section in the setup guide
- Check application logs for detailed error messages

---

**Built with ❤️ using Python Flask** 


---
1. Push Your Changes to GitHub (on your local machine)
Open PowerShell in your project folder and run:

git add .
git commit -m "Your commit message"
git push origin main

Make changes to your code locally.
Commit and push changes to your GitHub repo.
On PythonAnywhere, open a Bash console and pull the latest changes:
"cd ~/Tracker-system
git pull"
then reload webapp on pythonanywhere.