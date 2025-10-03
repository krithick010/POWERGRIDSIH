"""
Database models and operations
"""

from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
from database import get_db_cursor

class TicketModel:
    """Ticket database operations"""
    
    @staticmethod
    def create(
        source: str,
        employee: str,
        subject: str,
        description: str,
        priority: str,
        category: str,
        assigned_team: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new ticket"""
        with get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO tickets (source, employee, subject, description, priority, category, assigned_team, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'open')
                RETURNING id, source, employee, subject, description, priority, category, assigned_team, status, created_at, updated_at
            """, (source, employee, subject, description, priority, category, assigned_team))
            
            return dict(cursor.fetchone())
    
    @staticmethod
    def get_by_id(ticket_id: UUID) -> Optional[Dict[str, Any]]:
        """Get ticket by ID"""
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT id, source, employee, subject, description, priority, category, assigned_team, status, created_at, updated_at
                FROM tickets
                WHERE id = %s
            """, (str(ticket_id),))
            
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def list_tickets(
        employee: Optional[str] = None,
        status: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List tickets with optional filters"""
        query = """
            SELECT id, source, employee, subject, description, priority, category, assigned_team, status, created_at, updated_at
            FROM tickets
            WHERE 1=1
        """
        params = []
        
        if employee:
            query += " AND LOWER(employee) LIKE LOWER(%s)"
            params.append(f"%{employee}%")
        
        if status:
            query += " AND status = %s"
            params.append(status)
        
        if category:
            query += " AND category = %s"
            params.append(category)
        
        query += " ORDER BY created_at DESC LIMIT %s"
        params.append(limit)
        
        with get_db_cursor() as cursor:
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def update_status(ticket_id: UUID, status: str) -> Optional[Dict[str, Any]]:
        """Update ticket status"""
        with get_db_cursor() as cursor:
            cursor.execute("""
                UPDATE tickets
                SET status = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING id, source, employee, subject, description, priority, category, assigned_team, status, created_at, updated_at
            """, (status, str(ticket_id)))
            
            result = cursor.fetchone()
            return dict(result) if result else None

class KnowledgeBaseModel:
    """Knowledge Base database operations"""
    
    @staticmethod
    def search_by_keywords(query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Search KB by keywords (simple text search)"""
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT id, title, content, category, views, helpful_count
                FROM knowledge_base
                WHERE 
                    LOWER(title) LIKE LOWER(%s) OR
                    LOWER(content) LIKE LOWER(%s) OR
                    %s = ANY(keywords)
                ORDER BY helpful_count DESC, views DESC
                LIMIT %s
            """, (f"%{query}%", f"%{query}%", query.lower(), limit))
            
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_by_id(kb_id: UUID) -> Optional[Dict[str, Any]]:
        """Get KB article by ID"""
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT id, title, content, category, keywords, views, helpful_count, created_at
                FROM knowledge_base
                WHERE id = %s
            """, (str(kb_id),))
            
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def increment_views(kb_id: UUID):
        """Increment view count for KB article"""
        with get_db_cursor() as cursor:
            cursor.execute("""
                UPDATE knowledge_base
                SET views = views + 1
                WHERE id = %s
            """, (str(kb_id),))
    
    @staticmethod
    def get_all_with_embeddings() -> List[Dict[str, Any]]:
        """Get all KB articles with embeddings for semantic search"""
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT id, title, content, category, embedding
                FROM knowledge_base
                WHERE embedding IS NOT NULL
            """)
            
            return [dict(row) for row in cursor.fetchall()]
