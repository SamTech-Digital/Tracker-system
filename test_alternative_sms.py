#!/usr/bin/env python3
"""
Test Alternative SMS Services
Tests different RapidAPI SMS services to find one that works
"""

import os
from utils.sms_utils import RapidAPISMS

def test_alternative_services():
    """Test different SMS services"""
    print("🔄 TESTING ALTERNATIVE SMS SERVICES")
    print("=" * 50)
    
    services = [
        'sms-service.p.rapidapi.com',
        'twilio-sms.p.rapidapi.com',
        'nexmo-sms.p.rapidapi.com'
    ]
    
    test_phone = "+2348012345678"  # Example number
    test_message = "Testing SMS service compatibility"
    
    working_service = None
    
    for service in services:
        print(f"\n🧪 Testing {service}...")
        
        # Temporarily change the service
        original_host = os.environ.get('RAPIDAPI_SMS_HOST')
        os.environ['RAPIDAPI_SMS_HOST'] = service
        
        # Create new SMS service instance
        sms_service = RapidAPISMS()
        
        # Test connectivity first
        test_result = sms_service.test_sms_service()
        print(f"  Connectivity: {'✅' if test_result['success'] else '❌'}")
        
        if test_result['success']:
            # Try sending SMS
            result = sms_service.send_sms(test_phone, test_message, "Test")
            print(f"  SMS Send: {'✅' if result['success'] else '❌'}")
            
            if result['success']:
                print(f"  ✅ {service} - WORKING!")
                print(f"     Message ID: {result.get('message_id', 'N/A')}")
                working_service = service
                break
            else:
                print(f"     Error: {result['error']}")
        else:
            print(f"     Error: {test_result['error']}")
        
        # Restore original host
        if original_host:
            os.environ['RAPIDAPI_SMS_HOST'] = original_host
        else:
            os.environ.pop('RAPIDAPI_SMS_HOST', None)
    
    if working_service:
        print(f"\n💡 RECOMMENDATION: Use {working_service}")
        print(f"   Update your .env file:")
        print(f"   RAPIDAPI_SMS_HOST={working_service}")
    else:
        print(f"\n❌ All alternative services failed.")
        print(f"   You may need to:")
        print(f"   1. Subscribe to a different SMS service on RapidAPI")
        print(f"   2. Check your RapidAPI subscription limits")
        print(f"   3. Wait for rate limits to reset")

if __name__ == "__main__":
    test_alternative_services() 