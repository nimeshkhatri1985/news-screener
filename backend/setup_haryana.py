"""
Setup script for Haryana news screening
Adds Haryana-specific sources and filter presets to the database
"""

import os
import sys
from datetime import datetime

# Add backend directory to path
sys.path.append(os.path.dirname(__file__))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Source, Filter, Base
from haryana_config import HARYANA_NEWS_SOURCES, HARYANA_FILTER_PRESETS

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./news_screener.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_haryana_sources():
    """Add Haryana-specific news sources"""
    db = SessionLocal()
    try:
        print("Adding Haryana news sources...")
        added = 0
        
        for source_data in HARYANA_NEWS_SOURCES:
            # Check if source already exists
            existing = db.query(Source).filter(
                Source.rss_feed == source_data["rss_feed"]
            ).first()
            
            if not existing:
                source = Source(
                    name=source_data["name"],
                    url=source_data["url"],
                    rss_feed=source_data["rss_feed"],
                    is_active=source_data["is_active"],
                    created_at=datetime.utcnow()
                )
                db.add(source)
                added += 1
                print(f"  ✓ Added: {source_data['name']}")
            else:
                print(f"  - Already exists: {source_data['name']}")
        
        db.commit()
        print(f"\n✅ Successfully added {added} new sources")
        
    except Exception as e:
        print(f"❌ Error adding sources: {e}")
        db.rollback()
    finally:
        db.close()

def setup_haryana_filters():
    """Add Haryana-specific filter presets"""
    db = SessionLocal()
    try:
        print("\nAdding Haryana filter presets...")
        added = 0
        
        for key, preset in HARYANA_FILTER_PRESETS.items():
            # Check if filter already exists
            existing = db.query(Filter).filter(
                Filter.name == preset["name"]
            ).first()
            
            if not existing:
                # Combine all keywords into a comma-separated string
                keywords = ", ".join(preset["keywords"])
                
                filter_obj = Filter(
                    name=preset["name"],
                    keywords=keywords,
                    is_active=True,
                    created_at=datetime.utcnow()
                )
                db.add(filter_obj)
                added += 1
                print(f"  ✓ Added: {preset['name']}")
                print(f"    Description: {preset['description']}")
                print(f"    Keywords: {len(preset['keywords'])} keywords")
            else:
                print(f"  - Already exists: {preset['name']}")
        
        db.commit()
        print(f"\n✅ Successfully added {added} new filter presets")
        
    except Exception as e:
        print(f"❌ Error adding filters: {e}")
        db.rollback()
    finally:
        db.close()

def display_setup_summary():
    """Display summary of current setup"""
    db = SessionLocal()
    try:
        print("\n" + "="*60)
        print("HARYANA NEWS SCREENER - SETUP SUMMARY")
        print("="*60)
        
        # Count sources
        total_sources = db.query(Source).count()
        active_sources = db.query(Source).filter(Source.is_active == True).count()
        print(f"\n📰 News Sources:")
        print(f"   Total: {total_sources}")
        print(f"   Active: {active_sources}")
        
        # List sources
        sources = db.query(Source).all()
        for source in sources:
            status = "✓" if source.is_active else "✗"
            print(f"   {status} {source.name}")
        
        # Count filters
        total_filters = db.query(Filter).count()
        active_filters = db.query(Filter).filter(Filter.is_active == True).count()
        print(f"\n🔍 Filter Presets:")
        print(f"   Total: {total_filters}")
        print(f"   Active: {active_filters}")
        
        # List filters
        filters = db.query(Filter).all()
        for f in filters:
            status = "✓" if f.is_active else "✗"
            keyword_count = len(f.keywords.split(','))
            print(f"   {status} {f.name} ({keyword_count} keywords)")
        
        print("\n" + "="*60)
        print("\n✅ Setup complete! You can now:")
        print("   1. Start the backend: cd backend && python3 main.py")
        print("   2. Start the frontend: cd frontend && npm start")
        print("   3. Use filter presets to find specific types of news")
        print("\n💡 Filter Preset Categories:")
        for key, preset in HARYANA_FILTER_PRESETS.items():
            print(f"   • {preset['name']}: {preset['description']}")
        
    except Exception as e:
        print(f"❌ Error displaying summary: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("\n🚀 Setting up Haryana News Screener...\n")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Setup sources and filters
    setup_haryana_sources()
    setup_haryana_filters()
    
    # Display summary
    display_setup_summary()
    
    print("\n✨ All done!\n")

