#!/usr/bin/env python3
"""
Test script to verify the resolve ticket functionality
"""

import asyncio
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_resolve_ticket():
    """Test the complete resolve workflow"""
    print("🧪 Testing Resolve Ticket Functionality")
    print("=" * 50)
    
    # Step 1: Create a test ticket first
    print("1. Creating a test ticket...")
    ticket_data = {
        "message": "My computer won't turn on and I have an urgent presentation",
        "employee": "test.user@gmail.com (+1234567890)"
    }
    
    response = requests.post(f"{BASE_URL}/chatbot", json=ticket_data)
    if response.status_code != 200:
        print(f"❌ Failed to create ticket: {response.text}")
        return False
        
    chatbot_response = response.json()
    if not chatbot_response.get("ticket_created"):
        print("❌ No ticket was created by the chatbot")
        return False
        
    ticket_id = chatbot_response.get("ticket_id")
    print(f"✅ Ticket created successfully: {ticket_id}")
    
    # Step 2: Get the ticket to verify it's in 'open' status
    print("2. Verifying ticket status...")
    response = requests.get(f"{BASE_URL}/tickets/{ticket_id}")
    if response.status_code != 200:
        print(f"❌ Failed to get ticket: {response.text}")
        return False
        
    ticket = response.json()
    print(f"✅ Current ticket status: {ticket['status']}")
    
    # Step 3: Resolve the ticket
    print("3. Resolving the ticket...")
    resolve_data = {"status": "resolved"}
    response = requests.patch(f"{BASE_URL}/tickets/{ticket_id}/status", json=resolve_data)
    if response.status_code != 200:
        print(f"❌ Failed to resolve ticket: {response.text}")
        return False
        
    updated_ticket = response.json()
    print(f"✅ Ticket resolved successfully!")
    print(f"   - Ticket ID: {updated_ticket['id']}")
    print(f"   - New Status: {updated_ticket['status']}")
    print(f"   - Updated At: {updated_ticket['updated_at']}")
    
    # Step 4: Verify the ticket is actually resolved
    print("4. Verifying ticket is resolved...")
    response = requests.get(f"{BASE_URL}/tickets/{ticket_id}")
    if response.status_code != 200:
        print(f"❌ Failed to verify ticket: {response.text}")
        return False
        
    final_ticket = response.json()
    if final_ticket['status'] != 'resolved':
        print(f"❌ Ticket status is not resolved: {final_ticket['status']}")
        return False
        
    print(f"✅ Ticket is confirmed as resolved!")
    
    # Step 5: Test that we can fetch resolved tickets
    print("5. Testing filter for resolved tickets...")
    response = requests.get(f"{BASE_URL}/tickets?status=resolved&employee=test.user@gmail.com (+1234567890)")
    if response.status_code != 200:
        print(f"❌ Failed to fetch resolved tickets: {response.text}")
        return False
        
    resolved_tickets = response.json()
    found_our_ticket = any(t['id'] == ticket_id for t in resolved_tickets)
    if not found_our_ticket:
        print("❌ Our resolved ticket was not found in the resolved tickets filter")
        return False
        
    print(f"✅ Found {len(resolved_tickets)} resolved ticket(s) including ours")
    
    print("\n🎉 All resolve functionality tests passed!")
    print("✅ Ticket creation works")
    print("✅ Status update to 'resolved' works")
    print("✅ Database updates correctly")
    print("✅ Filtering by resolved status works")
    print("✅ SMS notification should be triggered (check logs)")
    
    return True

if __name__ == "__main__":
    try:
        success = test_resolve_ticket()
        if not success:
            exit(1)
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        exit(1)