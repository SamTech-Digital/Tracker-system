# Email Integration Setup Guide

This guide explains how to set up email notifications for the Teachers Attendance System.

## 🚨 **IMMEDIATE FIXES FOR YOUR CURRENT ERRORS**

### **Email Error: "Username and Password not accepted"**

**Problem**: Gmail is rejecting your credentials because you're using a regular password instead of an app password.

**Solution**:
1. **Enable 2-Factor Authentication** on your Gmail account (samtechdigital30@gmail.com):
   - Go to [Google Account settings](https://myaccount.google.com/)
   - Security → 2-Step Verification → Turn it on
2. **Generate an App Password**:
   - Go to [Google Account settings](https://myaccount.google.com/)
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and generate a new 16-character app password
3. **Update your .env file**:
   ```bash
   SMTP_USER=samtechdigital30@gmail.com
   SMTP_PASS=your-16-character-app-password  # Use the app password, not your regular password
   ```

## 🧪 **Test Your Configuration**

Run the test script to verify your setup:

```bash
python test_notifications.py
```

This script will:
- Check your environment variables
- Test email connectivity
- Send test messages (optional)

## 📧 Email Configuration

### Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
3. **Configure Environment Variables**:
   ```bash
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASS=your-app-password
   FROM_EMAIL=your-email@gmail.com
   FROM_NAME=Teachers Attendance System
   ```

### Other Email Providers

For other providers like Outlook, Yahoo, etc., adjust the SMTP settings accordingly:
- **Outlook**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`

## 📱 RapidAPI SMS Configuration

### 1. Get RapidAPI Key

1. Sign up at [RapidAPI](https://rapidapi.com)
2. Subscribe to an SMS service (recommended services):
   - **Text Local**: `textlocal.p.rapidapi.com` (most reliable)
   - **SMS Service**: `sms-service.p.rapidapi.com`
   - **Twilio Alternative**: `twilio-sms.p.rapidapi.com`

### 2. Configure Environment Variables

```bash
RAPIDAPI_KEY=your-rapidapi-key-here
RAPIDAPI_SMS_HOST=textlocal.p.rapidapi.com  # Try this first
```

### 3. Test SMS Service

The system will automatically test the SMS service when adding a teacher. Check the notification status on the teacher creation page.

## 🔧 Environment Variables Summary

Create a `.env` file in your project root with these variables:

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///attendance.db

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=samtechdigital30@gmail.com
SMTP_PASS=your-16-character-app-password
FROM_EMAIL=samtechdigital30@gmail.com
FROM_NAME=Teachers Attendance System

// SMS setup instructions removed
  2. Security → 2-Step Verification → App passwords
  3. Select "Mail" and generate new password
  4. Use the 16-character app password in your .env file

#### "Authentication failed" Error
- **Cause**: 2-Factor Authentication not enabled
- **Solution**: Enable 2FA on your Gmail account first

#### "Connection refused" Error
- **Cause**: Wrong SMTP settings
- **Solution**: Use these settings for Gmail:
  ```bash
  SMTP_SERVER=smtp.gmail.com
  SMTP_PORT=587
  ```

### SMS Issues

#### "API request failed with status 404" Error
- **Cause**: Wrong SMS service host or not subscribed
- **Solutions**:
  1. **Try different SMS service**:
     ```bash
     RAPIDAPI_SMS_HOST=textlocal.p.rapidapi.com
     ```
  2. **Check RapidAPI subscription**:
     - Ensure you're subscribed to the SMS service
     - Verify your API key is correct
  3. **Test with different service**:
     ```bash
     RAPIDAPI_SMS_HOST=twilio-sms.p.rapidapi.com
     ```

#### "API key not valid" Error
- **Cause**: Invalid or expired RapidAPI key
- **Solution**: Generate a new API key from RapidAPI dashboard

#### "Service not available" Error
- **Cause**: SMS service is down or not available in your region
- **Solution**: Try a different SMS service provider

## 📞 Alternative SMS Services

If RapidAPI SMS services don't work, consider these alternatives:

### 1. Twilio (Direct Integration)
```python
# Add to requirements.txt
twilio==8.10.0

# Environment variables
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=your-twilio-number
```

### 2. AWS SNS
```python
# Add to requirements.txt
boto3==1.26.0

# Environment variables
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
```

### 3. SendGrid SMS
```python
# Add to requirements.txt
sendgrid==6.9.0

# Environment variables
SENDGRID_API_KEY=your-api-key
SENDGRID_FROM_NUMBER=your-sendgrid-number
```

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Use app passwords instead of regular passwords for email
- Keep your RapidAPI key secure
- Regularly rotate your API keys

## 🆘 Support

For issues with:
- **Email**: Check your email provider's SMTP settings
- **SMS**: Contact RapidAPI support for your specific SMS service
- **System**: Check the application logs for detailed error messages
- **Testing**: Run `python test_notifications.py` for diagnostics

## 📋 Quick Checklist

- [ ] Gmail 2-Factor Authentication enabled
- [ ] Gmail App Password generated and configured
- [ ] RapidAPI account created
- [ ] SMS service subscribed to
- [ ] RapidAPI key configured
- [ ] .env file created with all variables
- [ ] Test script run successfully
- [ ] Application restarted after configuration changes 