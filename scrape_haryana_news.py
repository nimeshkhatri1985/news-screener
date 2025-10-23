"""
Script to scrape real Haryana news from configured RSS feeds
"""

import os
import sys
from datetime import datetime

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from scraper import NewsScraper
from main import SessionLocal, Source, Article

def scrape_haryana_news():
    """Scrape news from Haryana-specific sources"""
    print("\n" + "="*70)
    print("🚀 SCRAPING HARYANA NEWS FROM RSS FEEDS")
    print("="*70 + "\n")
    
    db = SessionLocal()
    scraper = NewsScraper()
    
    try:
        # Get Haryana news sources
        sources = db.query(Source).filter(Source.is_active == True).all()
        
        if not sources:
            print("❌ No active sources found!")
            print("   Run: python3 backend/setup_haryana.py")
            return
        
        print(f"📰 Found {len(sources)} active news sources:\n")
        for source in sources:
            print(f"   • {source.name}")
            print(f"     URL: {source.rss_feed}")
        
        print("\n" + "-"*70)
        print("Starting RSS feed scraping...")
        print("-"*70 + "\n")
        
        total_articles = 0
        total_new = 0
        
        for idx, source in enumerate(sources, 1):
            print(f"\n[{idx}/{len(sources)}] Scraping: {source.name}")
            print(f"     RSS: {source.rss_feed}")
            
            try:
                # Scrape articles from RSS feed
                articles = scraper.scrape_rss_feed(source.rss_feed, source.id)
                
                if not articles:
                    print(f"     ⚠️  No articles found (may be RSS feed issue)")
                    continue
                
                # Save articles to database
                saved_count = scraper.save_articles(articles)
                
                total_articles += len(articles)
                total_new += saved_count
                
                print(f"     ✅ Found: {len(articles)} articles")
                print(f"     ✅ New: {saved_count} articles saved")
                
                if saved_count < len(articles):
                    print(f"     ℹ️  Skipped: {len(articles) - saved_count} (already in database)")
                
            except Exception as e:
                print(f"     ❌ Error: {str(e)}")
        
        print("\n" + "="*70)
        print("📊 SCRAPING SUMMARY")
        print("="*70)
        
        # Get database statistics
        total_db_articles = db.query(Article).count()
        haryana_relevant = 0
        
        # Count Haryana-relevant articles
        from haryana_config import is_haryana_relevant
        all_articles = db.query(Article).all()
        for article in all_articles:
            article_text = f"{article.title} {article.content}"
            if is_haryana_relevant(article_text):
                haryana_relevant += 1
        
        print(f"\n✅ Total articles fetched: {total_articles}")
        print(f"✅ New articles saved: {total_new}")
        print(f"📊 Total articles in database: {total_db_articles}")
        print(f"🎯 Haryana-relevant articles: {haryana_relevant}")
        
        if total_new > 0:
            print("\n" + "="*70)
            print("🎉 SUCCESS! New articles have been added!")
            print("="*70)
            print("\n💡 Next steps:")
            print("   1. Restart your backend server to load Haryana endpoints")
            print("      → cd backend && python3 main.py")
            print("   2. Open http://localhost:3000/haryana in your browser")
            print("   3. Try different filter categories to see the articles!")
            print("\n" + "="*70)
        else:
            print("\n" + "="*70)
            print("ℹ️  No new articles (all articles already in database)")
            print("="*70)
            print("\n💡 To see the articles:")
            print("   1. Make sure backend is running: cd backend && python3 main.py")
            print("   2. Open http://localhost:3000/haryana")
            print("   3. Use filter categories to browse existing articles")
            print("\n   Articles will be updated next time you run this script.")
            print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error during scraping: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    scrape_haryana_news()

