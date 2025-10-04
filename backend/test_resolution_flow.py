#!/usr/bin/env python3
"""
Test complete ticket resolution flow with email + SMS
"""
import asyncio
from notifications import get_notification_service
from config import settings

async def test_resolution_flow():
    """Test the complete resolution notification flow"""
    print("Testing Complete Ticket Resolution Flow")
    print("="*50)
    
    print(f"📧 Email enabled: {settings.email_enabled}")
    print(f"📱 SMS enabled: {settings.sms_enabled}")
    print(f"🔧 Environment: {settings.ENVIRONMENT}")
    print()
    
    notification_service = get_notification_service()
    
    # Simulate a ticket resolution scenario
    ticket_data = {
        "ticket_id": "12345678-abcd-efgh-ijkl-123456789012",
        "employee": "sashreekbala864@gmail.com",  # User who will receive notifications
        "subject": "VPN connection issue - Unable to connect",
        "old_status": "in_progress", 
        "new_status": "resolved"
    }
    
    print("🎯 Simulating ticket resolution...")
    print(f"   Ticket: #{ticket_data['ticket_id'][:8]}")
    print(f"   User: {ticket_data['employee']}")
    print(f"   Subject: {ticket_data['subject']}")
    print(f"   Status: {ticket_data['old_status']} → {ticket_data['new_status']}")
    print()
    
    try:
        # This should send both email AND SMS (since status = resolved)
        await notification_service.notify_ticket_updated(
            ticket_id=ticket_data["ticket_id"],
            employee=ticket_data["employee"],
            subject=ticket_data["subject"],
            old_status=ticket_data["old_status"],
            new_status=ticket_data["new_status"]
        )
        
        print("✅ Resolution notification process completed!")
        print()
        print("Expected results:")
        print("📧 Email sent to: sashreekbala864@gmail.com")
        print("📱 SMS sent to: +919655524270 (verified number)")
        print("💌 Both notifications should mention ticket resolution")
        
    except Exception as e:
        print(f"❌ Error in resolution flow: {e}")

if __name__ == "__main__":
    asyncio.run(test_resolution_flow())