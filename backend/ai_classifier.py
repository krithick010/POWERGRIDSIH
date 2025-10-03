"""
AI-powered ticket classification using Hugging Face models
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class TicketClassifier:
    """
    Ticket classifier using fine-tuned or zero-shot classification models
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        # Initialize models
        self._init_classifier()
        
        # Auto-resolve patterns - ENHANCED with greetings
        self.auto_resolve_patterns = {
            "greeting": {
                "keywords": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
                "message": "Hello! I'm here to help with your IT support needs. Please describe your issue and I'll assist you or create a support ticket."
            },
            "thanks": {
                "keywords": ["thank you", "thanks", "thx", "appreciate"],
                "message": "You're welcome! Is there anything else I can help you with?"
            },
            "test": {
                "keywords": ["test", "testing", "check"],
                "message": "System is working properly! How can I assist you with your IT support needs?"
            },
            "password_reset": {
                "keywords": ["reset password", "forgot password", "password reset", "change password"],
                "message": "I can help you reset your password. Please visit our self-service portal at https://password.powergrid.in or contact your system administrator."
            },
            "vpn_setup": {
                "keywords": ["vpn setup", "vpn install", "vpn connection", "vpn download"],
                "message": "For VPN setup, please download the client from https://vpn.powergrid.in/downloads and follow the installation guide. If you need further assistance, I can create a support ticket."
            },
            "email_mobile": {
                "keywords": ["email on mobile", "mobile email", "phone email setup"],
                "message": "For mobile email configuration, please check our setup guide in the knowledge base. I can provide step-by-step instructions or create a support ticket if needed."
            }
        }
        
        logger.info("Classifier initialized successfully!")
    
    def _init_classifier(self):
        # Initialize zero-shot classification pipeline for categories
        logger.info("Loading zero-shot classification model...")
        self.category_classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=0 if self.device == "cuda" else -1
        )
        
        # Category labels
        self.category_labels = [
            "network and connectivity issues",
            "access and authentication problems",
            "hardware and equipment issues",
            "software and application issues",
            "other IT support"
        ]
        
        # Priority keywords for rule-based priority detection
        self.high_priority_keywords = [
            "urgent", "critical", "emergency", "down", "not working", 
            "broken", "crashed", "immediately", "asap", "production"
        ]
        
        self.medium_priority_keywords = [
            "soon", "important", "need", "required", "issue", 
            "problem", "help", "support"
        ]
    
    def classify_category(self, text: str) -> Tuple[str, float]:
        """
        Classify ticket into category using zero-shot classification
        Returns: (category, confidence)
        """
        try:
            result = self.category_classifier(text, self.category_labels)
            
            # Map label to category
            label_to_category = {
                "network and connectivity issues": "network",
                "access and authentication problems": "access",
                "hardware and equipment issues": "hardware",
                "software and application issues": "software",
                "other IT support": "other"
            }
            
            top_label = result['labels'][0]
            confidence = result['scores'][0]
            category = label_to_category.get(top_label, "other")
            
            logger.info(f"Classified as '{category}' with confidence {confidence:.2f}")
            return category, confidence
        
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return "other", 0.5
    
    def classify_priority(self, text: str) -> Tuple[str, float]:
        """
        Classify ticket priority using keyword matching
        Returns: (priority, confidence)
        """
        text_lower = text.lower()
        
        # Check for high priority keywords
        high_matches = sum(1 for keyword in self.high_priority_keywords if keyword in text_lower)
        medium_matches = sum(1 for keyword in self.medium_priority_keywords if keyword in text_lower)
        
        if high_matches > 0:
            confidence = min(0.7 + (high_matches * 0.1), 0.95)
            return "high", confidence
        elif medium_matches > 0:
            confidence = min(0.6 + (medium_matches * 0.05), 0.85)
            return "medium", confidence
        else:
            return "low", 0.6
    
    def check_auto_resolve(self, text: str) -> Tuple[bool, str]:
        """
        Check if the issue can be auto-resolved
        Returns: (can_auto_resolve, resolution_message)
        """
        text_lower = text.lower()
        
        for pattern_name, pattern_data in self.auto_resolve_patterns.items():
            for keyword in pattern_data["keywords"]:
                if keyword in text_lower:
                    logger.info(f"Auto-resolve pattern matched: {pattern_name}")
                    return True, pattern_data["message"]
        
        return False, ""
    
    def classify(self, text: str) -> Dict:
        """
        Full classification: category, priority, and auto-resolve check
        """
        category, cat_confidence = self.classify_category(text)
        priority, pri_confidence = self.classify_priority(text)
        auto_resolve, resolution_message = self.check_auto_resolve(text)
        
        # Average confidence
        avg_confidence = (cat_confidence + pri_confidence) / 2
        
        return {
            "category": category,
            "priority": priority,
            "confidence": round(avg_confidence, 2),
            "auto_resolve": auto_resolve,
            "resolution_message": resolution_message if auto_resolve else None
        }

# Global classifier instance
_classifier = None

def get_classifier() -> TicketClassifier:
    """Get or create classifier instance (singleton pattern)"""
    global _classifier
    if _classifier is None:
        _classifier = TicketClassifier()
    return _classifier
