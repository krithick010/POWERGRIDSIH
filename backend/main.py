"""
FastAPI backend for POWERGRID AI Ticketing System
"""

from fastapi import FastAPI, HTTPException, Depends, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from uuid import UUID
import os
from contextlib import asynccontextmanager
import logging

from database import init_db_pool, get_db_pool, get_db_cursor
from models import TicketModel, KnowledgeBaseModel
from ai_classifier import get_classifier
from semantic_search import get_search_engine
from notifications import get_notification_service
from config import settings
from automation import get_automation_engine
from intent_classifier import AdvancedIntentClassifier
from conversation_manager import ConversationManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing database connection pool...")
    init_db_pool()
    logger.info("Database pool initialized!")
    
    logger.info("Loading AI models...")
    get_classifier()
    get_search_engine()
    logger.info("AI models loaded!")
    
    yield
    
    # Shutdown
    logger.info("Closing database connections...")
    pool = get_db_pool()
    if pool:
        pool.closeall()
    logger.info("Database connections closed!")

app = FastAPI(
    title="POWERGRID AI Ticketing System",
    description="Centralized IT ticketing system with AI-powered classification and chatbot",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class TicketCreate(BaseModel):
    source: str = Field(..., pattern="^(chatbot|email|glpi|solman)$")
    employee: str = Field(..., min_length=1, max_length=255)
    subject: str = Field(..., min_length=1, max_length=500)
    description: str = Field(..., min_length=1)
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    category: Optional[str] = Field(None, pattern="^(network|access|hardware|software|other)$")

class TicketResponse(BaseModel):
    id: UUID
    source: str
    employee: str
    subject: str
    description: str
    priority: str
    category: str
    assigned_team: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

class TicketStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(open|in_progress|resolved)$")

class ClassificationRequest(BaseModel):
    text: str = Field(..., min_length=1)

class ClassificationResponse(BaseModel):
    category: str
    priority: str
    confidence: float
    auto_resolve: bool = False
    resolution_message: Optional[str] = None

class KBArticle(BaseModel):
    id: UUID
    title: str
    content: str
    category: str
    views: Optional[int] = 0
    helpful_count: Optional[int] = 0
    relevance_score: Optional[float] = None

class ChatbotRequest(BaseModel):
    message: str
    employee: str

class ChatbotResponse(BaseModel):
    response: str
    ticket_created: bool = False
    ticket_id: Optional[UUID] = None
    kb_suggestions: List[KBArticle] = []
    auto_resolved: bool = False

# Team assignment mapping
TEAM_MAPPING = {
    "network": "Network Team",
    "access": "IT Support",
    "hardware": "Hardware Support",
    "software": "Software Licensing",
    "other": "General IT Support"
}

# Initialize new components
intent_classifier = AdvancedIntentClassifier()
conversation_manager = ConversationManager()

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "POWERGRID AI Ticketing System API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "tickets": "/tickets",
            "classify": "/classify",
            "kb_search": "/kb/search",
            "chatbot": "/chatbot",
            "docs": "/docs"
        }
    }

@app.post("/tickets", response_model=TicketResponse, status_code=201)
async def create_ticket(ticket: TicketCreate, background_tasks: BackgroundTasks):
    """
    Create a new ticket from chatbot, email, or other sources.
    If priority/category not provided, they will be classified automatically.
    """
    try:
        # If priority/category not provided, use defaults (will be enhanced with AI later)
        priority = ticket.priority or "medium"
        category = ticket.category or "other"
        
        # Assign team based on category
        assigned_team = TEAM_MAPPING.get(category, "General IT Support")
        
        # Create ticket in database
        new_ticket = TicketModel.create(
            source=ticket.source,
            employee=ticket.employee,
            subject=ticket.subject,
            description=ticket.description,
            priority=priority,
            category=category,
            assigned_team=assigned_team
        )
        
        notification_service = get_notification_service()
        # If created from chatbot, optionally use a chatbot-specific From address
        from_addr = settings.CHATBOT_FROM if ticket.source == 'chatbot' and settings.CHATBOT_FROM else None
        background_tasks.add_task(
            notification_service.notify_ticket_created,
            ticket_id=str(new_ticket['id']),
            employee=new_ticket['employee'],
            subject=new_ticket['subject'],
            priority=new_ticket['priority'],
            category=new_ticket['category'],
            assigned_team=new_ticket['assigned_team'],
            from_email=from_addr
        )
        
        return new_ticket
    
    except Exception as e:
        logger.error(f"Failed to create ticket: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create ticket: {str(e)}")

@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: UUID):
    """Get ticket details by ID"""
    ticket = TicketModel.get_by_id(ticket_id)
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return ticket

@app.get("/tickets", response_model=List[TicketResponse])
async def list_tickets(
    employee: Optional[str] = Query(None, description="Filter by employee name or ID"),
    status: Optional[str] = Query(None, pattern="^(open|in_progress|resolved)$"),
    category: Optional[str] = Query(None, pattern="^(network|access|hardware|software|other)$"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of tickets to return")
):
    """
    List tickets with optional filters.
    Returns tickets sorted by creation date (newest first).
    """
    try:
        tickets = TicketModel.list_tickets(
            employee=employee,
            status=status,
            category=category,
            limit=limit
        )
        return tickets
    
    except Exception as e:
        logger.error(f"Failed to fetch tickets: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch tickets: {str(e)}")

@app.patch("/tickets/{ticket_id}/status", response_model=TicketResponse)
async def update_ticket_status(
    ticket_id: UUID,
    status_update: TicketStatusUpdate,
    background_tasks: BackgroundTasks
):
    """Update ticket status"""
    try:
        # Get current ticket
        current_ticket = TicketModel.get_by_id(ticket_id)
        if not current_ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        old_status = current_ticket['status']
        
        # Update ticket
        updated_ticket = TicketModel.update_status(ticket_id, status_update.status)
        
        notification_service = get_notification_service()
        background_tasks.add_task(
            notification_service.notify_ticket_updated,
            ticket_id=str(updated_ticket['id']),
            employee=updated_ticket['employee'],
            subject=updated_ticket['subject'],
            old_status=old_status,
            new_status=updated_ticket['status']
        )
        
        return updated_ticket
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update ticket: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update ticket: {str(e)}")

@app.post("/classify", response_model=ClassificationResponse)
async def classify_ticket(request: ClassificationRequest):
    """
    Classify ticket text into category and priority using Hugging Face AI models.
    Also checks for auto-resolvable issues.
    """
    try:
        classifier = get_classifier()
        result = classifier.classify(request.text)
        
        logger.info(f"Classification result: {result}")
        
        return {
            "category": result["category"],
            "priority": result["priority"],
            "confidence": result["confidence"],
            "auto_resolve": result["auto_resolve"],
            "resolution_message": result["resolution_message"]
        }
    
    except Exception as e:
        logger.error(f"Classification error: {e}")
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

@app.get("/kb/search", response_model=List[KBArticle])
async def search_knowledge_base(
    query: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(3, ge=1, le=10, description="Number of results to return"),
    use_semantic: bool = Query(True, description="Use semantic search (AI-powered)")
):
    """
    Search knowledge base using semantic similarity (AI-powered) or keyword matching.
    Semantic search provides better results by understanding context and meaning.
    """
    try:
        if use_semantic:
            search_engine = get_search_engine()
            articles = search_engine.search(query, limit)
        else:
            # Fallback to keyword search
            articles = KnowledgeBaseModel.search_by_keywords(query, limit)
        
        logger.info(f"Found {len(articles)} articles for query: {query}")
        return articles
    
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to search knowledge base: {str(e)}")

@app.get("/kb/{article_id}", response_model=KBArticle)
async def get_kb_article(article_id: UUID):
    """Get knowledge base article by ID and increment view count"""
    try:
        article = KnowledgeBaseModel.get_by_id(article_id)
        
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        # Increment view count
        KnowledgeBaseModel.increment_views(article_id)
        
        return article
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch article: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch article: {str(e)}")

@app.post("/chatbot", response_model=ChatbotResponse)
async def chatbot_interaction(request: ChatbotRequest, background_tasks: BackgroundTasks):
    """
    Enhanced chatbot with context awareness and better intent detection
    """
    try:
        # Get user intent
        intent_result = intent_classifier.classify_intent(request.message)
        
        # Handle non-IT related intents with context
        if not intent_result["is_it_related"]:
            response = conversation_manager.generate_contextual_response(
                request.employee, 
                request.message, 
                intent_result["intent"]
            )
            
            # Update conversation context
            conversation_manager.update_context(
                request.employee, 
                request.message, 
                response, 
                intent_result["intent"]
            )
            
            return {
                "response": response,
                "ticket_created": False,
                "kb_suggestions": [],
                "auto_resolved": True
            }
        
        # For IT-related queries, proceed with enhanced logic
        classification = await classify_ticket(ClassificationRequest(text=request.message))
        kb_articles = await search_knowledge_base(query=request.message, limit=3)
        
        # Enhanced auto-resolution with follow-up questions
        if classification['auto_resolve']:
            response = classification['resolution_message']
            
            # Add follow-up question
            response += "\n\nDid this help resolve your issue? If not, I can create a support ticket for further assistance."
            
            conversation_manager.update_context(
                request.employee, 
                request.message, 
                response, 
                "auto_resolved"
            )
            
            return {
                "response": response,
                "ticket_created": False,
                "kb_suggestions": kb_articles,
                "auto_resolved": True
            }
        
        # Check conversation context for better ticket creation
        context = conversation_manager.get_context(request.employee)
        
        # Enhanced ticket subject based on intent and context
        subject = _generate_smart_subject(request.message, intent_result["intent"], context)
        
        # Create ticket with enhanced information
        ticket = await create_ticket(
            TicketCreate(
                source="chatbot",
                employee=request.employee,
                subject=subject,
                description=_enhance_description(request.message, context),
                priority=classification['priority'],
                category=classification['category']
            ),
            background_tasks=background_tasks
        )
        
        # Generate personalized response
        response_message = _generate_ticket_response(ticket, classification, request.employee, context)
        
        if kb_articles:
            response_message += "\n\n📚 Here are some relevant articles that might help while you wait:"
            for article in kb_articles[:2]:  # Show top 2
                response_message += f"\n• {article['title']}"
        
        # Update conversation context
        conversation_manager.update_context(
            request.employee, 
            request.message, 
            response_message, 
            "ticket_created"
        )
        
        # Add ticket to user's context
        if request.employee in conversation_manager.conversations:
            conversation_manager.conversations[request.employee]["tickets_created"].append(str(ticket['id']))
        
        return {
            "response": response_message,
            "ticket_created": True,
            "ticket_id": ticket['id'],
            "kb_suggestions": kb_articles,
            "auto_resolved": False
        }
    
    except Exception as e:
        logger.error(f"Chatbot error: {e}")
        error_response = "I apologize, but I'm experiencing some technical difficulties. Please try again in a moment, or contact IT support directly."
        
        conversation_manager.update_context(
            request.employee, 
            request.message, 
            error_response, 
            "error"
        )
        
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")

@app.post("/chatbot/feedback")
async def chatbot_feedback(
    ticket_id: Optional[UUID] = None,
    helpful: bool = False,
    feedback_text: Optional[str] = None,
    employee: str = ""
):
    """Collect feedback on chatbot responses"""
    try:
        # Store feedback in database for improvement
        feedback_data = {
            "ticket_id": ticket_id,
            "employee": employee,
            "helpful": helpful,
            "feedback_text": feedback_text,
            "timestamp": datetime.now()
        }
        
        # Log feedback for analysis
        logger.info(f"Chatbot feedback: {feedback_data}")
        
        return {"message": "Thank you for your feedback!"}
    
    except Exception as e:
        logger.error(f"Feedback error: {e}")
        raise HTTPException(status_code=500, detail="Failed to record feedback")

@app.get("/chatbot/follow-up/{ticket_id}")
async def chatbot_follow_up(ticket_id: UUID):
    """Proactive follow-up on tickets"""
    try:
        ticket = TicketModel.get_by_id(ticket_id)
        
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        # Generate follow-up message based on ticket status
        if ticket['status'] == 'resolved':
            message = f"Your ticket #{str(ticket_id)[:8]} has been resolved! Was the solution helpful?"
        else:
            message = f"Your ticket #{str(ticket_id)[:8]} is being worked on. Do you have any additional information to add?"
        
        return {"message": message, "ticket": ticket}
    
    except Exception as e:
        logger.error(f"Follow-up error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate follow-up")

def _generate_smart_subject(message: str, intent: str, context: Optional[Dict]) -> str:
    """Generate intelligent subject line based on intent and context"""
    intent_subjects = {
        "password_issue": "Password Reset Request",
        "network_issue": "Network Connectivity Issue", 
        "hardware_issue": "Hardware Support Request",
        "software_issue": "Software Installation/Support",
        "email_issue": "Email Configuration Support",
        "access_issue": "File/Folder Access Request"
    }
    
    if intent in intent_subjects:
        return intent_subjects[intent]
    
    # Fallback to first 50 characters of message
    return message[:50].strip() + ("..." if len(message) > 50 else "")

def _enhance_description(message: str, context: Optional[Dict]) -> str:
    """Enhance ticket description with context"""
    description = f"User Message: {message}\n\n"
    
    if context and context.get("history"):
        description += "Previous Conversation:\n"
        for interaction in context["history"][-3:]:  # Last 3 interactions
            description += f"User: {interaction['message']}\n"
            description += f"Bot: {interaction['response'][:100]}...\n\n"
    
    description += f"Ticket created via AI Chatbot at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    return description

def _generate_ticket_response(ticket: Dict, classification: Dict, employee: str, context: Optional[Dict]) -> str:
    """Generate personalized ticket creation response"""
    response = f"✅ I've created support ticket #{ticket['id'][:8]} for you.\n\n"
    response += f"📋 **Details:**\n"
    response += f"• Category: {classification['category'].title()}\n"
    response += f"• Priority: {classification['priority'].title()}\n"
    response += f"• Assigned to: {ticket['assigned_team']}\n\n"
    
    # Add estimated resolution time based on priority
    eta_map = {"high": "2-4 hours", "medium": "4-8 hours", "low": "1-2 business days"}
    response += f"⏰ **Expected Resolution:** {eta_map.get(classification['priority'], '1-2 business days')}\n\n"
    
    response += f"📧 You'll receive email updates at your registered address."
    
    return response

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        with get_db_cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
