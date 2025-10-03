"""
Semantic search for knowledge base using sentence transformers
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
import logging

from models import KnowledgeBaseModel

logger = logging.getLogger(__name__)

class SemanticSearchEngine:
    """
    Semantic search engine using sentence transformers
    """
    
    def __init__(self):
        logger.info("Loading sentence transformer model...")
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        logger.info("Sentence transformer loaded successfully!")
        
        # Cache for KB embeddings
        self._kb_cache = None
        self._cache_timestamp = None
    
    def _load_kb_embeddings(self) -> List[Dict]:
        """Load KB articles with embeddings from database"""
        articles = KnowledgeBaseModel.get_all_with_embeddings()
        
        # Convert embedding arrays to numpy
        for article in articles:
            if article.get('embedding'):
                article['embedding'] = np.array(article['embedding'])
        
        return articles
    
    def _get_kb_cache(self) -> List[Dict]:
        """Get cached KB embeddings or load from database"""
        # Simple cache - in production, use Redis or similar
        if self._kb_cache is None:
            logger.info("Loading KB embeddings into cache...")
            self._kb_cache = self._load_kb_embeddings()
            logger.info(f"Loaded {len(self._kb_cache)} KB articles")
        
        return self._kb_cache
    
    def search(self, query: str, limit: int = 3) -> List[Dict]:
        """
        Search knowledge base using semantic similarity
        Returns articles sorted by relevance
        """
        try:
            # Generate query embedding
            query_embedding = self.model.encode(query)
            
            # Get KB articles with embeddings
            kb_articles = self._get_kb_cache()
            
            if not kb_articles:
                logger.warning("No KB articles with embeddings found")
                return []
            
            # Calculate cosine similarity
            similarities = []
            for article in kb_articles:
                if article.get('embedding') is not None:
                    # Cosine similarity
                    similarity = np.dot(query_embedding, article['embedding']) / (
                        np.linalg.norm(query_embedding) * np.linalg.norm(article['embedding'])
                    )
                    similarities.append((article, float(similarity)))
            
            # Sort by similarity (descending)
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Return top results with relevance scores
            results = []
            for article, score in similarities[:limit]:
                result = {
                    "id": article['id'],
                    "title": article['title'],
                    "content": article['content'],
                    "category": article['category'],
                    "relevance_score": round(score, 3)
                }
                results.append(result)
            
            logger.info(f"Found {len(results)} relevant articles for query: {query[:50]}...")
            return results
        
        except Exception as e:
            logger.error(f"Semantic search error: {e}")
            # Fallback to keyword search
            return KnowledgeBaseModel.search_by_keywords(query, limit)
    
    def refresh_cache(self):
        """Refresh the KB embeddings cache"""
        logger.info("Refreshing KB cache...")
        self._kb_cache = None
        self._get_kb_cache()

# Global search engine instance
_search_engine = None

def get_search_engine() -> SemanticSearchEngine:
    """Get or create search engine instance (singleton pattern)"""
    global _search_engine
    if _search_engine is None:
        _search_engine = SemanticSearchEngine()
    return _search_engine
