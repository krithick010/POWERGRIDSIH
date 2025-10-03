"""
Automation rules for ticket handling
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class AutomationEngine:
    """
    Automation engine for handling tickets based on rules
    """
    
    def __init__(self):
        # Define automation rules
        self.auto_resolve_rules = {
            'password_reset': {
                'keywords': ['password reset', 'reset password', 'forgot password', 'password expired'],
                'category': 'access',
                'resolution': 'Password reset instructions sent. Visit https://password.powergrid.in',
                'kb_article_id': None  # Link to KB article if available
            },
            'vpn_setup': {
                'keywords': ['vpn setup', 'vpn install', 'vpn download', 'vpn access'],
                'category': 'network',
                'resolution': 'VPN setup guide provided. Download from https://vpn.powergrid.in/downloads',
                'kb_article_id': None
            },
            'email_mobile': {
                'keywords': ['email on mobile', 'mobile email setup', 'configure email phone'],
                'category': 'software',
                'resolution': 'Email configuration guide sent. Check Knowledge Base for detailed steps.',
                'kb_article_id': None
            }
        }
        
        # Priority escalation rules
        self.escalation_rules = {
            'high_priority_keywords': [
                'production down', 'system down', 'critical', 'emergency',
                'urgent', 'not working', 'broken', 'crashed'
            ],
            'escalation_time': {
                'high': 2,      # 2 hours
                'medium': 24,   # 24 hours
                'low': 72       # 72 hours
            }
        }
        
        # Auto-assignment rules based on category
        self.assignment_rules = {
            'network': {
                'team': 'Network Team',
                'keywords': ['vpn', 'network', 'connection', 'internet', 'wifi', 'lan']
            },
            'access': {
                'team': 'IT Support',
                'keywords': ['password', 'login', 'access', 'permission', 'authentication', 'account']
            },
            'hardware': {
                'team': 'Hardware Support',
                'keywords': ['laptop', 'desktop', 'printer', 'monitor', 'keyboard', 'mouse', 'hardware']
            },
            'software': {
                'team': 'Software Licensing',
                'keywords': ['software', 'application', 'install', 'license', 'program', 'app']
            },
            'other': {
                'team': 'General IT Support',
                'keywords': []
            }
        }
    
    def check_auto_resolve(self, text: str, category: str) -> Optional[Dict]:
        """
        Check if ticket can be auto-resolved based on rules
        Returns resolution info if auto-resolvable, None otherwise
        """
        text_lower = text.lower()
        
        for rule_name, rule in self.auto_resolve_rules.items():
            # Check if any keyword matches
            for keyword in rule['keywords']:
                if keyword in text_lower:
                    # Verify category matches if specified
                    if rule['category'] and rule['category'] != category:
                        continue
                    
                    logger.info(f"Auto-resolve rule matched: {rule_name}")
                    return {
                        'can_resolve': True,
                        'rule_name': rule_name,
                        'resolution': rule['resolution'],
                        'kb_article_id': rule['kb_article_id']
                    }
        
        return None
    
    def should_escalate(self, text: str, priority: str, hours_open: int) -> bool:
        """
        Check if ticket should be escalated based on time and priority
        """
        text_lower = text.lower()
        
        # Check for high priority keywords
        for keyword in self.escalation_rules['high_priority_keywords']:
            if keyword in text_lower:
                return True
        
        # Check time-based escalation
        escalation_time = self.escalation_rules['escalation_time'].get(priority, 72)
        if hours_open >= escalation_time:
            logger.info(f"Ticket should be escalated: {hours_open} hours open (threshold: {escalation_time})")
            return True
        
        return False
    
    def get_assigned_team(self, category: str) -> str:
        """Get assigned team based on category"""
        rule = self.assignment_rules.get(category, self.assignment_rules['other'])
        return rule['team']
    
    def suggest_category(self, text: str) -> str:
        """Suggest category based on keywords"""
        text_lower = text.lower()
        
        # Count keyword matches for each category
        category_scores = {}
        for category, rule in self.assignment_rules.items():
            score = sum(1 for keyword in rule['keywords'] if keyword in text_lower)
            if score > 0:
                category_scores[category] = score
        
        # Return category with highest score
        if category_scores:
            return max(category_scores, key=category_scores.get)
        
        return 'other'
    
    def apply_sla_rules(self, priority: str) -> Dict:
        """
        Apply SLA (Service Level Agreement) rules based on priority
        Returns expected response and resolution times
        """
        sla_rules = {
            'high': {
                'response_time_hours': 1,
                'resolution_time_hours': 4,
                'description': 'Critical - Immediate attention required'
            },
            'medium': {
                'response_time_hours': 4,
                'resolution_time_hours': 24,
                'description': 'Important - Resolve within 1 business day'
            },
            'low': {
                'response_time_hours': 24,
                'resolution_time_hours': 72,
                'description': 'Standard - Resolve within 3 business days'
            }
        }
        
        return sla_rules.get(priority, sla_rules['medium'])

# Global automation engine instance
_automation_engine = None

def get_automation_engine() -> AutomationEngine:
    """Get or create automation engine instance (singleton pattern)"""
    global _automation_engine
    if _automation_engine is None:
        _automation_engine = AutomationEngine()
    return _automation_engine
