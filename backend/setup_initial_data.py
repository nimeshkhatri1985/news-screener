#!/usr/bin/env python3
"""
Script to add initial news sources and test the scraper
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import Source, SessionLocal
from scraper import NewsScraper

def add_initial_sources():
    """Add some initial news sources for testing"""
    db = SessionLocal()
    
    # Check if sources already exist
    existing_sources = db.query(Source).count()
    if existing_sources > 0:
        print(f"Found {existing_sources} existing sources. Skipping initial data.")
        db.close()
        return
    
    # Add some popular tech news sources
    initial_sources = [
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
        },
        {
            "name": "Wired",
            "url": "https://wired.com",
            "rss_feed": "https://www.wired.com/feed/rss"
        },
        {
            "name": "Hacker News",
            "url": "https://news.ycombinator.com",
            "rss_feed": "https://hnrss.org/frontpage"
        }
    ]
    
    try:
        for source_data in initial_sources:
            source = Source(**source_data)
            db.add(source)
        
        db.commit()
        print(f"Added {len(initial_sources)} initial news sources")
        
    except Exception as e:
        print(f"Error adding sources: {e}")
        db.rollback()
    finally:
        db.close()

def test_scraper():
    """Test the scraper with initial sources"""
    print("Testing news scraper...")
    scraper = NewsScraper()
    saved_count = scraper.scrape_all_sources()
    print(f"Scraper test completed. Saved {saved_count} articles.")

if __name__ == "__main__":
    print("Setting up initial data...")
    add_initial_sources()
    test_scraper()
    print("Setup complete!")
