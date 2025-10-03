"""
Generate embeddings for knowledge base articles using sentence-transformers.
This script should be run after seeding the knowledge base.
"""

import os
import sys
import psycopg2
from sentence_transformers import SentenceTransformer
import logging

# Configure logging
logging.basicConfig( 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database connection - Updated for your setup
DATABASE_URL = 'postgresql://vmeenakshisundaram@localhost:5432/powergrid_tickets'

def main():
    """Generate embeddings for all KB articles"""
    logger.info("Loading sentence transformer model...")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    logger.info("Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        # Get all KB articles without embeddings
        cursor.execute("""
            SELECT id, title, content 
            FROM knowledge_base 
            WHERE embedding IS NULL OR array_length(embedding, 1) IS NULL
        """)
        articles = cursor.fetchall()
        
        logger.info(f"Found {len(articles)} articles to process")
        
        for article_id, title, content in articles:
            # Combine title and content for embedding
            text = f"{title}\n\n{content}"
            
            # Generate embedding
            embedding = model.encode(text)
            
            # Update database
            cursor.execute("""
                UPDATE knowledge_base 
                SET embedding = %s 
                WHERE id = %s
            """, (embedding.tolist(), article_id))
            
            logger.info(f"Generated embedding for article: {title}")
        
        conn.commit()
        logger.info("All embeddings generated successfully!")
        
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
