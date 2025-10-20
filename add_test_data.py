#!/usr/bin/env python3
"""
Add test data to the News Screener database
"""

import requests
import json
from datetime import datetime, timedelta

API_BASE_URL = "http://localhost:8000"

def add_test_data():
    """Add test sources and articles"""
    print("📊 Adding Test Data to News Screener")
    print("=" * 40)
    
    # Test sources
    test_sources = [
        {
            "name": "TechCrunch",
            "url": "https://techcrunch.com",
            "rss_feed": "https://techcrunch.com/feed/"
        },
        {
            "name": "The Verge",
            "url": "https://theverge.com", 
            "rss_feed": "https://www.theverge.com/rss/index.xml"
        },
        {
            "name": "Ars Technica",
            "url": "https://arstechnica.com",
            "rss_feed": "https://feeds.arstechnica.com/arstechnica/index/"
        }
    ]
    
    # Add sources
    source_ids = []
    for source in test_sources:
        try:
            response = requests.post(f"{API_BASE_URL}/sources", json=source)
            if response.status_code == 200:
                source_data = response.json()
                source_ids.append(source_data['id'])
                print(f"✅ Added source: {source['name']} (ID: {source_data['id']})")
            else:
                print(f"❌ Failed to add source {source['name']}: {response.status_code}")
        except Exception as e:
            print(f"❌ Error adding source {source['name']}: {e}")
    
    # Test articles
    test_articles = [
        {
            "source_id": source_ids[0] if source_ids else 1,
            "title": "AI Revolution: How Machine Learning is Changing Everything",
            "content": "Artificial intelligence and machine learning are transforming industries across the globe. From healthcare to finance, AI is revolutionizing how we work and live.",
            "url": "https://techcrunch.com/ai-revolution",
            "published_at": datetime.now().isoformat()
        },
        {
            "source_id": source_ids[0] if source_ids else 1,
            "title": "New iPhone Features: What to Expect in 2024",
            "content": "Apple is rumored to be working on exciting new features for the iPhone. The latest leaks suggest significant improvements in camera technology and battery life.",
            "url": "https://techcrunch.com/iphone-2024",
            "published_at": (datetime.now() - timedelta(days=1)).isoformat()
        },
        {
            "source_id": source_ids[1] if len(source_ids) > 1 else 2,
            "title": "Tesla's Latest Electric Vehicle Breaks Records",
            "content": "Tesla has announced their newest electric vehicle model, featuring advanced autonomous driving capabilities and extended range. The automotive industry is taking notice.",
            "url": "https://theverge.com/tesla-new-model",
            "published_at": (datetime.now() - timedelta(days=2)).isoformat()
        },
        {
            "source_id": source_ids[2] if len(source_ids) > 2 else 3,
            "title": "Quantum Computing Breakthrough: New Algorithm Discovered",
            "content": "Researchers have developed a new quantum algorithm that could revolutionize cryptography and data processing. This breakthrough brings us closer to practical quantum computers.",
            "url": "https://arstechnica.com/quantum-breakthrough",
            "published_at": (datetime.now() - timedelta(days=3)).isoformat()
        },
        {
            "source_id": source_ids[0] if source_ids else 1,
            "title": "SpaceX Launches New Satellite Constellation",
            "content": "SpaceX successfully launched another batch of Starlink satellites, bringing global internet coverage closer to reality. The mission marks another milestone in space technology.",
            "url": "https://techcrunch.com/spacex-starlink",
            "published_at": (datetime.now() - timedelta(days=4)).isoformat()
        }
    ]
    
    # Add articles (we'll need to modify the API to accept articles directly)
    print("\n📰 Test articles created (would be added via scraper)")
    for i, article in enumerate(test_articles, 1):
        print(f"   {i}. {article['title']}")
    
    # Test filters
    test_filters = [
        {
            "name": "AI & Machine Learning",
            "keywords": "ai, artificial intelligence, machine learning, neural network"
        },
        {
            "name": "Space Technology", 
            "keywords": "spacex, nasa, satellite, space, rocket"
        },
        {
            "name": "Apple Products",
            "keywords": "apple, iphone, ipad, macbook, ios"
        }
    ]
    
    # Add filters
    for filter_data in test_filters:
        try:
            response = requests.post(f"{API_BASE_URL}/filters", json=filter_data)
            if response.status_code == 200:
                filter_result = response.json()
                print(f"✅ Added filter: {filter_data['name']} (ID: {filter_result['id']})")
            else:
                print(f"❌ Failed to add filter {filter_data['name']}: {response.status_code}")
        except Exception as e:
            print(f"❌ Error adding filter {filter_data['name']}: {e}")
    
    print(f"\n🎯 Test Data Summary:")
    print(f"   Sources: {len(source_ids)}")
    print(f"   Articles: {len(test_articles)}")
    print(f"   Filters: {len(test_filters)}")
    
    print(f"\n🌐 Frontend: http://localhost:3000")
    print(f"🔧 Backend API: http://localhost:8000")
    print(f"📚 API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    add_test_data()
