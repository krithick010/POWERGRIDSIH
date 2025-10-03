"""
Test script for AI classification and semantic search
"""

import asyncio
from ai_classifier import get_classifier
from semantic_search import get_search_engine

def test_classifier():
    """Test the ticket classifier"""
    print("\n" + "="*60)
    print("Testing AI Classifier")
    print("="*60)
    
    classifier = get_classifier()
    
    test_cases = [
        "I cannot connect to VPN from home. Getting connection failed error.",
        "My password has expired and I need to reset it urgently.",
        "Laptop screen is flickering and sometimes goes black.",
        "Need Microsoft Office license for new project.",
        "Cannot access the shared drive S:\\Engineering folder.",
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n[Test {i}] Input: {text}")
        result = classifier.classify(text)
        print(f"Category: {result['category']}")
        print(f"Priority: {result['priority']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Auto-resolve: {result['auto_resolve']}")
        if result['auto_resolve']:
            print(f"Resolution: {result['resolution_message'][:100]}...")

def test_semantic_search():
    """Test semantic search"""
    print("\n" + "="*60)
    print("Testing Semantic Search")
    print("="*60)
    
    search_engine = get_search_engine()
    
    test_queries = [
        "How do I reset my password?",
        "VPN not connecting",
        "Setup email on iPhone",
        "Request new laptop",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[Query {i}] {query}")
        results = search_engine.search(query, limit=2)
        
        if results:
            for j, article in enumerate(results, 1):
                print(f"  [{j}] {article['title']} (score: {article.get('relevance_score', 'N/A')})")
        else:
            print("  No results found")

if __name__ == "__main__":
    print("POWERGRID AI Ticketing System - AI Component Tests")
    
    test_classifier()
    test_semantic_search()
    
    print("\n" + "="*60)
    print("Tests completed!")
    print("="*60)
