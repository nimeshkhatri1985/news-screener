from celery import Celery
import os

# Celery configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

celery_app = Celery(
    "news_screener",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task
def scrape_news_sources():
    """Celery task to scrape all news sources"""
    from scraper import NewsScraper
    
    scraper = NewsScraper()
    saved_count = scraper.scrape_all_sources()
    
    return {
        "status": "success",
        "articles_saved": saved_count,
        "timestamp": "2024-01-01T00:00:00Z"  # You'd use datetime.utcnow().isoformat()
    }

# Schedule periodic tasks
celery_app.conf.beat_schedule = {
    "scrape-news-every-30-minutes": {
        "task": "celery_tasks.scrape_news_sources",
        "schedule": 30.0 * 60.0,  # 30 minutes
    },
}

celery_app.conf.timezone = "UTC"

if __name__ == "__main__":
    celery_app.start()
