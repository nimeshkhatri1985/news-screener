from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from haryana_config import HARYANA_FILTER_PRESETS, calculate_relevance_score, is_haryana_relevant
    HARYANA_CONFIG_AVAILABLE = True
except ImportError:
    HARYANA_CONFIG_AVAILABLE = False
    print("⚠️  Warning: Haryana configuration not available")

try:
    from twitter_service import twitter_service
    TWITTER_AVAILABLE = True
except ImportError:
    TWITTER_AVAILABLE = False
    print("⚠️  Warning: Twitter service not available")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./news_screener.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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
    keywords = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, index=True)
    content = Column(Text)
    posted_at = Column(DateTime)
    twitter_id = Column(String)
    status = Column(String, default="draft")
    platform = Column(String, default="twitter")
    post_url = Column(String)
    post_content = Column(Text)

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

class TweetRequest(BaseModel):
    article_id: int
    custom_message: Optional[str] = None
    include_hashtags: bool = True
    use_premium: bool = False

Base.metadata.create_all(bind=engine)

app = FastAPI(title="News Screener API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {
        "message": "News Screener API",
        "version": "1.0.0",
        "haryana_config": HARYANA_CONFIG_AVAILABLE,
        "twitter_available": TWITTER_AVAILABLE
    }

@app.get("/sources", response_model=List[SourceResponse])
async def get_sources(db: Session = Depends(get_db)):
    sources = db.query(Source).all()
    return sources

@app.post("/sources", response_model=SourceResponse)
async def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    db_source = Source(**source.dict())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source

@app.get("/articles", response_model=List[ArticleResponse])
async def get_articles(source_id: Optional[int] = None, limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    query = db.query(Article)
    if source_id:
        query = query.filter(Article.source_id == source_id)
    articles = query.order_by(Article.published_at.desc()).offset(offset).limit(limit).all()
    return articles

@app.get("/search", response_model=List[ArticleResponse])
async def search_articles(q: str, source_id: Optional[int] = None, limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    query = db.query(Article)
    if source_id:
        query = query.filter(Article.source_id == source_id)
    articles = query.filter((Article.title.like(f"%{q}%")) | (Article.content.like(f"%{q}%"))).order_by(Article.published_at.desc()).offset(offset).limit(limit).all()
    return articles

@app.get("/filters", response_model=List[FilterResponse])
async def get_filters(db: Session = Depends(get_db)):
    filters = db.query(Filter).all()
    return filters

@app.post("/filters", response_model=FilterResponse)
async def create_filter(filter: FilterCreate, db: Session = Depends(get_db)):
    db_filter = Filter(**filter.dict())
    db.add(db_filter)
    db.commit()
    db.refresh(db_filter)
    return db_filter

@app.get("/posts", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

@app.post("/posts", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

if HARYANA_CONFIG_AVAILABLE:
    @app.get("/haryana/filter-presets")
    async def get_haryana_filter_presets():
        presets = {}
        for key, config in HARYANA_FILTER_PRESETS.items():
            presets[key] = {"name": config["name"], "description": config["description"], "keyword_count": len(config["keywords"])}
        return presets
    
    @app.get("/haryana/articles")
    async def get_haryana_articles(filter_preset: str, source_id: Optional[int] = None, sentiment: Optional[str] = None, min_score: int = 0, limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
        if filter_preset not in HARYANA_FILTER_PRESETS:
            raise HTTPException(status_code=400, detail=f"Invalid filter preset: {filter_preset}")
        query = db.query(Article)
        if source_id:
            query = query.filter(Article.source_id == source_id)
        articles = query.order_by(Article.published_at.desc()).limit(limit * 3).all()
        scored_articles = []
        for article in articles:
            article_text = f"{article.title} {article.content}"
            if not is_haryana_relevant(article_text):
                continue
            result = calculate_relevance_score(article_text, filter_preset)
            relevance_score = result.get("score", result.get("relevance_score", 0))
            if relevance_score < min_score:
                continue
            if sentiment and result["sentiment"] != sentiment:
                continue
            article_dict = {"id": article.id, "source_id": article.source_id, "title": article.title, "content": article.content, "url": article.url, "published_at": article.published_at.isoformat(), "crawled_at": article.crawled_at.isoformat(), "relevance_score": relevance_score, "matched_keywords": result["matched_keywords"], "sentiment": result["sentiment"], "positive_matches": result.get("positive_matches", []), "negative_matches": result.get("negative_matches", [])}
            scored_articles.append(article_dict)
        scored_articles.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored_articles[:limit]
    
    @app.get("/haryana/articles/{article_id}/analyze")
    async def analyze_haryana_article(article_id: int, filter_preset: str, db: Session = Depends(get_db)):
        article = db.query(Article).filter(Article.id == article_id).first()
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        if filter_preset not in HARYANA_FILTER_PRESETS:
            raise HTTPException(status_code=400, detail=f"Invalid filter preset: {filter_preset}")
        article_text = f"{article.title} {article.content}"
        result = calculate_relevance_score(article_text, filter_preset)
        return {"article_id": article.id, "title": article.title, "filter_preset": filter_preset, "is_relevant": is_haryana_relevant(article_text), **result}

if TWITTER_AVAILABLE:
    @app.get("/twitter/status")
    async def get_twitter_status():
        return twitter_service.get_status()
    
    @app.post("/twitter/post")
    async def post_to_twitter(request: TweetRequest, db: Session = Depends(get_db)):
        article = db.query(Article).filter(Article.id == request.article_id).first()
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        article_dict = {'id': article.id, 'title': article.title, 'url': article.url, 'content': article.content[:500]}
        max_length = 4000 if request.use_premium else 280
        tweet_text = twitter_service.create_engaging_tweet(article=article_dict, custom_message=request.custom_message, include_hashtags=request.include_hashtags, max_length=max_length, use_premium=request.use_premium)
        result = twitter_service.post_tweet(tweet_text)
        if result['success']:
            db_post = Post(article_id=article.id, content=tweet_text, posted_at=datetime.utcnow(), twitter_id=result.get('tweet_id'), status='posted', platform='twitter', post_url=result.get('tweet_url'), post_content=tweet_text)
            db.add(db_post)
            db.commit()
            return {'success': True, 'tweet_id': result.get('tweet_id'), 'tweet_url': result.get('tweet_url'), 'message': 'Tweet posted successfully!'}
        else:
            raise HTTPException(status_code=500, detail=result.get('error', 'Failed to post tweet'))
    
    @app.post("/twitter/preview")
    async def preview_tweet(request: TweetRequest, db: Session = Depends(get_db)):
        article = db.query(Article).filter(Article.id == request.article_id).first()
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        article_dict = {'id': article.id, 'title': article.title, 'url': article.url, 'content': article.content[:500]}
        max_length = 4000 if request.use_premium else 280
        tweet_text = twitter_service.create_engaging_tweet(article=article_dict, custom_message=request.custom_message, include_hashtags=request.include_hashtags, max_length=max_length, use_premium=request.use_premium)
        return {'tweet_text': tweet_text, 'character_count': len(tweet_text), 'article': {'id': article.id, 'title': article.title, 'url': article.url}}

@app.post("/scrape/trigger")
async def trigger_manual_scrape():
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(__file__))
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from auto_scrape import auto_scrape
        results = auto_scrape(verbose=False)
        return {"success": True, "message": "Scraping completed successfully", "results": {"sources_scraped": results.get('sources_scraped', 0), "articles_found": results.get('articles_found', 0), "new_articles": results.get('new_articles', 0), "errors": results.get('errors', [])}}
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error during manual scrape: {error_detail}")
        raise HTTPException(status_code=500, detail=f"Failed to trigger scraping: {str(e)}")

@app.get("/scrape/status")
async def get_scrape_status(db: Session = Depends(get_db)):
    try:
        total_articles = db.query(Article).count()
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_articles = db.query(Article).filter(Article.crawled_at >= yesterday).count()
        last_hour = datetime.utcnow() - timedelta(hours=1)
        last_hour_articles = db.query(Article).filter(Article.crawled_at >= last_hour).count()
        latest_article = db.query(Article).order_by(Article.crawled_at.desc()).first()
        return {"total_articles": total_articles, "last_24h": recent_articles, "last_hour": last_hour_articles, "latest_article": {"title": latest_article.title if latest_article else None, "crawled_at": latest_article.crawled_at.isoformat() if latest_article else None} if latest_article else None, "active_sources": db.query(Source).filter(Source.is_active == True).count()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get scrape status: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
