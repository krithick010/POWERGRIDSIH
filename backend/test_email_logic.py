#!/usr/bin/env python3
"""
Test email extraction logic for real users
"""
import os
from notifications import get_notification_service
from config import settings

def test_email_extraction():
    """Test email extraction logic"""
    print("Testing email extraction logic")
    print("="*50)
    
    # Print current settings
    print(f"ENVIRONMENT: {settings.ENVIRONMENT}")
    print(f"TEST_NOTIFICATION_EMAIL: {settings.TEST_NOTIFICATION_EMAIL}")
    print(f"CHATBOT_FROM: {settings.CHATBOT_FROM}")
    print()
    
    notification_service = get_notification_service()
    
    # Test cases with different employee formats
    test_cases = [
        "user@gmail.com",  # Direct email
        "john.doe@company.com",  # Corporate email
        "Jane Smith (EMP123)",  # Name with ID
        "Bob Wilson",  # Just name
    ]
    
    print("Email extraction results:")
    print("-" * 30)
    
    for employee in test_cases:
        extracted = notification_service._extract_email(employee)
        print(f"Input: '{employee}' -> Email: '{extracted}'")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_email_extraction()