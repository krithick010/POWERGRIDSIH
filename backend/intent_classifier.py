from transformers import pipeline
import re
from typing import Dict, List, Tuple

class AdvancedIntentClassifier:
    def __init__(self):
        # Use a more sophisticated NLP model for intent classification
        self.intent_classifier = pipeline(
            "text-classification", 
            model="microsoft/DialoGPT-medium"  # Better conversational model
        )
        
        # Multi-turn conversation patterns
        self.conversation_patterns = {
            "greeting": [r"\b(hi|hello|hey|good (morning|afternoon|evening))\b"],
            "farewell": [r"\b(bye|goodbye|see you|thanks|thank you)\b"],
            "question_about_bot": [r"\b(who are you|what (do you do|can you do)|help me understand)\b"],
            "status_inquiry": [r"\b(how are you|what's up|how's it going)\b"],
            "password_issue": [r"\b(password|forgot password|reset password|can't log in|login issue)\b"],
            "network_issue": [r"\b(internet|wifi|network|connection|vpn|slow)\b"],
            "hardware_issue": [r"\b(computer|laptop|printer|mouse|keyboard|screen|monitor)\b"],
            "software_issue": [r"\b(software|application|program|install|update|error)\b"],
            "email_issue": [r"\b(email|outlook|gmail|mail|smtp)\b"],
            "access_issue": [r"\b(access|permission|folder|drive|file)\b"]
        }
    
    def classify_intent(self, text: str) -> Dict[str, any]:
        """Classify user intent with confidence score"""
        text_lower = text.lower().strip()
        
        # Check for specific patterns first
        for intent, patterns in self.conversation_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return {
                        "intent": intent,
                        "confidence": 0.9,
                        "is_it_related": intent not in ["greeting", "farewell", "question_about_bot", "status_inquiry"]
                    }
        
        # Fallback classification
        if len(text_lower) < 10:
            return {"intent": "greeting", "confidence": 0.7, "is_it_related": False}
        
        return {"intent": "it_support", "confidence": 0.8, "is_it_related": True}