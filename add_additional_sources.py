"""
One-time helper script to add additional Haryana-focused sources.
Run with: python3 add_additional_sources.py
"""

from pathlib import Path
import sys
from urllib.parse import quote_plus
from datetime import datetime

BACKEND_DIR = Path(__file__).resolve().parent / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from main import SessionLocal, Source  # type: ignore


def google_news_feed(site: str, extra_terms: str = "") -> str:
    terms = "Haryana"
    if extra_terms:
        terms = f"{terms} {extra_terms}"
    query = quote_plus(f"{terms} site:{site}")
    return (
        f"https://news.google.com/rss/search?q={query}"
        "&hl=en-IN&gl=IN&ceid=IN:en"
    )


NEW_SOURCES = [
    {
        "name": "YourStory (Haryana)",
        "url": "https://yourstory.com",
        "rss": "https://yourstory.com/tag/haryana/feed",
    },
    {
        "name": "Inc42 (Haryana)",
        "url": "https://inc42.com",
        "rss": "https://inc42.com/?s=Haryana&feed=rss2",
    },
    {
        "name": "Startup India (Haryana)",
        "url": "https://www.startupindia.gov.in",
        "rss": google_news_feed("startupindia.gov.in"),
    },
    {
        "name": "Startup Talky (Haryana)",
        "url": "https://startuptalky.com",
        "rss": google_news_feed("startuptalky.com"),
    },
    {
        "name": "Indian Startup News (Haryana)",
        "url": "https://www.indianstartupnews.com",
        "rss": google_news_feed("indianstartupnews.com"),
    },
    {
        "name": "Way2World (Haryana)",
        "url": "https://www.way2world.in",
        "rss": google_news_feed("way2world.in"),
    },
    {
        "name": "FeedSpot (Haryana)",
        "url": "https://www.feedspot.com",
        "rss": google_news_feed("feedspot.com"),
    },
    {
        "name": "StartupBlink (Haryana)",
        "url": "https://www.startupblink.com",
        "rss": google_news_feed("startupblink.com"),
    },
    {
        "name": "Economic Times (Haryana)",
        "url": "https://economictimes.indiatimes.com",
        "rss": google_news_feed("economictimes.indiatimes.com"),
    },
    {
        "name": "Business Standard (Haryana)",
        "url": "https://www.business-standard.com",
        "rss": google_news_feed("business-standard.com"),
    },
    {
        "name": "IndiaTimes (Haryana)",
        "url": "https://www.indiatimes.com",
        "rss": google_news_feed("indiatimes.com"),
    },
    {
        "name": "Aaj Tak (Haryana)",
        "url": "https://www.aajtak.in",
        "rss": google_news_feed("aajtak.in"),
    },
    {
        "name": "PM GatiShakti (Haryana)",
        "url": "https://www.pmgatishakti.gov.in",
        "rss": google_news_feed("pmgatishakti.gov.in"),
    },
    {
        "name": "Infrastructure Today (Haryana)",
        "url": "https://infrastructuretoday.co.in",
        "rss": "https://infrastructuretoday.co.in/feed/",
    },
    {
        "name": "Construction World (Haryana)",
        "url": "https://www.constructionworld.in",
        "rss": "https://www.constructionworld.in/rss",
    },
    {
        "name": "InfraBazaar (Haryana)",
        "url": "https://www.infrabazaar.com",
        "rss": google_news_feed("infrabazaar.com"),
    },
    {
        "name": "ET Infra (Haryana)",
        "url": "https://etinfra.com",
        "rss": google_news_feed("etinfra.com"),
    },
    {
        "name": "NDTV (Haryana)",
        "url": "https://www.ndtv.com",
        "rss": google_news_feed("ndtv.com"),
    },
    {
        "name": "The Better India (Haryana)",
        "url": "https://www.thebetterindia.com",
        "rss": "https://www.thebetterindia.com/feed/",
    },
    {
        "name": "IndiaSpend (Haryana)",
        "url": "https://www.indiaspend.com",
        "rss": "https://www.indiaspend.com/feed/",
    },
    {
        "name": "LiveMint (Haryana)",
        "url": "https://www.livemint.com",
        "rss": google_news_feed("livemint.com"),
    },
    {
        "name": "Scroll (Haryana)",
        "url": "https://scroll.in",
        "rss": "https://scroll.in/rss",
    },
    {
        "name": "India Together (Haryana)",
        "url": "https://indiatogether.org",
        "rss": "https://indiatogether.org/feeds/all.xml",
    },
    {
        "name": "YourStory Social (Haryana)",
        "url": "https://yourstory.com",
        "rss": "https://yourstory.com/category/socialstories/feed",
    },
]


def add_sources():
    db = SessionLocal()
    added = 0
    try:
        for source in NEW_SOURCES:
            existing = (
                db.query(Source)
                .filter(Source.name == source["name"])
                .first()
            )
            if existing:
                continue
            db_source = Source(
                name=source["name"],
                url=source["url"],
                rss_feed=source["rss"],
                is_active=True,
                created_at=datetime.utcnow(),
            )
            db.add(db_source)
            added += 1
        db.commit()
        print(f"Added {added} new sources.")
    finally:
        db.close()


if __name__ == "__main__":
    add_sources()

