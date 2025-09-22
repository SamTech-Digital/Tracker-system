import requests
import os
from typing import Dict, Any, Optional

class RapidAPISMS:
    """RapidAPI SMS integration utility"""
    
    def __init__(self):
        self.api_key = os.environ.get('RAPIDAPI_KEY')
        self.api_host = os.environ.get('RAPIDAPI_SMS_HOST', 'sms-service.p.rapidapi.com')
        self.base_url = f"https://{self.api_host}"
        
        # Common RapidAPI SMS service configurations
        self.sms_services = {
            'sms-service.p.rapidapi.com': {
                'endpoint': '/send',
                'payload_keys': {'to': 'phone', 'message': 'text', 'from': 'sender'}
            },
            'textlocal.p.rapidapi.com': {
                'endpoint': '/send',
                'payload_keys': {'to': 'numbers', 'message': 'message', 'from': 'sender'}
            },
            'twilio-sms.p.rapidapi.com': {
                'endpoint': '/send',
                'payload_keys': {'to': 'To', 'message': 'Body', 'from': 'From'}
            },
            'nexmo-sms.p.rapidapi.com': {
                'endpoint': '/send',
                'payload_keys': {'to': 'to', 'message': 'text', 'from': 'from'}
            }
        }
        
    def send_sms(self, phone_number: str, message: str, sender_name: str = "TeacherTracker") -> Dict[str, Any]:
        """
        Send SMS using RapidAPI SMS service
        
        Args:
            phone_number: Recipient phone number (with country code)
            message: SMS message content
            sender_name: Sender name (optional)
            
        Returns:
            Dict containing success status and response details
        """
        if not self.api_key:
            return {
                'success': False,
                'error': 'RAPIDAPI_KEY not configured in environment variables'
            }
        
        # Get service configuration
        service_config = self.sms_services.get(self.api_host, {
            'endpoint': '/send',
            'payload_keys': {'to': 'to', 'message': 'message', 'from': 'from'}
        })
        
        headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': self.api_host,
            'Content-Type': 'application/json'
        }
        
        # Build payload based on service configuration
        payload_keys = service_config['payload_keys']
        payload = {
            payload_keys['to']: phone_number,
            payload_keys['message']: message,
            payload_keys['from']: sender_name
        }
        
        # Add additional required fields for specific services
        if 'textlocal' in self.api_host:
            payload['apikey'] = self.api_key
        elif 'twilio' in self.api_host:
            payload['AccountSid'] = os.environ.get('TWILIO_ACCOUNT_SID', '')
            payload['AuthToken'] = os.environ.get('TWILIO_AUTH_TOKEN', '')
        
        try:
            response = requests.post(
                f"{self.base_url}{service_config['endpoint']}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'message_id': result.get('message_id') or result.get('sid') or result.get('id'),
                    'status': result.get('status') or 'sent',
                    'response': result
                }
            else:
                return {
                    'success': False,
                    'error': f'API request failed with status {response.status_code}',
                    'response': response.text,
                    'endpoint': f"{self.base_url}{service_config['endpoint']}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}',
                'endpoint': f"{self.base_url}{service_config['endpoint']}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'endpoint': f"{self.base_url}{service_config['endpoint']}"
            }
    
    def test_sms_service(self) -> Dict[str, Any]:
        """
        Test SMS service connectivity
        
        Returns:
            Dict containing test results
        """
        if not self.api_key:
            return {
                'success': False,
                'error': 'RAPIDAPI_KEY not configured'
            }
        
        headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': self.api_host
        }
        
        try:
            # Try to get service info or test endpoint
            response = requests.get(
                f"{self.base_url}/",
                headers=headers,
                timeout=10
            )
            
            return {
                'success': True,
                'status_code': response.status_code,
                'service_info': response.text[:200] if response.text else 'No response body'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Service test failed: {str(e)}'
            }
    
    def send_welcome_sms(self, phone_number: str, teacher_name: str) -> Dict[str, Any]:
        """
        Send welcome SMS to newly added teacher
        
        Args:
            phone_number: Teacher's phone number
            teacher_name: Teacher's name
            
        Returns:
            Dict containing success status and response details
        """
        message = f"Welcome {teacher_name}! You have been successfully added to the Teachers Attendance System. Your QR code has been sent to your email. Please use it to check in and out for attendance."
        
        return self.send_sms(phone_number, message)
    
    def send_attendance_reminder(self, phone_number: str, teacher_name: str, reminder_type: str = "check_in") -> Dict[str, Any]:
        """
        Send attendance reminder SMS
        
        Args:
            phone_number: Teacher's phone number
            teacher_name: Teacher's name
            reminder_type: Type of reminder ("check_in" or "check_out")
            
        Returns:
            Dict containing success status and response details
        """
        if reminder_type == "check_in":
            message = f"Good morning {teacher_name}! Don't forget to check in using your QR code when you arrive at work."
        elif reminder_type == "check_out":
            message = f"Good evening {teacher_name}! Please remember to check out using your QR code before leaving."
        else:
            message = f"Hello {teacher_name}! This is a reminder to use your QR code for attendance tracking."
        
        return self.send_sms(phone_number, message)

# Global instance
sms_service = RapidAPISMS() 