#!/usr/bin/env python3
"""
Debug SMS Issues
Simple script to test SMS functionality
"""

import os
from utils.sms_utils import RapidAPISMS

def debug_sms():
    """Debug SMS functionality"""
    print("🔍 SMS DEBUG SCRIPT")
    print("=" * 50)
    
    # Initialize SMS service
    sms_service = RapidAPISMS()
    
    print("📋 CONFIGURATION:")
    print(f"  API Key: {'*' * len(sms_service.api_key) if sms_service.api_key else 'NOT SET'}")
    print(f"  API Host: {sms_service.api_host}")
    print(f"  Base URL: {sms_service.base_url}")
    
    if not sms_service.api_key:
        print("❌ RAPIDAPI_KEY not configured")
        return
    
    # Test service connectivity
    print("\n🔍 TESTING SERVICE CONNECTIVITY:")
    test_result = sms_service.test_sms_service()
    print(f"  Success: {test_result['success']}")
    if test_result['success']:
        print(f"  Status Code: {test_result.get('status_code', 'N/A')}")
        print(f"  Service Info: {test_result.get('service_info', 'N/A')}")
    else:
        print(f"  Error: {test_result['error']}")
    
    # Test with a sample phone number (you can change this)
    test_phone = "+2348012345678"  # Example Nigerian number
    test_message = "Test SMS from Teachers Attendance System"
    
    print(f"\n📤 TESTING SMS SEND:")
    print(f"  To: {test_phone}")
    print(f"  Message: {test_message}")
    print(f"  Service: {sms_service.api_host}")
    
    # Send test SMS
    result = sms_service.send_sms(test_phone, test_message, "TeacherTracker")
    
    print(f"\n📊 RESULT:")
    print(f"  Success: {result['success']}")
    
    if result['success']:
        print(f"  Message ID: {result.get('message_id', 'N/A')}")
        print(f"  Status: {result.get('status', 'N/A')}")
        print("✅ SMS sent successfully!")
    else:
        print(f"  Error: {result['error']}")
        if 'endpoint' in result:
            print(f"  Endpoint: {result['endpoint']}")
        if 'response' in result:
            print(f"  API Response: {result['response']}")
    
    # Show service configuration
    print(f"\n🔧 SERVICE CONFIGURATION:")
    service_config = sms_service.sms_services.get(sms_service.api_host, {
        'endpoint': '/send',
        'payload_keys': {'to': 'to', 'message': 'message', 'from': 'from'}
    })
    print(f"  Endpoint: {service_config['endpoint']}")
    print(f"  Payload Keys: {service_config['payload_keys']}")
    
    # Check if it's a 404 error
    if not result['success'] and '404' in str(result.get('error', '')):
        print(f"\n💡 404 ERROR DETECTED - POSSIBLE SOLUTIONS:")
        print("   1. Check if you're subscribed to the SMS service on RapidAPI")
        print("   2. Try a different SMS service:")
        print("      - textlocal.p.rapidapi.com")
        print("      - twilio-sms.p.rapidapi.com")
        print("      - nexmo-sms.p.rapidapi.com")
        print("   3. Verify your API key is valid")
        print("   4. Check if the service endpoint exists")

if __name__ == "__main__":
    debug_sms() 