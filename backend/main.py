from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict
import os

# Import Haryana-specific configuration
try:
    from haryana_config import (
        HARYANA_FILTER_PRESETS, 
        calculate_relevance_score, 
        is_haryana_relevant
    )
    HARYANA_CONFIG_AVAILABLE = True
except ImportError:
    HARYANA_CONFIG_AVAILABLE = False
    print("⚠️  Warning: Haryana configuration not available")

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./news_screener.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class Source(Base):
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    url = Column(String)
    rss_feed = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    url = Column(String, unique=True, index=True)
    published_at = Column(DateTime)
    crawled_at = Column(DateTime, default=datetime.utcnow)

class Filter(Base):
    __tablename__ = "filters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    keywords = Column(Text)  # JSON string of keywords
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, index=True)
    content = Column(Text)
    posted_at = Column(DateTime)
    twitter_id = Column(String)
    status = Column(String, default="draft")  # draft, posted, failed

# Pydantic Models
class SourceCreate(BaseModel):
    name: str
    url: str
    rss_feed: str

class SourceResponse(BaseModel):
    id: int
    name: str
    url: str
    rss_feed: str
    is_active: bool
    created_at: datetime

class ArticleResponse(BaseModel):
    id: int
    source_id: int
    title: str
    content: str
    url: str
    published_at: datetime
    crawled_at: datetime

class ArticleWithScoreResponse(BaseModel):
    id: int
    source_id: int
    title: str
    content: str
    url: str
    published_at: datetime
    crawled_at: datetime
    relevance_score: Optional[float] = None
    matched_keywords: Optional[List[str]] = None
    sentiment: Optional[str] = None
    positive_matches: Optional[List[str]] = None
    negative_matches: Optional[List[str]] = None

class FilterCreate(BaseModel):
    name: str
    keywords: str

class FilterResponse(BaseModel):
    id: int
    name: str
    keywords: str
    is_active: bool
    created_at: datetime

class PostCreate(BaseModel):
    article_id: int
    content: str

class PostResponse(BaseModel):
    id: int
    article_id: int
    content: str
    posted_at: Optional[datetime]
    twitter_id: Optional[str]
    status: str

# FastAPI app
app = FastAPI(title="News Screener API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
Base.metadata.create_all(bind=engine)

# API Routes
@app.get("/")
async def root():
    return {"message": "News Screener API"}

@app.get("/sources", response_model=List[SourceResponse])
async def get_sources(db: Session = Depends(get_db)):
    sources = db.query(Source).filter(Source.is_active == True).all()
    return sources

@app.post("/sources", response_model=SourceResponse)
async def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    db_source = Source(**source.dict())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source

@app.get("/articles", response_model=List[ArticleResponse])
async def get_articles(
    source_id: Optional[int] = None,
    keywords: Optional[str] = None,
    category: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(Article)
    
    # Filter by source
    if source_id:
        query = query.filter(Article.source_id == source_id)
    
    # Filter by keywords (search in title and content)
    if keywords:
        keyword_list = [kw.strip().lower() for kw in keywords.split(',')]
        for keyword in keyword_list:
            query = query.filter(
                db.or_(
                    Article.title.ilike(f'%{keyword}%'),
                    Article.content.ilike(f'%{keyword}%')
                )
            )
    
    # Filter by category (if we add category field later)
    if category:
        query = query.filter(Article.title.ilike(f'%{category}%'))
    
    # Filter by date range
    if date_from:
        try:
            from_date = datetime.fromisoformat(date_from)
            query = query.filter(Article.published_at >= from_date)
        except ValueError:
            pass
    
    if date_to:
        try:
            to_date = datetime.fromisoformat(date_to)
            query = query.filter(Article.published_at <= to_date)
        except ValueError:
            pass
    
    articles = query.order_by(Article.published_at.desc()).offset(offset).limit(limit).all()
    return articles

@app.get("/filters", response_model=List[FilterResponse])
async def get_filters(db: Session = Depends(get_db)):
    filters = db.query(Filter).filter(Filter.is_active == True).all()
    return filters

@app.post("/filters", response_model=FilterResponse)
async def create_filter(filter_data: FilterCreate, db: Session = Depends(get_db)):
    db_filter = Filter(**filter_data.dict())
    db.add(db_filter)
    db.commit()
    db.refresh(db_filter)
    return db_filter

@app.get("/search", response_model=List[ArticleResponse])
async def search_articles(
    q: str,
    source_id: Optional[int] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Full-text search across articles"""
    query = db.query(Article)
    
    # Filter by source if specified
    if source_id:
        query = query.filter(Article.source_id == source_id)
    
    # Search in title and content
    search_term = f'%{q.lower()}%'
    query = query.filter(
        db.or_(
            Article.title.ilike(search_term),
            Article.content.ilike(search_term)
        )
    )
    
    articles = query.order_by(Article.published_at.desc()).offset(offset).limit(limit).all()
    return articles

@app.get("/posts", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.posted_at.desc()).all()
    return posts

@app.post("/posts", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Haryana-specific endpoints
@app.get("/haryana/filter-presets")
async def get_haryana_filter_presets():
    """Get available Haryana filter presets"""
    if not HARYANA_CONFIG_AVAILABLE:
        raise HTTPException(status_code=503, detail="Haryana configuration not available")
    
    # Return simplified preset information
    presets = {}
    for key, preset in HARYANA_FILTER_PRESETS.items():
        presets[key] = {
            "name": preset["name"],
            "description": preset["description"],
            "keyword_count": len(preset["keywords"])
        }
    return presets

@app.get("/haryana/articles", response_model=List[ArticleWithScoreResponse])
async def get_haryana_articles(
    filter_preset: str,
    source_id: Optional[int] = None,
    sentiment: Optional[str] = None,  # positive, negative, neutral
    min_score: Optional[int] = 0,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get articles filtered and scored for Haryana-specific topics
    
    Args:
        filter_preset: One of tourism, infrastructure, economy, education, agriculture, sports, environment, governance
        source_id: Optional source filter
        sentiment: Filter by sentiment (positive, negative, neutral)
        min_score: Minimum relevance score
        limit: Number of results
        offset: Pagination offset
    """
    if not HARYANA_CONFIG_AVAILABLE:
        raise HTTPException(status_code=503, detail="Haryana configuration not available")
    
    if filter_preset not in HARYANA_FILTER_PRESETS:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid filter preset. Available: {', '.join(HARYANA_FILTER_PRESETS.keys())}"
        )
    
    # Get articles
    query = db.query(Article)
    
    if source_id:
        query = query.filter(Article.source_id == source_id)
    
    articles = query.order_by(Article.published_at.desc()).all()
    
    # Score and filter articles
    scored_articles = []
    for article in articles:
        article_text = f"{article.title} {article.content}"
        
        # Check if article is Haryana-relevant
        if not is_haryana_relevant(article_text):
            continue
        
        # Calculate relevance score
        score_data = calculate_relevance_score(article_text, filter_preset)
        
        # Filter by minimum score
        if score_data["score"] < min_score:
            continue
        
        # Filter by sentiment if specified
        if sentiment and score_data["sentiment"] != sentiment:
            continue
        
        # Create enhanced response
        scored_article = ArticleWithScoreResponse(
            id=article.id,
            source_id=article.source_id,
            title=article.title,
            content=article.content,
            url=article.url,
            published_at=article.published_at,
            crawled_at=article.crawled_at,
            relevance_score=score_data["score"],
            matched_keywords=score_data["matched_keywords"],
            sentiment=score_data["sentiment"],
            positive_matches=score_data.get("positive_matches", []),
            negative_matches=score_data.get("negative_matches", [])
        )
        scored_articles.append(scored_article)
    
    # Sort by relevance score
    scored_articles.sort(key=lambda x: x.relevance_score, reverse=True)
    
    # Apply pagination
    return scored_articles[offset:offset + limit]

@app.get("/haryana/articles/{article_id}/analyze")
async def analyze_haryana_article(
    article_id: int,
    filter_preset: str,
    db: Session = Depends(get_db)
):
    """Analyze a specific article against a Haryana filter preset"""
    if not HARYANA_CONFIG_AVAILABLE:
        raise HTTPException(status_code=503, detail="Haryana configuration not available")
    
    if filter_preset not in HARYANA_FILTER_PRESETS:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid filter preset. Available: {', '.join(HARYANA_FILTER_PRESETS.keys())}"
        )
    
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    article_text = f"{article.title} {article.content}"
    
    # Check Haryana relevance
    haryana_relevant = is_haryana_relevant(article_text)
    
    # Calculate score
    score_data = calculate_relevance_score(article_text, filter_preset)
    
    return {
        "article_id": article_id,
        "article_title": article.title,
        "filter_preset": filter_preset,
        "haryana_relevant": haryana_relevant,
        "relevance_score": score_data["score"],
        "sentiment": score_data["sentiment"],
        "matched_keywords": score_data["matched_keywords"],
        "positive_matches": score_data.get("positive_matches", []),
        "negative_matches": score_data.get("negative_matches", []),
        "analysis": {
            "keyword_matches": len(score_data["matched_keywords"]),
            "positive_indicators": len(score_data.get("positive_matches", [])),
            "negative_indicators": len(score_data.get("negative_matches", []))
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
