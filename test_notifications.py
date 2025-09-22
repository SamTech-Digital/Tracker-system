#!/usr/bin/env python3
"""
Test script for email and SMS notifications
Run this script to test your configuration before using the main application
"""

import os
from dotenv import load_dotenv
from utils.email_notifications import email_service
from utils.sms_utils import sms_service

# Load environment variables
load_dotenv()

def test_email_configuration():
    """Test email configuration"""
    print("=" * 50)
    print("📧 TESTING EMAIL CONFIGURATION")
    print("=" * 50)
    
    # Check environment variables
    required_vars = ['SMTP_USER', 'SMTP_PASS', 'SMTP_SERVER', 'SMTP_PORT']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file")
        return False
    
    print(f"✅ SMTP Server: {os.environ.get('SMTP_SERVER')}")
    print(f"✅ SMTP Port: {os.environ.get('SMTP_PORT')}")
    print(f"✅ SMTP User: {os.environ.get('SMTP_USER')}")
    print(f"✅ SMTP Pass: {'*' * len(os.environ.get('SMTP_PASS', ''))}")
    
    # Test email service
    test_email = input("\nEnter test email address (or press Enter to skip): ").strip()
    if test_email:
        print(f"\n📤 Sending test email to {test_email}...")
        
        result = email_service.send_attendance_notification(
            test_email,
            "Test Teacher",
            "check_in",
            "2024-01-01 08:00 AM"
        )
        
        if result['success']:
            print("✅ Email sent successfully!")
            print(f"   Message: {result['message']}")
        else:
            print("❌ Email failed!")
            print(f"   Error: {result['error']}")
            return False
    
    return True

def test_sms_configuration():
    """Test SMS configuration"""
    print("\n" + "=" * 50)
    print("📱 TESTING SMS CONFIGURATION")
    print("=" * 50)
    
    # Check environment variables
    if not os.environ.get('RAPIDAPI_KEY'):
        print("❌ RAPIDAPI_KEY not configured")
        print("Please set RAPIDAPI_KEY in your .env file")
        return False
    
    print(f"✅ RapidAPI Key: {os.environ.get('RAPIDAPI_KEY')[:10]}...")
    print(f"✅ SMS Host: {os.environ.get('RAPIDAPI_SMS_HOST', 'sms-service.p.rapidapi.com')}")
    
    # Test SMS service connectivity
    print("\n🔍 Testing SMS service connectivity...")
    test_result = sms_service.test_sms_service()
    
    if test_result['success']:
        print("✅ SMS service is reachable")
        print(f"   Status Code: {test_result['status_code']}")
    else:
        print("❌ SMS service test failed")
        print(f"   Error: {test_result['error']}")
        print("\n💡 Possible solutions:")
        print("   1. Check your RapidAPI subscription")
        print("   2. Verify the SMS service host")
        print("   3. Ensure your API key is valid")
    
    # Test SMS sending
    test_phone = input("\nEnter test phone number (with country code, e.g., +1234567890) or press Enter to skip: ").strip()
    if test_phone:
        print(f"\n📤 Sending test SMS to {test_phone}...")
        
        result = sms_service.send_welcome_sms(test_phone, "Test Teacher")
        
        if result['success']:
            print("✅ SMS sent successfully!")
            print(f"   Message ID: {result.get('message_id', 'N/A')}")
            print(f"   Status: {result.get('status', 'N/A')}")
        else:
            print("❌ SMS failed!")
            print(f"   Error: {result['error']}")
            if 'endpoint' in result:
                print(f"   Endpoint: {result['endpoint']}")
            return False
    
    return True

def show_configuration_help():
    """Show configuration help"""
    print("\n" + "=" * 50)
    print("🔧 CONFIGURATION HELP")
    print("=" * 50)
    
    print("\n📧 EMAIL SETUP (Gmail):")
    print("1. Enable 2-Factor Authentication on your Gmail account")
    print("2. Generate an App Password:")
    print("   - Go to https://myaccount.google.com/")
    print("   - Security → 2-Step Verification → App passwords")
    print("   - Select 'Mail' and generate a new app password")
    print("3. Add to your .env file:")
    print("   SMTP_SERVER=smtp.gmail.com")
    print("   SMTP_PORT=587")
    print("   SMTP_USER=your-email@gmail.com")
    print("   SMTP_PASS=your-16-character-app-password")
    
    print("\n📱 SMS SETUP (RapidAPI):")
    print("1. Sign up at https://rapidapi.com")
    print("2. Subscribe to an SMS service:")
    print("   - SMS Service: sms-service.p.rapidapi.com")
    print("   - Text Local: textlocal.p.rapidapi.com")
    print("   - Twilio Alternative: twilio-sms.p.rapidapi.com")
    print("3. Add to your .env file:")
    print("   RAPIDAPI_KEY=your-rapidapi-key")
    print("   RAPIDAPI_SMS_HOST=sms-service.p.rapidapi.com")
    
    print("\n📄 SAMPLE .env FILE:")
    print("""
# Flask Configuration
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///attendance.db

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

# RapidAPI SMS Configuration
RAPIDAPI_KEY=your-rapidapi-key-here
RAPIDAPI_SMS_HOST=sms-service.p.rapidapi.com
    """)

def main():
    """Main test function"""
    print("🧪 NOTIFICATION TEST SCRIPT")
    print("This script will test your email and SMS configuration")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\n❌ .env file not found!")
        show_configuration_help()
        return
    
    # Test configurations
    email_ok = test_email_configuration()
    sms_ok = test_sms_configuration()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    if email_ok:
        print("✅ Email configuration is working")
    else:
        print("❌ Email configuration needs attention")
    
    if sms_ok:
        print("✅ SMS configuration is working")
    else:
        print("❌ SMS configuration needs attention")
    
    if not (email_ok and sms_ok):
        print("\n💡 Need help? Run this script again and follow the configuration guide above.")

if __name__ == "__main__":
    main() 