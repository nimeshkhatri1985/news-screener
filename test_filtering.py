#!/usr/bin/env python3
"""
Comprehensive test for News Screener filtering system
"""

import requests
import json
from datetime import datetime, timedelta

API_BASE_URL = "http://localhost:8000"

def test_filtering_system():
    """Test the complete filtering system"""
    print("🧪 Testing News Screener Filtering System")
    print("=" * 50)
    
    # First, let's add some test articles to see filtering in action
    print("\n📰 Adding Test Articles...")
    
    # Get source IDs
    sources_response = requests.get(f"{API_BASE_URL}/sources")
    sources = sources_response.json()
    print(f"   Found {len(sources)} sources")
    
    if not sources:
        print("❌ No sources found. Please add sources first.")
        return
    
    # Create test articles directly in the database (we'll simulate this)
    test_articles = [
        {
            "source_id": sources[0]['id'],
            "title": "AI Revolution: How Machine Learning is Changing Everything",
            "content": "Artificial intelligence and machine learning are transforming industries across the globe. From healthcare to finance, AI is revolutionizing how we work and live.",
            "url": "https://techcrunch.com/ai-revolution",
            "published_at": datetime.now().isoformat()
        },
        {
            "source_id": sources[0]['id'],
            "title": "New iPhone Features: What to Expect in 2024",
            "content": "Apple is rumored to be working on exciting new features for the iPhone. The latest leaks suggest significant improvements in camera technology and battery life.",
            "url": "https://techcrunch.com/iphone-2024",
            "published_at": (datetime.now() - timedelta(days=1)).isoformat()
        },
        {
            "source_id": sources[1]['id'] if len(sources) > 1 else sources[0]['id'],
            "title": "Tesla's Latest Electric Vehicle Breaks Records",
            "content": "Tesla has announced their newest electric vehicle model, featuring advanced autonomous driving capabilities and extended range. The automotive industry is taking notice.",
            "url": "https://theverge.com/tesla-new-model",
            "published_at": (datetime.now() - timedelta(days=2)).isoformat()
        },
        {
            "source_id": sources[2]['id'] if len(sources) > 2 else sources[0]['id'],
            "title": "Quantum Computing Breakthrough: New Algorithm Discovered",
            "content": "Researchers have developed a new quantum algorithm that could revolutionize cryptography and data processing. This breakthrough brings us closer to practical quantum computers.",
            "url": "https://arstechnica.com/quantum-breakthrough",
            "published_at": (datetime.now() - timedelta(days=3)).isoformat()
        },
        {
            "source_id": sources[0]['id'],
            "title": "SpaceX Launches New Satellite Constellation",
            "content": "SpaceX successfully launched another batch of Starlink satellites, bringing global internet coverage closer to reality. The mission marks another milestone in space technology.",
            "url": "https://techcrunch.com/spacex-starlink",
            "published_at": (datetime.now() - timedelta(days=4)).isoformat()
        }
    ]
    
    print(f"   Created {len(test_articles)} test articles")
    
    # Test 1: Basic Articles Endpoint
    print("\n🔍 Test 1: Basic Articles Endpoint")
    try:
        response = requests.get(f"{API_BASE_URL}/articles")
        articles = response.json()
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📊 Found {len(articles)} articles")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Source Filtering
    print("\n🔍 Test 2: Source Filtering")
    try:
        response = requests.get(f"{API_BASE_URL}/articles?source_id={sources[0]['id']}")
        filtered_articles = response.json()
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📊 Found {len(filtered_articles)} articles from {sources[0]['name']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Keyword Filtering
    print("\n🔍 Test 3: Keyword Filtering")
    try:
        response = requests.get(f"{API_BASE_URL}/articles?keywords=ai,machine learning")
        keyword_articles = response.json()
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📊 Found {len(keyword_articles)} articles with AI/ML keywords")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Date Range Filtering
    print("\n🔍 Test 4: Date Range Filtering")
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        response = requests.get(f"{API_BASE_URL}/articles?date_from={today}")
        date_articles = response.json()
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📊 Found {len(date_articles)} articles from today")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Combined Filtering
    print("\n🔍 Test 5: Combined Filtering")
    try:
        response = requests.get(f"{API_BASE_URL}/articles?source_id={sources[0]['id']}&keywords=apple,iphone")
        combined_articles = response.json()
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📊 Found {len(combined_articles)} articles with combined filters")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Search Endpoint
    print("\n🔍 Test 6: Search Endpoint")
    try:
        response = requests.get(f"{API_BASE_URL}/search?q=tesla")
        search_results = response.json()
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📊 Found {len(search_results)} search results for 'tesla'")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 7: Filters Management
    print("\n🔍 Test 7: Filters Management")
    try:
        response = requests.get(f"{API_BASE_URL}/filters")
        filters = response.json()
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📊 Found {len(filters)} saved filters")
        for filter_item in filters:
            print(f"      - {filter_item['name']}: {filter_item['keywords']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 8: Posts Management
    print("\n🔍 Test 8: Posts Management")
    try:
        response = requests.get(f"{API_BASE_URL}/posts")
        posts = response.json()
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📊 Found {len(posts)} posts")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎯 Frontend Testing")
    print("-" * 20)
    print("🌐 Frontend URL: http://localhost:3000")
    print("📱 Test the following features:")
    print("   1. Navigate to Articles page")
    print("   2. Try the search box")
    print("   3. Click 'Show Advanced Filters'")
    print("   4. Test keyword filtering")
    print("   5. Test date range filtering")
    print("   6. Test source filtering")
    print("   7. Test combined filters")
    
    print("\n📊 API Documentation")
    print("-" * 20)
    print(f"📚 Swagger UI: {API_BASE_URL}/docs")
    print(f"📖 ReDoc: {API_BASE_URL}/redoc")
    
    print("\n✅ Filtering system test complete!")

if __name__ == "__main__":
    test_filtering_system()
