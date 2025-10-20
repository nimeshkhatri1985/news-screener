#!/usr/bin/env python3
"""
Simple test script to verify the news screener setup
"""

import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"❌ SQLAlchemy import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        import feedparser
        print("✅ Feedparser imported successfully")
    except ImportError as e:
        print(f"❌ Feedparser import failed: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup imported successfully")
    except ImportError as e:
        print(f"❌ BeautifulSoup import failed: {e}")
        return False
    
    return True

def test_scraper():
    """Test the scraper functionality"""
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        from scraper import NewsScraper
        scraper = NewsScraper()
        print("✅ NewsScraper created successfully")
        
        # Test RSS parsing with a simple feed
        test_feed = "https://hnrss.org/frontpage"
        articles = scraper.scrape_rss_feed(test_feed, 1)
        print(f"✅ RSS scraping test: Found {len(articles)} articles")
        
        return True
    except Exception as e:
        print(f"❌ Scraper test failed: {e}")
        return False

def main():
    print("🧪 Testing News Screener Setup")
    print("=" * 40)
    
    # Test imports
    print("\n📦 Testing imports...")
    imports_ok = test_imports()
    
    if not imports_ok:
        print("\n❌ Some imports failed. Please install missing dependencies:")
        print("pip install -r requirements.txt")
        return
    
    # Test scraper
    print("\n🔍 Testing scraper...")
    scraper_ok = test_scraper()
    
    if scraper_ok:
        print("\n✅ All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up PostgreSQL database")
        print("3. Run: python main.py")
        print("4. Visit: http://localhost:8000/docs")
    else:
        print("\n❌ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
