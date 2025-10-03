"""
FastAPI backend for POWERGRID AI Ticketing System
"""

from fastapi import FastAPI, HTTPException, Depends, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
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
from automation import get_automation_engine

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
        background_tasks.add_task(
            notification_service.notify_ticket_created,
            ticket_id=str(new_ticket['id']),
            employee=new_ticket['employee'],
            subject=new_ticket['subject'],
            priority=new_ticket['priority'],
            category=new_ticket['category'],
            assigned_team=new_ticket['assigned_team']
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
    Handle chatbot interaction: classify message, search KB, and optionally create ticket.
    """
    try:
        message_lower = request.message.lower().strip()
        
        # First, classify the message to determine if it's IT-related
        classification = await classify_ticket(ClassificationRequest(text=request.message))
        
        # Check if message is too short or has very low confidence (likely greeting/non-IT)
        if len(message_lower) <= 20 or classification['confidence'] < 0.3:
            # Use AI to determine if it's actually an IT issue
            it_keywords = ["password", "vpn", "email", "network", "computer", "laptop", "software", 
                          "hardware", "install", "error", "problem", "issue", "help", "support",
                          "not working", "broken", "access", "login", "wifi", "internet", "printer"]
            
            has_it_context = any(keyword in message_lower for keyword in it_keywords)
            
            if not has_it_context:
                return {
                    "response": "Hello! I'm your IT support assistant. Please describe any technical issues you're experiencing, and I'll help you find a solution or create a support ticket.",
                    "ticket_created": False,
                    "kb_suggestions": [],
                    "auto_resolved": True
                }
        
        # Search knowledge base
        kb_articles = await search_knowledge_base(query=request.message, limit=3)
        
        # Check if auto-resolvable
        if classification['auto_resolve']:
            return {
                "response": classification['resolution_message'],
                "ticket_created": False,
                "kb_suggestions": kb_articles,
                "auto_resolved": True
            }
        
        # Create ticket for legitimate IT issues
        ticket = await create_ticket(
            TicketCreate(
                source="chatbot",
                employee=request.employee,
                subject=request.message[:100],
                description=request.message,
                priority=classification['priority'],
                category=classification['category']
            ),
            background_tasks=background_tasks
        )
        
        response_message = f"I've created a support ticket for you (ID: {ticket['id']}). Your issue has been categorized as '{classification['category']}' with '{classification['priority']}' priority and assigned to {ticket['assigned_team']}. You'll receive updates via email."
        
        if kb_articles:
            response_message += "\n\nHere are some relevant knowledge base articles that might help:"
        
        return {
            "response": response_message,
            "ticket_created": True,
            "ticket_id": ticket['id'],
            "kb_suggestions": kb_articles,
            "auto_resolved": False
        }
    
    except Exception as e:
        logger.error(f"Chatbot error: {e}")
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")

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
