"""
Scrape articles from the newly added Haryana sources
"""
import sys
sys.path.append('backend')

from scraper import NewsScraper
from main import SessionLocal, Source

def scrape_new_sources():
    db = SessionLocal()
    scraper = NewsScraper()
    
    # Get the newly added sources (IDs 6, 7, 8, 9)
    new_source_ids = [6, 7, 8, 9]
    new_sources = db.query(Source).filter(Source.id.in_(new_source_ids)).all()
    
    print("🔄 Scraping articles from new Haryana sources...")
    print("=" * 60)
    
    total_fetched = 0
    total_saved = 0
    
    for source in new_sources:
        print(f"\n📰 Scraping: {source.name}")
        print(f"   RSS: {source.rss_feed}")
        print("-" * 60)
        
        try:
            # Scrape the RSS feed
            articles = scraper.scrape_rss_feed(source.rss_feed, source.id)
            fetched = len(articles)
            
            # Save articles to database
            saved = scraper.save_articles(articles)
            
            print(f"   ✅ Fetched: {fetched} articles")
            print(f"   ✅ Saved: {saved} new articles")
            
            total_fetched += fetched
            total_saved += saved
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"📊 SUMMARY:")
    print(f"   Total fetched: {total_fetched} articles")
    print(f"   Total saved: {total_saved} new articles")
    print(f"   Sources processed: {len(new_sources)}")
    
    # Check Haryana relevance
    from haryana_config import is_haryana_relevant
    from main import Article
    
    print("\n🔍 Checking Haryana relevance of new articles...")
    
    # Get articles from new sources
    new_articles = db.query(Article).filter(Article.source_id.in_(new_source_ids)).all()
    
    haryana_relevant = 0
    for article in new_articles:
        article_text = f"{article.title} {article.content}"
        if is_haryana_relevant(article_text):
            haryana_relevant += 1
    
    print(f"   ✅ {haryana_relevant} out of {len(new_articles)} articles are Haryana-relevant")
    print(f"   📈 Relevance rate: {(haryana_relevant/len(new_articles)*100) if new_articles else 0:.1f}%")
    
    db.close()

if __name__ == "__main__":
    scrape_new_sources()

