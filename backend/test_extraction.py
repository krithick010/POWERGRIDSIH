#!/usr/bin/env python3
"""
Test email and phone extraction with new frontend format
"""
import os
from notifications import get_notification_service
from config import settings

def test_extraction():
    """Test email and phone extraction logic"""
    print("Testing Email and Phone Extraction")
    print("="*50)
    
    notification_service = get_notification_service()
    
    # Test cases with new frontend format: "email (phone)"
    test_cases = [
        "user@gmail.com (+919876543210)",
        "sashreekbala864@gmail.com (+918825686207)",
        "john.doe@company.com (9876543210)",
        "jane.smith@gmail.com (+1-234-567-8900)",
        "simple@gmail.com (8765432109)",
        # Fallback case
        "test.user@gmail.com",
    ]
    
    print("Extraction Results:")
    print("-" * 60)
    print(f"{'Input':<35} {'Email':<25} {'Phone'}")
    print("-" * 60)
    
    for employee in test_cases:
        email = notification_service._extract_email(employee)
        phone = notification_service._extract_phone(employee)
        print(f"{employee:<35} {email:<25} {phone or 'None'}")
    
    print("\n" + "="*50)
    print("✅ Extraction test completed!")
    print("\nExpected behavior:")
    print("- Email should be extracted from before '(' or full string if no '('")
    print("- Phone should be extracted from inside '()' and formatted with country code")
    print("- Indian numbers (10 digits starting with 9,8,7,6) get +91 prefix")
    print("- Other numbers get + prefix if not already present")

if __name__ == "__main__":
    test_extraction()