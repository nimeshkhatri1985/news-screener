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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsScraper:
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
            
            articles = []
            for entry in feed.entries:
                article_data = {
                    'source_id': source_id,
                    'title': entry.get('title', ''),
                    'url': entry.get('link', ''),
                    'published_at': self._parse_date(entry.get('published', '')),
                    'content': self._extract_content(entry)
                }
                articles.append(article_data)
            
            logger.info(f"Found {len(articles)} articles from {rss_url}")
            return articles
            
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

def main():
    """Main function for testing"""
    scraper = NewsScraper()
    scraper.scrape_all_sources()

if __name__ == "__main__":
    main()
