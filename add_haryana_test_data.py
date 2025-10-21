"""
Add sample Haryana-related articles for testing the filtering system
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Article, Source, Base

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./news_screener.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sample articles for different categories
SAMPLE_ARTICLES = [
    # Tourism & Heritage
    {
        "title": "New Heritage Walk Inaugurated in Kurukshetra to Boost Tourism",
        "content": "The Haryana Tourism Department launched a new heritage walk in Kurukshetra yesterday, featuring ancient temples and the historic Brahma Sarovar. The initiative aims to attract more tourists and showcase the rich cultural heritage of Haryana. Local guides will be available to explain the historical significance of each site.",
        "category": "tourism"
    },
    {
        "title": "Surajkund Mela Attracts Record Number of Visitors This Year",
        "content": "The annual Surajkund International Crafts Mela in Faridabad witnessed a record footfall this year, with over 1 million visitors. The festival showcased handicrafts from across India and featured cultural performances. Tourism Minister announced plans to expand the festival grounds for next year.",
        "category": "tourism"
    },
    {
        "title": "Vintage Car Museum in Gurugram Becomes Major Tourist Attraction",
        "content": "The recently opened vintage car museum in Heritage Transport Museum, Gurugram, has become a popular destination for tourists. The museum displays over 100 classic cars and has already attracted more than 50,000 visitors since its inauguration three months ago.",
        "category": "tourism"
    },
    
    # Infrastructure
    {
        "title": "New Metro Line Connecting Gurugram to Faridabad Approved",
        "content": "Haryana government has approved the construction of a new metro line connecting Gurugram to Faridabad, improving connectivity between the two major cities. The 25-kilometer line will have 15 stations and is expected to be completed within three years. This infrastructure project will enhance public transport in the region.",
        "category": "infrastructure"
    },
    {
        "title": "Six-Lane Expressway Between Delhi and Chandigarh Nears Completion",
        "content": "The ambitious six-lane expressway project between Delhi and Chandigarh through Haryana is 85% complete. The new highway will reduce travel time by 2 hours and improve road connectivity. Officials announced that the expressway will be inaugurated next quarter.",
        "category": "infrastructure"
    },
    {
        "title": "Smart City Project in Karnal Shows Progress with Digital Infrastructure",
        "content": "Karnal's smart city initiative has made significant progress with the installation of smart streetlights, WiFi hotspots, and digital payment systems across the city. The urban development project aims to improve quality of life and enhance connectivity for residents.",
        "category": "infrastructure"
    },
    
    # Economy
    {
        "title": "Major IT Company Opens New Office in Gurugram, Creates 5000 Jobs",
        "content": "A leading technology company has inaugurated its new campus in Gurugram, Haryana, creating 5000 employment opportunities. The investment of Rs 1000 crore demonstrates Haryana's growing importance as an IT hub. The company plans to expand further in the coming years.",
        "category": "economy"
    },
    {
        "title": "Haryana Attracts Rs 5000 Crore Investment in Manufacturing Sector",
        "content": "During the recent investor summit, Haryana government signed MOUs worth Rs 5000 crore in the manufacturing sector. The investment will create over 10,000 jobs and strengthen Haryana's industrial base. Multiple companies from automotive, electronics, and consumer goods sectors participated.",
        "category": "economy"
    },
    {
        "title": "Startup Ecosystem in Gurugram Grows with New Incubator Launch",
        "content": "A new startup incubator was launched in Gurugram to support technology entrepreneurs. The facility will provide mentorship, funding support, and workspace to innovative startups. The initiative aims to boost Haryana's startup ecosystem and create employment opportunities.",
        "category": "economy"
    },
    
    # Education
    {
        "title": "IIT Delhi Opens New Campus in Sonipat to Expand Educational Opportunities",
        "content": "Indian Institute of Technology (IIT) Delhi has inaugurated its new satellite campus in Sonipat, Haryana. The campus will offer specialized courses in artificial intelligence and data science. This expansion will provide quality higher education opportunities to students in the region.",
        "category": "education"
    },
    {
        "title": "Haryana Students Win National Science Competition",
        "content": "A team of students from Gurugram won the prestigious National Science Olympiad, bringing laurels to Haryana. The achievement showcases the improving quality of science education in the state. The winning team will represent India at the International Science Fair.",
        "category": "education"
    },
    {
        "title": "New Skill Development Center Inaugurated in Panipat",
        "content": "A state-of-the-art skill development center was inaugurated in Panipat to provide vocational training to youth. The center will offer courses in IT, manufacturing, and hospitality sectors. The initiative aims to enhance employability of local youth.",
        "category": "education"
    },
    
    # Agriculture
    {
        "title": "Haryana Farmers Report Bumper Wheat Harvest This Season",
        "content": "Farmers across Haryana have reported a record wheat harvest this year, with yields exceeding expectations. The success is attributed to improved irrigation facilities, quality seeds, and favorable weather conditions. Agricultural experts credit modern farming techniques and government support schemes.",
        "category": "agriculture"
    },
    {
        "title": "New Agricultural Technology Center Opens in Hisar",
        "content": "A modern agricultural research and technology center was inaugurated in Hisar to help farmers adopt advanced farming methods. The center will provide training on precision agriculture, drone technology, and organic farming. This initiative aims to improve crop yields and farmer income.",
        "category": "agriculture"
    },
    
    # Sports
    {
        "title": "Haryana Wrestler Wins Gold Medal at Asian Championships",
        "content": "A young wrestler from Rohtak, Haryana, won the gold medal at the Asian Wrestling Championships. The achievement adds to Haryana's rich legacy in wrestling. The state government announced a cash award and job opportunity for the champion athlete.",
        "category": "sports"
    },
    {
        "title": "New Sports Academy Launched in Panchkula for Olympic Training",
        "content": "A world-class sports academy focused on Olympic sports was launched in Panchkula. The facility includes state-of-the-art training equipment and international coaches. The academy will nurture young talent in athletics, boxing, and wrestling.",
        "category": "sports"
    },
    
    # Environment
    {
        "title": "Haryana Plants 5 Million Trees in Massive Green Drive",
        "content": "Haryana government's ambitious tree plantation drive has successfully planted 5 million saplings across the state. The initiative aims to improve air quality and increase green cover. Citizens and volunteers participated enthusiastically in the environmental campaign.",
        "category": "environment"
    },
    {
        "title": "Gurugram Sees Improvement in Air Quality After Anti-Pollution Measures",
        "content": "Air quality in Gurugram has shown improvement following strict anti-pollution measures implemented by the government. The measures include increased monitoring, traffic management, and industrial emission controls. Environmental agencies report a 20% reduction in pollution levels.",
        "category": "environment"
    },
    {
        "title": "Solar Energy Park Inaugurated in Haryana to Boost Renewable Power",
        "content": "A large-scale solar energy park was inaugurated in Haryana, adding 500 MW of renewable energy capacity. The project demonstrates the state's commitment to sustainable development and clean energy. Officials announced plans for more solar projects across the state.",
        "category": "environment"
    },
    
    # Governance
    {
        "title": "Haryana Launches Digital Platform for Citizen Services",
        "content": "The state government launched a comprehensive digital platform offering over 100 government services online. Citizens can now apply for certificates, licenses, and permits from home. The e-governance initiative aims to improve transparency and reduce bureaucratic delays.",
        "category": "governance"
    },
    {
        "title": "New Welfare Scheme Announced for Farmers in Haryana",
        "content": "Haryana Chief Minister announced a new welfare scheme providing financial assistance and insurance coverage to small farmers. The initiative will benefit over 500,000 farming families across the state. The scheme includes provisions for crop insurance and direct benefit transfer.",
        "category": "governance"
    }
]

def add_sample_articles():
    """Add sample Haryana articles to the database"""
    db = SessionLocal()
    try:
        # Get an active source (preferably a Haryana source)
        source = db.query(Source).filter(Source.is_active == True).first()
        
        if not source:
            print("❌ No active source found. Please run setup_haryana.py first.")
            return
        
        print(f"Using source: {source.name}")
        print("\nAdding sample Haryana articles...\n")
        
        added = 0
        for i, article_data in enumerate(SAMPLE_ARTICLES):
            # Generate a unique URL
            article_url = f"https://example.com/haryana/{article_data['category']}/{i+1}"
            
            # Check if article already exists
            existing = db.query(Article).filter(Article.url == article_url).first()
            if existing:
                print(f"  - Already exists: {article_data['title'][:50]}...")
                continue
            
            # Create article with a date in the past week
            days_ago = random.randint(0, 7)
            published_date = datetime.utcnow() - timedelta(days=days_ago)
            
            article = Article(
                source_id=source.id,
                title=article_data['title'],
                content=article_data['content'],
                url=article_url,
                published_at=published_date,
                crawled_at=datetime.utcnow()
            )
            
            db.add(article)
            added += 1
            print(f"  ✓ Added [{article_data['category']}]: {article_data['title'][:60]}...")
        
        db.commit()
        print(f"\n✅ Successfully added {added} sample articles")
        print(f"\n📊 Total articles in database: {db.query(Article).count()}")
        
        print("\n" + "="*70)
        print("Sample data added! You can now:")
        print("  1. Start the backend: cd backend && python3 main.py")
        print("  2. Start the frontend: cd frontend && npm start")
        print("  3. Go to http://localhost:3000/haryana")
        print("  4. Try different filter presets to see the articles")
        print("="*70)
        
    except Exception as e:
        print(f"❌ Error adding articles: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("\n🚀 Adding sample Haryana test data...\n")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Add sample articles
    add_sample_articles()
    
    print("\n✨ Done!\n")

