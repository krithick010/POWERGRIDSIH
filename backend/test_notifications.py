"""
Test script for notification and automation systems
"""

import asyncio
from notifications import get_notification_service
from automation import get_automation_engine

async def test_notifications():
    """Test notification service"""
    print("\n" + "="*60)
    print("Testing Notification Service")
    print("="*60)
    
    notification_service = get_notification_service()
    
    # Test ticket creation notification
    print("\n[Test 1] Ticket Creation Notification")
    await notification_service.notify_ticket_created(
        ticket_id="test-123-456",
        employee="Rajesh Kumar (PG12345)",
        subject="VPN connection issue",
        priority="high",
        category="network",
        assigned_team="Network Team"
    )
    print("✓ Ticket creation notification sent")
    
    # Test ticket update notification
    print("\n[Test 2] Ticket Update Notification")
    await notification_service.notify_ticket_updated(
        ticket_id="test-123-456",
        employee="Rajesh Kumar (PG12345)",
        subject="VPN connection issue",
        old_status="open",
        new_status="resolved"
    )
    print("✓ Ticket update notification sent")

def test_automation():
    """Test automation engine"""
    print("\n" + "="*60)
    print("Testing Automation Engine")
    print("="*60)
    
    automation_engine = get_automation_engine()
    
    # Test auto-resolve detection
    print("\n[Test 1] Auto-Resolve Detection")
    test_cases = [
        "I need to reset my password",
        "How do I setup VPN on my laptop?",
        "My laptop screen is broken",
    ]
    
    for text in test_cases:
        result = automation_engine.check_auto_resolve(text, "access")
        print(f"\nText: {text}")
        if result:
            print(f"  ✓ Can auto-resolve: {result['rule_name']}")
            print(f"  Resolution: {result['resolution'][:60]}...")
        else:
            print("  ✗ Cannot auto-resolve")
    
    # Test category suggestion
    print("\n[Test 2] Category Suggestion")
    test_texts = [
        "VPN not connecting",
        "Need software license",
        "Printer not working",
        "Cannot login to system",
    ]
    
    for text in test_texts:
        category = automation_engine.suggest_category(text)
        team = automation_engine.get_assigned_team(category)
        print(f"\nText: {text}")
        print(f"  Suggested Category: {category}")
        print(f"  Assigned Team: {team}")
    
    # Test SLA rules
    print("\n[Test 3] SLA Rules")
    for priority in ['high', 'medium', 'low']:
        sla = automation_engine.apply_sla_rules(priority)
        print(f"\nPriority: {priority.upper()}")
        print(f"  Response Time: {sla['response_time_hours']} hours")
        print(f"  Resolution Time: {sla['resolution_time_hours']} hours")
        print(f"  Description: {sla['description']}")

async def main():
    """Run all tests"""
    print("POWERGRID AI Ticketing System - Notification & Automation Tests")
    
    await test_notifications()
    test_automation()
    
    print("\n" + "="*60)
    print("Tests completed!")
    print("="*60)
    print("\nNote: Email/SMS may not be sent if credentials are not configured.")
    print("Check logs for notification status.")

if __name__ == "__main__":
    asyncio.run(main())
