#!/usr/bin/env python3
"""
Test Twilio SMS functionality
"""
import os
import asyncio
from notifications import get_notification_service
from config import settings

async def test_sms():
    """Test SMS sending"""
    print("Testing Twilio SMS functionality")
    print("="*50)
    
    # Print current SMS settings
    print(f"SMS Enabled: {settings.sms_enabled}")
    print(f"TWILIO_ACCOUNT_SID: {'Set' if settings.TWILIO_ACCOUNT_SID else 'Not set'}")
    print(f"TWILIO_AUTH_TOKEN: {'Set' if settings.TWILIO_AUTH_TOKEN else 'Not set'}")
    print(f"TWILIO_PHONE_NUMBER: {settings.TWILIO_PHONE_NUMBER}")
    print()
    
    if not settings.sms_enabled:
        print("❌ SMS is not enabled. Please set TWILIO credentials.")
        return
    
    notification_service = get_notification_service()
    
    # Test SMS sending
    print("📱 Testing SMS notification...")
    
    # Test phone extraction
    test_employee = "sashreekbala864@gmail.com"  # This should return a test phone number
    # Use the phone number you used to sign up for Twilio (should be verified)
    phone = "+919655524270"  # This should be the number you verified when signing up
    print(f"Testing SMS to verified number: {phone}")
    print("Note: This should be the phone number you used to sign up for Twilio")
    
    if phone:
        # Test sending SMS
        try:
            success = await notification_service.sms_service.send_sms(
                phone, 
                "🚀 POWERGRID IT: Test SMS from your ticketing system!"
            )
            if success:
                print("✅ SMS sent successfully!")
            else:
                print("❌ SMS sending failed")
        except Exception as e:
            print(f"❌ SMS error: {e}")
    else:
        print("❌ No phone number found for testing")

if __name__ == "__main__":
    asyncio.run(test_sms())