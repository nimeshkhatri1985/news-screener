#!/usr/bin/env python3
"""
Frontend Interface Test for News Screener
"""

import requests
import time
from datetime import datetime

def test_frontend_interface():
    """Test the frontend interface functionality"""
    print("🌐 Testing News Screener Frontend Interface")
    print("=" * 50)
    
    # Test frontend availability
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend server is running on http://localhost:3000")
        else:
            print(f"❌ Frontend server returned status: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Frontend server not accessible: {e}")
        return
    
    # Test backend API connectivity
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is accessible")
        else:
            print(f"❌ Backend API returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Backend API not accessible: {e}")
    
    print("\n🎯 Frontend Interface Testing")
    print("-" * 30)
    
    # Test API endpoints that the frontend will use
    endpoints_to_test = [
        ("/sources", "Sources"),
        ("/articles", "Articles"),
        ("/filters", "Filters"),
        ("/posts", "Posts"),
        ("/articles?keywords=ai,machine%20learning", "Keyword Filtering"),
        ("/articles?source_id=1", "Source Filtering"),
        ("/search?q=tech", "Search")
    ]
    
    for endpoint, description in endpoints_to_test:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"✅ {description}: {len(data)} items")
                else:
                    print(f"✅ {description}: Working")
            else:
                print(f"⚠️  {description}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {description}: {e}")
    
    print("\n📱 Frontend Pages to Test")
    print("-" * 25)
    print("🌐 Open http://localhost:3000 in your browser")
    print("\n📋 Test Checklist:")
    print("   ✅ Dashboard Page:")
    print("      - View statistics cards")
    print("      - Check navigation menu")
    print("      - Verify responsive design")
    
    print("\n   ✅ Articles Page:")
    print("      - Test search functionality")
    print("      - Try source filtering dropdown")
    print("      - Check 'Show Advanced Filters' button")
    print("      - Test keyword input field")
    print("      - Test date range picker")
    print("      - Try 'Clear Filters' button")
    
    print("\n   ✅ Sources Page:")
    print("      - View existing sources (TechCrunch, The Verge, Ars Technica)")
    print("      - Check source status indicators")
    print("      - Verify source URLs and RSS feeds")
    
    print("\n   ✅ Posts Page:")
    print("      - View empty posts state")
    print("      - Check page layout and styling")
    
    print("\n🎨 UI/UX Features to Verify:")
    print("   ✅ Responsive design (try different screen sizes)")
    print("   ✅ Navigation between pages")
    print("   ✅ Consistent styling with Tailwind CSS")
    print("   ✅ Loading states and empty states")
    print("   ✅ Form inputs and buttons")
    print("   ✅ Color scheme and typography")
    
    print("\n🔧 Advanced Features to Test:")
    print("   ✅ Filter combinations (source + keywords + date)")
    print("   ✅ Search functionality")
    print("   ✅ Real-time filtering")
    print("   ✅ Error handling")
    
    print("\n📊 Current Data Status:")
    try:
        sources_response = requests.get("http://localhost:8000/sources")
        sources = sources_response.json()
        print(f"   📰 Sources: {len(sources)} loaded")
        
        filters_response = requests.get("http://localhost:8000/filters")
        filters = filters_response.json()
        print(f"   🔍 Filters: {len(filters)} loaded")
        
        articles_response = requests.get("http://localhost:8000/articles")
        articles = articles_response.json()
        print(f"   📄 Articles: {len(articles)} loaded")
        
    except Exception as e:
        print(f"   ❌ Error fetching data status: {e}")
    
    print("\n🚀 Next Steps:")
    print("   1. Test all frontend pages manually")
    print("   2. Verify filtering functionality")
    print("   3. Test responsive design")
    print("   4. Check for any UI/UX issues")
    print("   5. Ready for Twitter API integration")
    
    print("\n✅ Frontend interface test complete!")
    print("🌐 Frontend: http://localhost:3000")
    print("🔧 Backend: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    test_frontend_interface()
