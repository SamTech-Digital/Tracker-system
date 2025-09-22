#!/usr/bin/env python3
"""
Fix Notifications Script
Helps diagnose and fix email and SMS notification issues
"""

import os
import sys
from utils.email_notifications import EmailNotifications
from utils.sms_utils import RapidAPISMS

def check_environment_variables():
    """Check if all required environment variables are set"""
    print("🔍 CHECKING ENVIRONMENT VARIABLES")
    print("=" * 50)
    
    email_vars = {
        'SMTP_SERVER': os.environ.get('SMTP_SERVER'),
        'SMTP_PORT': os.environ.get('SMTP_PORT'),
        'SMTP_USER': os.environ.get('SMTP_USER'),
        'SMTP_PASS': os.environ.get('SMTP_PASS'),
        'FROM_EMAIL': os.environ.get('FROM_EMAIL'),
    }
    
    sms_vars = {
        'RAPIDAPI_KEY': os.environ.get('RAPIDAPI_KEY'),
        'RAPIDAPI_SMS_HOST': os.environ.get('RAPIDAPI_SMS_HOST'),
    }
    
    print("📧 Email Configuration:")
    for var, value in email_vars.items():
        if value:
            if 'PASS' in var:
                print(f"  ✅ {var}: {'*' * len(value)}")
            else:
                print(f"  ✅ {var}: {value}")
        else:
            print(f"  ❌ {var}: NOT SET")
    
    print("\n📱 SMS Configuration:")
    for var, value in sms_vars.items():
        if value:
            if 'KEY' in var:
                print(f"  ✅ {var}: {'*' * len(value)}")
            else:
                print(f"  ✅ {var}: {value}")
        else:
            print(f"  ❌ {var}: NOT SET")
    
    return email_vars, sms_vars

def test_email_configuration():
    """Test email configuration"""
    print("\n📧 TESTING EMAIL CONFIGURATION")
    print("=" * 50)
    
    email_service = EmailNotifications()
    
    # Check if credentials are set
    if not email_service.smtp_user or not email_service.smtp_pass:
        print("❌ Email credentials not configured")
        print("   Please set SMTP_USER and SMTP_PASS environment variables")
        return False
    
    print(f"✅ SMTP Server: {email_service.smtp_server}")
    print(f"✅ SMTP Port: {email_service.smtp_port}")
    print(f"✅ SMTP User: {email_service.smtp_user}")
    print(f"✅ SMTP Pass: {'*' * len(email_service.smtp_pass)}")
    
    # Test connection
    try:
        import smtplib
        import ssl
        
        context = ssl.create_default_context()
        
        if email_service.smtp_port == 465:
            with smtplib.SMTP_SSL(email_service.smtp_server, email_service.smtp_port, context=context) as server:
                server.login(email_service.smtp_user, email_service.smtp_pass)
                print("✅ Email authentication successful!")
                return True
        else:
            with smtplib.SMTP(email_service.smtp_server, email_service.smtp_port) as server:
                server.starttls(context=context)
                server.login(email_service.smtp_user, email_service.smtp_pass)
                print("✅ Email authentication successful!")
                return True
                
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Email authentication failed: {e}")
        print("\n🔧 SOLUTION:")
        print("   1. Enable 2-Factor Authentication on your Gmail account")
        print("   2. Generate an App Password:")
        print("      - Go to https://myaccount.google.com/")
        print("      - Security → 2-Step Verification → App passwords")
        print("      - Select 'Mail' and generate a new app password")
        print("   3. Use the 16-character app password in your .env file")
        return False
        
    except Exception as e:
        print(f"❌ Email connection failed: {e}")
        return False

def test_sms_configuration():
    """Test SMS configuration"""
    print("\n📱 TESTING SMS CONFIGURATION")
    print("=" * 50)
    
    sms_service = RapidAPISMS()
    
    if not sms_service.api_key:
        print("❌ RAPIDAPI_KEY not configured")
        print("   Please set RAPIDAPI_KEY environment variable")
        return False
    
    print(f"✅ API Key: {'*' * len(sms_service.api_key)}")
    print(f"✅ API Host: {sms_service.api_host}")
    
    # Test service connectivity
    result = sms_service.test_sms_service()
    
    if result['success']:
        print("✅ SMS service connectivity successful!")
        return True
    else:
        print(f"❌ SMS service test failed: {result['error']}")
        print("\n🔧 SOLUTION:")
        print("   1. Check your RapidAPI subscription:")
        print("      - Go to https://rapidapi.com")
        print("      - Ensure you're subscribed to an SMS service")
        print("   2. Try a different SMS service:")
        print("      RAPIDAPI_SMS_HOST=textlocal.p.rapidapi.com")
        print("      RAPIDAPI_SMS_HOST=twilio-sms.p.rapidapi.com")
        print("      RAPIDAPI_SMS_HOST=nexmo-sms.p.rapidapi.com")
        return False

def create_env_template():
    """Create a template .env file"""
    print("\n📝 CREATING .env TEMPLATE")
    print("=" * 50)
    
    template = """# Flask Configuration
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///attendance.db

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Email Configuration (Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=samtechdigital30@gmail.com
SMTP_PASS=your-16-character-app-password
FROM_EMAIL=samtechdigital30@gmail.com
FROM_NAME=Teachers Attendance System

# RapidAPI SMS Configuration
RAPIDAPI_KEY=your-rapidapi-key-here
RAPIDAPI_SMS_HOST=textlocal.p.rapidapi.com
"""
    
    with open('.env.template', 'w') as f:
        f.write(template)
    
    print("✅ Created .env.template file")
    print("   Copy this file to .env and update with your actual values")

def main():
    """Main function"""
    print("🔧 NOTIFICATION FIX SCRIPT")
    print("=" * 50)
    print("This script will help you diagnose and fix notification issues")
    print()
    
    # Check environment variables
    email_vars, sms_vars = check_environment_variables()
    
    # Test email
    email_ok = test_email_configuration()
    
    # Test SMS
    sms_ok = test_sms_configuration()
    
    # Summary
    print("\n📊 SUMMARY")
    print("=" * 50)
    if email_ok:
        print("✅ Email configuration is working")
    else:
        print("❌ Email configuration needs fixing")
    
    if sms_ok:
        print("✅ SMS configuration is working")
    else:
        print("❌ SMS configuration needs fixing")
    
    if not email_ok or not sms_ok:
        print("\n🔧 NEXT STEPS:")
        print("   1. Follow the solutions above to fix the issues")
        print("   2. Run this script again to verify the fixes")
        print("   3. Try adding a teacher again")
        
        # Create template if needed
        if not os.path.exists('.env'):
            create_env_template()

if __name__ == "__main__":
    main() 