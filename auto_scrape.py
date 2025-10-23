#!/usr/bin/env python3
"""
Automated scraping script for continuous news updates
Can be run manually or scheduled with cron/task scheduler
"""

import os
import sys
import time
from datetime import datetime, timedelta

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from scraper import NewsScraper
from main import SessionLocal, Source, Article
from haryana_config import is_haryana_relevant

def get_stats(db):
    """Get database statistics"""
    total_articles = db.query(Article).count()
    
    # Count Haryana-relevant articles
    haryana_count = 0
    recent_articles = db.query(Article).order_by(Article.crawled_at.desc()).limit(100).all()
    
    for article in recent_articles:
        article_text = f"{article.title} {article.content}"
        if is_haryana_relevant(article_text):
            haryana_count += 1
    
    # Get recent article count (last 24 hours)
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_count = db.query(Article).filter(Article.crawled_at >= yesterday).count()
    
    return {
        'total': total_articles,
        'haryana_relevant': haryana_count,
        'last_24h': recent_count
    }

def auto_scrape(verbose=True):
    """
    Automatically scrape news from all active sources
    
    Args:
        verbose: Print detailed output (default True)
    
    Returns:
        dict: Scraping results
    """
    if verbose:
        print(f"\n{'='*70}")
        print(f"🤖 AUTO SCRAPER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
    
    db = SessionLocal()
    scraper = NewsScraper()
    results = {
        'timestamp': datetime.now().isoformat(),
        'sources_scraped': 0,
        'articles_found': 0,
        'new_articles': 0,
        'errors': []
    }
    
    try:
        # Get statistics before scraping
        if verbose:
            print("📊 Current database status:")
            stats_before = get_stats(db)
            print(f"   • Total articles: {stats_before['total']}")
            print(f"   • Haryana-relevant (sample): ~{stats_before['haryana_relevant']}%")
            print(f"   • Added in last 24h: {stats_before['last_24h']}")
            print()
        
        # Get active sources
        sources = db.query(Source).filter(Source.is_active == True).all()
        
        if not sources:
            if verbose:
                print("❌ No active sources configured!")
            results['errors'].append("No active sources")
            return results
        
        if verbose:
            print(f"🔍 Scraping {len(sources)} news sources...")
            print()
        
        # Scrape each source
        for source in sources:
            results['sources_scraped'] += 1
            
            try:
                if verbose:
                    print(f"   [{results['sources_scraped']}/{len(sources)}] {source.name}...", end=' ')
                
                articles = scraper.scrape_rss_feed(source.rss_feed, source.id)
                saved_count = scraper.save_articles(articles)
                
                results['articles_found'] += len(articles)
                results['new_articles'] += saved_count
                
                if verbose:
                    if saved_count > 0:
                        print(f"✅ +{saved_count} new")
                    elif len(articles) > 0:
                        print(f"✓ {len(articles)} checked, none new")
                    else:
                        print("⚠️ no articles")
                
                # Small delay between sources
                time.sleep(1)
                
            except Exception as e:
                error_msg = f"Error scraping {source.name}: {str(e)}"
                results['errors'].append(error_msg)
                if verbose:
                    print(f"❌ Error: {str(e)}")
        
        # Get statistics after scraping
        if verbose:
            print()
            print(f"{'='*70}")
            print("📊 SCRAPING RESULTS")
            print(f"{'='*70}")
            stats_after = get_stats(db)
            print(f"\n✅ Sources scraped: {results['sources_scraped']}")
            print(f"✅ Articles checked: {results['articles_found']}")
            print(f"✅ New articles saved: {results['new_articles']}")
            print(f"\n📈 Database status:")
            print(f"   • Total articles: {stats_after['total']} (+{stats_after['total'] - stats_before['total']})")
            print(f"   • Haryana-relevant: ~{stats_after['haryana_relevant']}% of recent articles")
            
            if results['errors']:
                print(f"\n⚠️  Errors encountered: {len(results['errors'])}")
                for error in results['errors']:
                    print(f"   • {error}")
            
            print(f"\n{'='*70}")
            
            if results['new_articles'] > 0:
                print("✨ New articles are ready to view!")
                print("   → Open http://localhost:3000/haryana")
            else:
                print("✓ All articles are up to date")
            
            print(f"{'='*70}\n")
        
    except Exception as e:
        error_msg = f"Fatal error during scraping: {str(e)}"
        results['errors'].append(error_msg)
        if verbose:
            print(f"\n❌ {error_msg}")
            import traceback
            traceback.print_exc()
    finally:
        db.close()
    
    return results

def continuous_scrape(interval_minutes=60):
    """
    Continuously scrape news at specified intervals
    
    Args:
        interval_minutes: Minutes between scraping runs (default 60)
    """
    print(f"\n🤖 CONTINUOUS AUTO SCRAPER STARTED")
    print(f"{'='*70}")
    print(f"⏱️  Interval: Every {interval_minutes} minutes")
    print(f"⏹️  Press Ctrl+C to stop")
    print(f"{'='*70}\n")
    
    try:
        while True:
            auto_scrape(verbose=True)
            
            next_run = datetime.now() + timedelta(minutes=interval_minutes)
            print(f"⏳ Next scrape at: {next_run.strftime('%H:%M:%S')}")
            print(f"   (Sleeping for {interval_minutes} minutes...)\n")
            
            time.sleep(interval_minutes * 60)
            
    except KeyboardInterrupt:
        print(f"\n\n{'='*70}")
        print("⏹️  Auto scraper stopped by user")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Automated Haryana news scraper')
    parser.add_argument('--continuous', action='store_true', 
                       help='Run continuously at specified intervals')
    parser.add_argument('--interval', type=int, default=60,
                       help='Minutes between scraping runs (default: 60)')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress detailed output')
    
    args = parser.parse_args()
    
    if args.continuous:
        continuous_scrape(interval_minutes=args.interval)
    else:
        auto_scrape(verbose=not args.quiet)

