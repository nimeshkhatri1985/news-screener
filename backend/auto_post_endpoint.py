"""
Auto-Posting to Twitter Endpoint
This endpoint will be called daily by GitHub Actions to automatically post
the best Haryana news articles to Twitter.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
import logging

from main import get_db, Article
from twitter_service import twitter_service
from haryana_config import calculate_relevance_score, is_haryana_relevant, HARYANA_FILTER_PRESETS

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/haryana/auto-post")
async def auto_post_to_twitter(
    filter_preset: str = "tourism",
    num_posts: int = 3,
    min_score: int = 50,
    db: Session = Depends(get_db)
):
    """
    Automatically post top articles to Twitter
    
    Args:
        filter_preset: Which category to post (tourism, infrastructure, etc.)
        num_posts: Number of articles to post (default: 3)
        min_score: Minimum relevance score (default: 50)
    
    Returns:
        dict with post results
    """
    
    if not twitter_service.is_configured():
        raise HTTPException(status_code=500, detail="Twitter API not configured")
    
    if filter_preset not in HARYANA_FILTER_PRESETS:
        raise HTTPException(status_code=400, detail=f"Invalid filter preset: {filter_preset}")
    
    # Get articles from last 24 hours
    yesterday = datetime.utcnow() - timedelta(days=1)
    articles = db.query(Article).filter(Article.published_at >= yesterday).all()
    
    scored_articles = []
    for article in articles:
        article_text = f"{article.title} {article.content}"
        
        # Check if article is Haryana-relevant
        if not is_haryana_relevant(article_text):
            continue
        
        # Calculate relevance score
        result = calculate_relevance_score(article_text, filter_preset)
        score = result.get("score", 0)
        
        # Filter by minimum score and positive sentiment only
        if score < min_score or result.get("sentiment") != "positive":
            continue
        
        scored_articles.append({
            "article": article,
            "score": score,
            "relevance": result
        })
    
    # Sort by score and get top N
    scored_articles.sort(key=lambda x: x["score"], reverse=True)
    top_articles = scored_articles[:num_posts]
    
    if not top_articles:
        return {
            "success": True,
            "message": "No articles found matching criteria",
            "posts_made": 0,
            "articles_checked": len(articles),
            "articles_scored": len(scored_articles)
        }
    
    # Check which articles have already been posted (to avoid duplicates)
    already_posted_urls = set()
    
    # Post to Twitter
    posts_made = []
    errors = []
    
    for article_data in top_articles:
        article = article_data["article"]
        
        # Check if already posted
        from main import Post
        existing = db.query(Post).filter(
            Post.article_id == article.id,
            Post.platform == "twitter"
        ).first()
        
        if existing:
            logger.info(f"Skipping article {article.id} - already posted")
            continue
        
        # Create tweet content
        article_dict = {
            'id': article.id,
            'title': article.title,
            'url': article.url,
            'content': article.content[:500] if article.content else "",
            'matched_keywords': article_data["relevance"].get("matched_keywords", []),
            'sentiment': article_data["relevance"].get("sentiment", "positive")
        }
        
        try:
            # Generate tweet using premium format
            tweet_text = twitter_service.create_engaging_tweet(
                article=article_dict,
                include_hashtags=True,
                use_premium=True
            )
            
            # Post to Twitter
            result = twitter_service.post_tweet(tweet_text, article_id=article.id)
            
            if result['success']:
                # Save to database
                db_post = Post(
                    article_id=article.id,
                    content=tweet_text,
                    posted_at=datetime.utcnow(),
                    twitter_id=result.get('tweet_id'),
                    status='posted',
                    platform='twitter',
                    post_url=result.get('tweet_url'),
                    post_content=tweet_text
                )
                db.add(db_post)
                db.commit()
                
                posts_made.append({
                    "article_id": article.id,
                    "title": article.title,
                    "tweet_url": result.get('tweet_url'),
                    "score": article_data["score"]
                })
                
                logger.info(f"Posted article {article.id} to Twitter: {result.get('tweet_url')}")
                
            else:
                errors.append({
                    "article_id": article.id,
                    "error": result.get('error', 'Unknown error')
                })
                logger.error(f"Failed to post article {article.id}: {result.get('error')}")
                
        except Exception as e:
            errors.append({
                "article_id": article.id,
                "error": str(e)
            })
            logger.error(f"Error posting article {article.id}: {str(e)}")
    
    return {
        "success": True,
        "posts_made": len(posts_made),
        "errors": len(errors),
        "details": posts_made,
        "error_details": errors,
        "articles_checked": len(articles),
        "articles_scored": len(scored_articles),
        "filter_preset": filter_preset
    }

