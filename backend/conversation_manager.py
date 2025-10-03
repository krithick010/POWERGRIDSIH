from typing import Dict, List, Optional
from datetime import datetime, timedelta

class ConversationManager:
    def __init__(self):
        # Store conversation history per user
        self.conversations = {}
        self.context_timeout = timedelta(minutes=30)
    
    def get_context(self, employee: str) -> Optional[Dict]:
        """Get conversation context for user"""
        if employee in self.conversations:
            last_interaction = self.conversations[employee].get("last_interaction")
            if last_interaction and datetime.now() - last_interaction < self.context_timeout:
                return self.conversations[employee]
        return None
    
    def update_context(self, employee: str, message: str, response: str, intent: str):
        """Update conversation context"""
        if employee not in self.conversations:
            self.conversations[employee] = {
                "history": [],
                "current_issue": None,
                "tickets_created": []
            }
        
        self.conversations[employee]["history"].append({
            "message": message,
            "response": response,
            "intent": intent,
            "timestamp": datetime.now()
        })
        self.conversations[employee]["last_interaction"] = datetime.now()
        
        # Keep only last 10 interactions
        if len(self.conversations[employee]["history"]) > 10:
            self.conversations[employee]["history"] = self.conversations[employee]["history"][-10:]
    
    def generate_contextual_response(self, employee: str, message: str, intent: str) -> str:
        """Generate response based on conversation context"""
        context = self.get_context(employee)
        
        if not context:
            # First interaction
            return self._get_first_time_response(intent)
        
        # Returning user
        if intent == "greeting":
            recent_tickets = len(context.get("tickets_created", []))
            if recent_tickets > 0:
                return f"Welcome back! I see you've created {recent_tickets} tickets recently. How can I help you today?"
            else:
                return "Hello again! What can I help you with today?"
        
        return self._get_default_response(intent)
    
    def _get_first_time_response(self, intent: str) -> str:
        responses = {
            "greeting": "Hello! I'm your AI IT support assistant. I can help you with technical issues, search our knowledge base, or create support tickets. What's on your mind?",
            "status_inquiry": "I'm doing great, thank you! I'm here to help with your IT support needs. What can I assist you with?",
            "question_about_bot": "I'm an AI assistant specialized in IT support for POWERGRID. I can help resolve common issues, search our knowledge base, and create tickets for complex problems. How can I help you today?"
        }
        return responses.get(intent, "Hello! I'm your IT support assistant. How can I help you today?")