#!/usr/bin/env python3
"""
Test script for News Screener API endpoints
"""

import requests
import json
from datetime import datetime

API_BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test all API endpoints"""
    print("🧪 Testing News Screener API Endpoints")
    print("=" * 50)
    
    # Test root endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
    
    # Test sources endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/sources")
        print(f"✅ Sources endpoint: {response.status_code}")
        sources = response.json()
        print(f"   Found {len(sources)} sources")
    except Exception as e:
        print(f"❌ Sources endpoint failed: {e}")
    
    # Test articles endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/articles")
        print(f"✅ Articles endpoint: {response.status_code}")
        articles = response.json()
        print(f"   Found {len(articles)} articles")
    except Exception as e:
        print(f"❌ Articles endpoint failed: {e}")
    
    # Test search endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/search?q=tech")
        print(f"✅ Search endpoint: {response.status_code}")
        search_results = response.json()
        print(f"   Found {len(search_results)} search results")
    except Exception as e:
        print(f"❌ Search endpoint failed: {e}")
    
    # Test filters endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/filters")
        print(f"✅ Filters endpoint: {response.status_code}")
        filters = response.json()
        print(f"   Found {len(filters)} filters")
    except Exception as e:
        print(f"❌ Filters endpoint failed: {e}")
    
    # Test posts endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/posts")
        print(f"✅ Posts endpoint: {response.status_code}")
        posts = response.json()
        print(f"   Found {len(posts)} posts")
    except Exception as e:
        print(f"❌ Posts endpoint failed: {e}")
    
    print("\n🎯 Testing Advanced Filtering")
    print("-" * 30)
    
    # Test advanced filtering
    try:
        # Test keyword filtering
        response = requests.get(f"{API_BASE_URL}/articles?keywords=ai,machine learning")
        print(f"✅ Keyword filtering: {response.status_code}")
        filtered_articles = response.json()
        print(f"   Found {len(filtered_articles)} articles with keywords")
        
        # Test date filtering
        today = datetime.now().strftime("%Y-%m-%d")
        response = requests.get(f"{API_BASE_URL}/articles?date_from={today}")
        print(f"✅ Date filtering: {response.status_code}")
        date_filtered = response.json()
        print(f"   Found {len(date_filtered)} articles from today")
        
    except Exception as e:
        print(f"❌ Advanced filtering failed: {e}")
    
    print("\n📊 API Documentation")
    print("-" * 20)
    print(f"📚 Swagger UI: {API_BASE_URL}/docs")
    print(f"📖 ReDoc: {API_BASE_URL}/redoc")
    
    print("\n✅ API testing complete!")

if __name__ == "__main__":
    test_api_endpoints()
