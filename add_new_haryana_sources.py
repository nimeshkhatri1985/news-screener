"""
Add new Haryana news sources to the database
"""
import sys
sys.path.append('backend')

from main import SessionLocal, Source
from datetime import datetime

def add_new_sources():
    db = SessionLocal()
    
    new_sources = [
        {
            "name": "Haryana Today",
            "url": "https://haryanatoday.in/",
            "rss_feed": "https://haryanatoday.in/feed/",
            "is_active": True
        },
        {
            "name": "Haryana Chronicle",
            "url": "https://haryanachronicle.com/",
            "rss_feed": "https://haryanachronicle.com/feed/",
            "is_active": True
        },
        {
            "name": "Top Haryana",
            "url": "https://topharyana.in/",
            "rss_feed": "https://topharyana.in/feed/",
            "is_active": True
        },
        {
            "name": "Invest Haryana",
            "url": "https://investharyana.in/",
            "rss_feed": "https://investharyana.in/feed/",
            "is_active": True
        }
    ]
    
    print("Adding new Haryana news sources...")
    print("=" * 60)
    
    added_count = 0
    for source_data in new_sources:
        # Check if source already exists
        existing = db.query(Source).filter(Source.name == source_data["name"]).first()
        
        if existing:
            print(f"⚠️  {source_data['name']} already exists (ID: {existing.id})")
            continue
        
        # Add new source
        source = Source(
            name=source_data["name"],
            url=source_data["url"],
            rss_feed=source_data["rss_feed"],
            is_active=source_data["is_active"],
            created_at=datetime.utcnow()
        )
        
        db.add(source)
        db.commit()
        db.refresh(source)
        
        print(f"✅ Added: {source.name}")
        print(f"   URL: {source.url}")
        print(f"   RSS: {source.rss_feed}")
        print(f"   ID: {source.id}")
        print()
        added_count += 1
    
    print("=" * 60)
    print(f"✅ Successfully added {added_count} new sources!")
    
    # Show all Haryana sources
    print("\n📰 All Haryana News Sources:")
    print("=" * 60)
    
    haryana_keywords = ['haryana', 'chandigarh']
    all_sources = db.query(Source).filter(Source.is_active == True).all()
    
    haryana_sources = [s for s in all_sources if any(kw in s.name.lower() for kw in haryana_keywords)]
    
    for i, source in enumerate(haryana_sources, 1):
        print(f"{i}. {source.name} (ID: {source.id})")
        print(f"   RSS: {source.rss_feed}")
    
    print(f"\nTotal active Haryana sources: {len(haryana_sources)}")
    
    db.close()

if __name__ == "__main__":
    add_new_sources()

