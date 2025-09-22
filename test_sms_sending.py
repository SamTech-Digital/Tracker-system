#!/usr/bin/env python3
"""
Test SMS Sending Script
Tests SMS functionality with detailed debugging
"""

import os
import sys
from utils.sms_utils import RapidAPISMS
import requests

def test_sms_with_debug():
    """Test SMS sending with detailed debugging information"""
    print("📱 SMS SENDING TEST WITH DEBUG")
    print("=" * 50)
    
    # Initialize SMS service
    sms_service = RapidAPISMS()
    
    # Check configuration
    print("🔍 CONFIGURATION CHECK:")
    print(f"  API Key: {'*' * len(sms_service.api_key) if sms_service.api_key else 'NOT SET'}")
    print(f"  API Host: {sms_service.api_host}")
    print(f"  Base URL: {sms_service.base_url}")
    
    if not sms_service.api_key:
        print("❌ RAPIDAPI_KEY not configured")
        return False
    
    # Get service configuration
    service_config = sms_service.sms_services.get(sms_service.api_host, {
        'endpoint': '/send',
        'payload_keys': {'to': 'to', 'message': 'message', 'from': 'from'}
    })
    
    print(f"  Endpoint: {service_config['endpoint']}")
    print(f"  Payload Keys: {service_config['payload_keys']}")
    
    # Test phone number
    test_phone = input("\n📞 Enter test phone number (with country code, e.g., +2348012345678): ").strip()
    if not test_phone:
        print("❌ No phone number provided")
        return False
    
    # Test message
    test_message = "Test SMS from Teachers Attendance System. If you receive this, SMS is working!"
    
    print(f"\n📤 SENDING TEST SMS:")
    print(f"  To: {test_phone}")
    print(f"  Message: {test_message}")
    print(f"  Service: {sms_service.api_host}")
    
    # Send SMS with detailed debugging
    result = sms_service.send_sms(test_phone, test_message, "TeacherTracker")
    
    print(f"\n📊 RESULT:")
    print(f"  Success: {result['success']}")
    
    if result['success']:
        print(f"  Message ID: {result.get('message_id', 'N/A')}")
        print(f"  Status: {result.get('status', 'N/A')}")
        print("✅ SMS sent successfully!")
        
        # Show full response for debugging
        if 'response' in result:
            print(f"\n📋 FULL API RESPONSE:")
            print(f"  {result['response']}")
    else:
        print(f"  Error: {result['error']}")
        if 'endpoint' in result:
            print(f"  Endpoint: {result['endpoint']}")
        if 'response' in result:
            print(f"  API Response: {result['response']}")
        
        # Additional debugging for common issues
        print(f"\n🔧 DEBUGGING INFO:")
        print(f"  Status Code: {result.get('status_code', 'N/A')}")
        print(f"  Endpoint Used: {result.get('endpoint', 'N/A')}")
        
        # Check if it's a 404 error
        if '404' in str(result.get('error', '')):
            print("\n💡 404 Error Solutions:")
            print("   1. Check if you're subscribed to the SMS service on RapidAPI")
            print("   2. Try a different SMS service:")
            print("      - textlocal.p.rapidapi.com")
            print("      - twilio-sms.p.rapidapi.com")
            print("      - nexmo-sms.p.rapidapi.com")
            print("   3. Verify your API key is valid")
    
    return result['success']

def test_different_sms_services():
    """Test different SMS services to find one that works"""
    print("\n🔄 TESTING DIFFERENT SMS SERVICES")
    print("=" * 50)
    
    services = [
        'textlocal.p.rapidapi.com',
        'sms-service.p.rapidapi.com',
        'twilio-sms.p.rapidapi.com',
        'nexmo-sms.p.rapidapi.com'
    ]
    
    test_phone = input("📞 Enter test phone number (with country code): ").strip()
    if not test_phone:
        print("❌ No phone number provided")
        return
    
    test_message = "Testing SMS service compatibility"
    
    for service in services:
        print(f"\n🧪 Testing {service}...")
        
        # Temporarily change the service
        original_host = os.environ.get('RAPIDAPI_SMS_HOST')
        os.environ['RAPIDAPI_SMS_HOST'] = service
        
        # Create new SMS service instance
        sms_service = RapidAPISMS()
        result = sms_service.send_sms(test_phone, test_message, "Test")
        
        if result['success']:
            print(f"✅ {service} - WORKING!")
            print(f"   Message ID: {result.get('message_id', 'N/A')}")
            print(f"   Status: {result.get('status', 'N/A')}")
            
            # Restore original host
            if original_host:
                os.environ['RAPIDAPI_SMS_HOST'] = original_host
            else:
                os.environ.pop('RAPIDAPI_SMS_HOST', None)
            
            print(f"\n💡 RECOMMENDATION: Use {service} for your SMS service")
            print(f"   Set RAPIDAPI_SMS_HOST={service} in your .env file")
            return True
        else:
            print(f"❌ {service} - Failed: {result['error']}")
        
        # Restore original host
        if original_host:
            os.environ['RAPIDAPI_SMS_HOST'] = original_host
        else:
            os.environ.pop('RAPIDAPI_SMS_HOST', None)
    
    print("\n❌ All SMS services failed. Please check your RapidAPI subscription.")
    return False

def main():
    """Main function"""
    print("📱 SMS TESTING TOOL")
    print("=" * 50)
    print("This tool will help you test and debug SMS functionality")
    print()
    
    choice = input("Choose test type:\n1. Test current SMS service\n2. Test different SMS services\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        success = test_sms_with_debug()
        if success:
            print("\n✅ SMS is working correctly!")
        else:
            print("\n❌ SMS needs configuration. Try option 2 to test different services.")
    elif choice == "2":
        test_different_sms_services()
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main() 