import feedparser
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from datetime import datetime
import time
import logging
from typing import List, Dict
import re

from main import Article, Source, SessionLocal
from haryana_config import (
    HARYANA_FILTER_PRESETS,
    HARYANA_LOCATIONS,
    calculate_relevance_score,
    is_haryana_relevant,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsScraper:
    HIGH_IMPACT_KEYWORDS = [
        "investment",
        "invests",
        "invest",
        "crore",
        "lakh",
        "jobs",
        "employment",
        "employed",
        "startup",
        "funding",
        "scheme",
        "benefit",
        "benefits",
        "beneficiaries",
        "subsidy",
        "loan waiver",
        "incentive",
        "plant",
        "factory",
        "manufacturing",
        "production",
        "inaugur",
        "launch",
        "portal",
        "app",
        "hospital",
        "school",
        "college",
        "university",
        "training",
        "skill",
        "renewable",
        "solar",
        "wind",
        "metro",
        "highway",
        "expressway",
        "airport",
        "rail",
        "power",
        "electric",
        "smart city",
        "development",
        "water supply",
        "sanitation",
        "medal",
        "gold",
        "champion",
        "record",
        "award",
        "recognition",
        "startup hub",
        "msme",
        "cluster",
        "infra",
        "infrastructure",
        "loan",
        "credit",
        "women",
        "youth",
        "entrepreneur",
        "innovation",
        "skill centre",
        "cow shed",
        "dairy",
        "irrigation",
        "canal",
        "clean energy",
        "biogas",
        "electric bus",
        "manufacturing unit",
        "industrial park",
    ]

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_rss_feed(self, rss_url: str, source_id: int) -> List[Dict]:
        """Scrape articles from an RSS feed"""
        try:
            logger.info(f"Scraping RSS feed: {rss_url}")
            feed = feedparser.parse(rss_url)
            
            scored_articles = []
            for entry in feed.entries:
                article_data = {
                    'source_id': source_id,
                    'title': entry.get('title', ''),
                    'url': entry.get('link', ''),
                    'published_at': self._parse_date(entry.get('published', '')),
                    'content': self._extract_content(entry)
                }
                positivity_score = self._calculate_positivity_score(
                    article_data.get('title', ''),
                    article_data.get('content', '')
                )
                scored_articles.append((positivity_score, article_data))
            
            logger.info(f"Found {len(scored_articles)} articles from {rss_url}")
            
            # Sort by positivity score first, then by newest publish date
            scored_articles.sort(
                key=lambda item: (
                    item[0],
                    item[1].get('published_at') or datetime.utcnow()
                ),
                reverse=True
            )
            
            positive_articles = [
                item[1] for item in scored_articles
                if item[0] is not None and item[0] > float('-inf')
            ]
            
            if not positive_articles:
                logger.info(f"No clearly positive articles found for source {source_id}; skipping.")
                return []
            
            limited_articles = positive_articles[:3]
            logger.info(f"Limiting to top {len(limited_articles)} positive articles for source {source_id}")
            return limited_articles
            
        except Exception as e:
            logger.error(f"Error scraping RSS feed {rss_url}: {str(e)}")
            return []
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse various date formats from RSS feeds"""
        if not date_str:
            return datetime.utcnow()
        
        try:
            # Try parsing common RSS date formats
            date_formats = [
                '%a, %d %b %Y %H:%M:%S %z',
                '%a, %d %b %Y %H:%M:%S %Z',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%dT%H:%M:%S%z',
                '%Y-%m-%dT%H:%M:%SZ'
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            # If all else fails, return current time
            return datetime.utcnow()
            
        except Exception:
            return datetime.utcnow()
    
    def _extract_content(self, entry) -> str:
        """Extract content from RSS entry"""
        # Try different content fields
        content_fields = ['content', 'summary', 'description']
        
        for field in content_fields:
            if hasattr(entry, field) and entry[field]:
                content = entry[field]
                if isinstance(content, list) and content:
                    content = content[0].get('value', '')
                
                # Clean HTML tags
                soup = BeautifulSoup(content, 'html.parser')
                return soup.get_text().strip()
        
        return ''
    
    def scrape_article_content(self, url: str) -> str:
        """Scrape full article content from URL"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Try to find main content
            content_selectors = [
                'article',
                '.article-content',
                '.post-content',
                '.entry-content',
                '.content',
                'main'
            ]
            
            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    return content_element.get_text().strip()
            
            # Fallback to body text
            return soup.get_text().strip()
            
        except Exception as e:
            logger.error(f"Error scraping article content from {url}: {str(e)}")
            return ''
    
    def save_articles(self, articles: List[Dict]) -> int:
        """Save articles to database"""
        db = SessionLocal()
        saved_count = 0
        
        try:
            for article_data in articles:
                # Check if article already exists
                existing = db.query(Article).filter(Article.url == article_data['url']).first()
                if existing:
                    continue

                # Ensure Haryana relevance (title/content)
                article_text = f"{article_data.get('title', '')} {article_data.get('content', '')}"
                if not is_haryana_relevant(article_text):
                    # Try fetching full article content once before skipping
                    full_content = self.scrape_article_content(article_data['url'])
                    if full_content:
                        article_data['content'] = full_content
                        article_text = f"{article_data.get('title', '')} {full_content}"
                    if not is_haryana_relevant(article_text):
                        continue
                
                if not self._is_primary_haryana_story(article_data.get('title', ''), article_text):
                    continue
                
                # Create new article
                article = Article(**article_data)
                db.add(article)
                saved_count += 1
            
            db.commit()
            logger.info(f"Saved {saved_count} new articles")
            
        except Exception as e:
            logger.error(f"Error saving articles: {str(e)}")
            db.rollback()
        finally:
            db.close()
        
        return saved_count
    
    def scrape_all_sources(self) -> int:
        """Scrape all active sources"""
        db = SessionLocal()
        total_saved = 0
        
        try:
            sources = db.query(Source).filter(Source.is_active == True).all()
            
            for source in sources:
                if source.rss_feed:
                    articles = self.scrape_rss_feed(source.rss_feed, source.id)
                    saved_count = self.save_articles(articles)
                    total_saved += saved_count
                    
                    # Small delay between sources
                    time.sleep(1)
            
            logger.info(f"Total articles saved: {total_saved}")
            
        except Exception as e:
            logger.error(f"Error scraping sources: {str(e)}")
        finally:
            db.close()
        
        return total_saved

    def _calculate_positivity_score(self, title: str, content: str) -> float:
        """Calculate a positivity-oriented score using all Haryana presets"""
        article_text = f"{title} {content or ''}"
        best_positive: tuple[float, dict] | None = None
        
        for preset_key in HARYANA_FILTER_PRESETS.keys():
            result = calculate_relevance_score(article_text, preset_key)
            score = result.get('score', 0)
            sentiment = result.get('sentiment')
            
            if sentiment == "positive":
                if best_positive is None or score > best_positive[0]:
                    best_positive = (score, result)
        
        if not best_positive:
            return float('-inf')
        
        score, result = best_positive
        positive_matches = result.get("positive_matches", [])
        negative_matches = result.get("negative_matches", [])
        
        if negative_matches:
            return float('-inf')
        
        # Require at least two positive indicators or a very high score
        if len(positive_matches) < 2 and score < 140:
            return float('-inf')
        
        if score < 100:
            return float('-inf')
        
        if not self._has_high_impact_indicator(article_text):
            return float('-inf')
        
        return score

    def _has_high_impact_indicator(self, text: str) -> bool:
        text_lower = text.lower()
        for keyword in self.HIGH_IMPACT_KEYWORDS:
            if keyword in text_lower:
                return True
        if re.search(r"(₹|rs\.?\s?\d|inr\.?\s?\d|\d+\s?(crore|lakhs?|jobs|families|beneficiaries|students|mw|km|units|villages|districts))", text_lower):
            return True
        return False

    def _is_primary_haryana_story(self, title: str, full_text: str) -> bool:
        """Ensure Haryana mention is central, not incidental"""
        title_lower = title.lower()
        text_lower = full_text.lower()
        location_hits = 0
        for location in HARYANA_LOCATIONS:
            loc = location.lower()
            if loc in title_lower:
                return True
            count = text_lower.count(loc)
            location_hits += count
            if count > 1:
                return True
        first_chunk = text_lower[:200]
        for location in HARYANA_LOCATIONS:
            if location.lower() in first_chunk:
                return True
        return False

def main():
    """Main function for testing"""
    scraper = NewsScraper()
    scraper.scrape_all_sources()

if __name__ == "__main__":
    main()
