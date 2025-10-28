"""
Twitter Integration Service
Handles posting articles to Twitter using Twitter API v2
Enhanced with image support, URL shortening, and optimized tweet generation
"""
import os
import tweepy
import requests
from typing import Dict, Optional, List
from datetime import datetime
import logging
import re
from bs4 import BeautifulSoup
from io import BytesIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLShortener:
    """URL shortening service using TinyURL (free, no API key) or Bitly (with API key)"""
    
    @staticmethod
    def shorten_with_tinyurl(url: str) -> str:
        """
        Shorten URL using TinyURL (free, no API key required)
        
        Args:
            url: Original URL to shorten
        
        Returns:
            Shortened URL or original URL if shortening fails
        """
        try:
            api_url = f"http://tinyurl.com/api-create.php?url={url}"
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                short_url = response.text.strip()
                logger.info(f"✂️  Shortened URL: {url} -> {short_url}")
                return short_url
            else:
                logger.warning(f"⚠️  TinyURL failed with status {response.status_code}")
                return url
        except Exception as e:
            logger.warning(f"⚠️  URL shortening failed: {str(e)}")
            return url
    
    @staticmethod
    def shorten_with_bitly(url: str, api_token: Optional[str] = None) -> str:
        """
        Shorten URL using Bitly (requires API token)
        
        Args:
            url: Original URL to shorten
            api_token: Bitly API token (optional, from env)
        
        Returns:
            Shortened URL or original URL if shortening fails
        """
        if not api_token:
            api_token = os.getenv('BITLY_API_TOKEN')
        
        if not api_token:
            logger.warning("⚠️  Bitly API token not configured, falling back to TinyURL")
            return URLShortener.shorten_with_tinyurl(url)
        
        try:
            headers = {
                'Authorization': f'Bearer {api_token}',
                'Content-Type': 'application/json'
            }
            data = {
                'long_url': url,
                'domain': 'bit.ly'
            }
            response = requests.post(
                'https://api-ssl.bitly.com/v4/shorten',
                json=data,
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200 or response.status_code == 201:
                short_url = response.json().get('link')
                logger.info(f"✂️  Shortened URL (Bitly): {url} -> {short_url}")
                return short_url
            else:
                logger.warning(f"⚠️  Bitly failed with status {response.status_code}")
                return URLShortener.shorten_with_tinyurl(url)
        except Exception as e:
            logger.warning(f"⚠️  Bitly URL shortening failed: {str(e)}, trying TinyURL")
            return URLShortener.shorten_with_tinyurl(url)
    
    @staticmethod
    def shorten_url(url: str, service: str = 'tinyurl') -> str:
        """
        Shorten URL using specified service
        
        Args:
            url: Original URL to shorten
            service: 'tinyurl' or 'bitly' (default: tinyurl)
        
        Returns:
            Shortened URL
        """
        if service.lower() == 'bitly':
            return URLShortener.shorten_with_bitly(url)
        else:
            return URLShortener.shorten_with_tinyurl(url)


class TwitterService:
    """Service for posting to Twitter"""
    
    def __init__(self):
        """Initialize Twitter API client"""
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        # URL shortening service ('tinyurl' or 'bitly')
        self.url_shortener_service = os.getenv('URL_SHORTENER_SERVICE', 'tinyurl')
        self.use_url_shortening = os.getenv('USE_URL_SHORTENING', 'true').lower() == 'true'
        
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Twitter API client"""
        try:
            if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
                logger.warning("Twitter credentials not configured. Set environment variables:")
                logger.warning("  TWITTER_API_KEY, TWITTER_API_SECRET")
                logger.warning("  TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET")
                return
            
            # Initialize Twitter API v2 client
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                wait_on_rate_limit=True
            )
            
            # Initialize API v1.1 for media upload (required for images)
            auth = tweepy.OAuth1UserHandler(
                self.api_key, 
                self.api_secret,
                self.access_token, 
                self.access_token_secret
            )
            self.api_v1 = tweepy.API(auth)
            
            logger.info("✅ Twitter API client initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Twitter client: {str(e)}")
            self.client = None
            self.api_v1 = None
    
    def is_configured(self) -> bool:
        """Check if Twitter API is properly configured"""
        return self.client is not None
    
    def get_status(self) -> Dict:
        """Get Twitter service status"""
        configured = self.is_configured()
        return {
            'configured': configured,
            'message': 'Twitter API configured and ready' if configured else 'Twitter API not configured'
        }
    
    def extract_images_from_article(self, article_url: str, max_images: int = 1) -> List[str]:
        """
        Extract image URLs from article page
        
        Args:
            article_url: URL of the article
            max_images: Maximum number of images to extract (free tier: 1-4)
        
        Returns:
            List of image URLs
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(article_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            image_urls = []
            
            # Look for Open Graph image first (usually the main image)
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                image_urls.append(og_image['content'])
            
            # Look for Twitter card image
            if len(image_urls) < max_images:
                twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
                if twitter_image and twitter_image.get('content'):
                    img_url = twitter_image['content']
                    if img_url not in image_urls:
                        image_urls.append(img_url)
            
            # Look for article images
            if len(image_urls) < max_images:
                for img in soup.find_all('img', limit=10):
                    src = img.get('src') or img.get('data-src')
                    if src and len(image_urls) < max_images:
                        # Filter out small images (likely icons/logos)
                        if not any(x in src.lower() for x in ['logo', 'icon', 'avatar', 'button']):
                            # Make absolute URL if relative
                            if src.startswith('//'):
                                src = 'https:' + src
                            elif src.startswith('/'):
                                from urllib.parse import urljoin
                                src = urljoin(article_url, src)
                            
                            if src.startswith('http') and src not in image_urls:
                                image_urls.append(src)
            
            logger.info(f"📸 Found {len(image_urls)} images from {article_url}")
            return image_urls[:max_images]
            
        except Exception as e:
            logger.warning(f"⚠️  Could not extract images from {article_url}: {str(e)}")
            return []
    
    def upload_media(self, image_url: str) -> Optional[str]:
        """
        Upload media to Twitter and return media_id
        
        Args:
            image_url: URL of the image to upload
        
        Returns:
            Media ID string or None if upload fails
        """
        if not hasattr(self, 'api_v1') or not self.api_v1:
            logger.warning("⚠️  Twitter API v1.1 not initialized, cannot upload media")
            return None
        
        try:
            # Download image
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Upload to Twitter
            media = self.api_v1.media_upload(
                filename='image.jpg',
                file=BytesIO(response.content)
            )
            
            logger.info(f"✅ Media uploaded successfully: {media.media_id_string}")
            return media.media_id_string
            
        except Exception as e:
            logger.warning(f"⚠️  Failed to upload media from {image_url}: {str(e)}")
            return None
    
    def generate_engaging_summary(self, article: Dict, max_sentences: int = 3) -> str:
        """
        Generate an engaging summary from article content
        
        Args:
            article: Article dictionary with title and content
            max_sentences: Maximum number of sentences in summary
        
        Returns:
            Engaging summary text
        """
        content = article.get('content', '')
        title = article.get('title', '')
        
        if not content:
            return ""
        
        # Split content into sentences
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
        
        # Extract key information sentences (those with positive indicators and numbers)
        # Note: Removed generic words like 'launch', 'new' as per user preference
        key_sentences = []
        positive_words = ['inaugurate', 'develop', 'improve', 'boost', 
                         'attract', 'increase', 'record', 'success', 'achieve', 'milestone',
                         'expand', 'grow', 'invest', 'create', 'approve', 'complete',
                         'benefit', 'enhance', 'modern', 'advanced', 'quality']
        
        for sentence in sentences[:10]:  # Check first 10 sentences
            sentence_lower = sentence.lower()
            # Prioritize sentences with numbers or positive indicators
            has_number = any(char.isdigit() for char in sentence)
            has_positive = any(word in sentence_lower for word in positive_words)
            
            if has_number or has_positive:
                key_sentences.append(sentence)
                if len(key_sentences) >= max_sentences:
                    break
        
        # If we don't have enough key sentences, add more
        if len(key_sentences) < max_sentences:
            for sentence in sentences:
                if sentence not in key_sentences and len(sentence) > 30:
                    key_sentences.append(sentence)
                    if len(key_sentences) >= max_sentences:
                        break
        
        # Create engaging summary
        summary = '. '.join(key_sentences[:max_sentences])
        if summary and not summary.endswith('.'):
            summary += '.'
        
        return summary
    
    def create_engaging_tweet_premium(
        self,
        article: Dict,
        custom_message: Optional[str] = None,
        include_hashtags: bool = True,
        include_summary: bool = True,
        max_length: int = 4000
    ) -> str:
        """
        Create an engaging, informative tweet for PAID Twitter accounts (up to 4000 chars)
        Includes article summary so readers get value without clicking
        
        Args:
            article: Article dictionary
            custom_message: Optional custom intro message
            include_hashtags: Whether to include hashtags
            include_summary: Whether to include article summary
            max_length: Maximum tweet length (4000 for paid accounts)
        
        Returns:
            Optimized long-form tweet text
        """
        title = article.get('title', '')
        url = article.get('url', '')
        content = article.get('content', '')
        
        # Build comprehensive hashtags for better reach
        hashtags = []
        if include_hashtags:
            hashtags = ['#Haryana']
            
            # Add category-specific Haryana hashtags based on article content
            matched_keywords = article.get('matched_keywords', [])
            matched_keywords_lower = [kw.lower() for kw in matched_keywords]
            
            # Check for tourism-related keywords
            if any(any(term in kw for term in ['tourism', 'heritage', 'tourist', 'monument', 'temple', 'fort', 'festival']) for kw in matched_keywords_lower):
                hashtags.extend(['#HaryanaTourism', '#Tourism', '#IncredibleHaryana'])
            # Check for infrastructure-related keywords
            elif any(any(term in kw for term in ['infrastructure', 'metro', 'highway', 'road', 'bridge', 'construction', 'flyover', 'expressway']) for kw in matched_keywords_lower):
                hashtags.extend(['#HaryanaInfrastructure', '#Development', '#Infrastructure', '#SmartCity'])
            # Check for business-related keywords
            elif any(any(term in kw for term in ['business', 'investment', 'startup', 'economy', 'company', 'industry', 'manufacturing', 'factory']) for kw in matched_keywords_lower):
                hashtags.extend(['#HaryanaBusiness', '#Business', '#Investment', '#EconomicGrowth'])
            # Check for education-related keywords
            elif any(any(term in kw for term in ['education', 'school', 'university', 'college', 'student', 'skill']) for kw in matched_keywords_lower):
                hashtags.extend(['#HaryanaEducation', '#Education', '#SkillDevelopment'])
            # Check for agriculture-related keywords
            elif any(any(term in kw for term in ['agriculture', 'farmer', 'crop', 'farming']) for kw in matched_keywords_lower):
                hashtags.extend(['#HaryanaAgriculture', '#Agriculture', '#Farming'])
            # Check for sports-related keywords
            elif any(any(term in kw for term in ['sports', 'athlete', 'medal', 'championship']) for kw in matched_keywords_lower):
                hashtags.extend(['#HaryanaSports', '#Sports', '#Athletes'])
            # Check for environment-related keywords
            elif any(any(term in kw for term in ['environment', 'green', 'pollution', 'tree', 'clean']) for kw in matched_keywords_lower):
                hashtags.extend(['#HaryanaEnvironment', '#Environment', '#GreenHaryana'])
            # Check for governance-related keywords
            elif any(any(term in kw for term in ['governance', 'government', 'policy', 'scheme', 'minister']) for kw in matched_keywords_lower):
                hashtags.extend(['#HaryanaGovernance', '#Governance', '#PublicService'])
            else:
                # Default category-specific hashtag
                hashtags.append('#HaryanaNews')
            
            # Add India-related hashtags for broader reach
            hashtags.extend(['#India', '#MakeInIndia'])
            
            # Remove duplicates while preserving order
            seen = set()
            hashtags = [x for x in hashtags if not (x in seen or seen.add(x))]
        
        # Build tweet components
        tweet_parts = []
        
        # 1. Custom message (if provided)
        if custom_message:
            tweet_parts.append(f"✨ {custom_message}\n")
        
        # 2. Title with emoji for visual appeal
        title_emoji = "🎯"
        matched_keywords = article.get('matched_keywords', [])
        if any(kw in ['tourism', 'heritage'] for kw in matched_keywords):
            title_emoji = "🏛️"
        elif any(kw in ['infrastructure', 'metro', 'highway'] for kw in matched_keywords):
            title_emoji = "🚇"
        elif any(kw in ['business', 'investment'] for kw in matched_keywords):
            title_emoji = "💼"
        elif any(kw in ['education'] for kw in matched_keywords):
            title_emoji = "📚"
        
        tweet_parts.append(f"{title_emoji} {title}\n")
        
        # 3. Engaging summary (key feature for paid accounts)
        if include_summary and content:
            summary = self.generate_engaging_summary(article, max_sentences=4)
            if summary:
                tweet_parts.append(f"📰 {summary}\n")
        
        # Note: Key Highlights section removed as per user preference
        
        # 4. Hashtags
        if hashtags:
            # Group hashtags nicely (max 10 for readability)
            hashtag_text = ' '.join(hashtags[:10])
            tweet_parts.append(f"\n{hashtag_text}")
        
        # 5. Call to action and link (with URL shortening)
        if url:
            # Shorten URL if enabled
            display_url = url
            if self.use_url_shortening:
                display_url = URLShortener.shorten_url(url, self.url_shortener_service)
            tweet_parts.append(f"\n📖 Read full story: {display_url}")
        
        # Join all parts
        tweet = '\n'.join(tweet_parts)
        
        # Ensure we don't exceed max length (should rarely happen with 4000 chars)
        if len(tweet) > max_length:
            # Intelligently truncate summary if needed
            if include_summary:
                # Reduce summary and try again
                summary = self.generate_engaging_summary(article, max_sentences=2)
                tweet_parts[2] = f"📰 {summary}\n" if summary else ""
                tweet = '\n'.join(filter(None, tweet_parts))
            
            # Final truncation if still too long
            if len(tweet) > max_length:
                tweet = tweet[:max_length-3] + '...'
        
        return tweet
    
    def create_engaging_tweet(
        self,
        article: Dict,
        custom_message: Optional[str] = None,
        include_hashtags: bool = True,
        max_length: int = 280,
        use_premium: bool = False
    ) -> str:
        """
        Create an engaging tweet - automatically uses premium format if use_premium=True
        
        Args:
            article: Article dictionary
            custom_message: Optional custom intro message
            include_hashtags: Whether to include hashtags
            max_length: Maximum tweet length (280 for free, 4000 for paid)
            use_premium: Whether to use premium long-form format
        
        Returns:
            Optimized tweet text
        """
        if use_premium or max_length > 280:
            return self.create_engaging_tweet_premium(
                article=article,
                custom_message=custom_message,
                include_hashtags=include_hashtags,
                max_length=max_length
            )
        
        # Original short-form tweet for free accounts
        title = article.get('title', '')
        url = article.get('url', '')
        
        # Twitter URL shortening: URLs are counted as 23 characters
        url_length = 23 if url else 0
        
        # Build hashtags (keep it minimal for free accounts)
        hashtags = []
        if include_hashtags:
            hashtags = ['#Haryana']
            
            # Add category-specific Haryana hashtag based on keywords
            matched_keywords = article.get('matched_keywords', [])
            matched_keywords_lower = [kw.lower() for kw in matched_keywords]
            
            if any(any(term in kw for term in ['tourism', 'heritage', 'tourist', 'monument', 'temple']) for kw in matched_keywords_lower):
                hashtags.append('#HaryanaTourism')
            elif any(any(term in kw for term in ['infrastructure', 'metro', 'highway', 'road', 'bridge', 'construction']) for kw in matched_keywords_lower):
                hashtags.append('#HaryanaInfrastructure')
            elif any(any(term in kw for term in ['business', 'investment', 'startup', 'economy', 'company']) for kw in matched_keywords_lower):
                hashtags.append('#HaryanaBusiness')
            elif any(any(term in kw for term in ['education', 'school', 'university', 'college']) for kw in matched_keywords_lower):
                hashtags.append('#HaryanaEducation')
            elif any(any(term in kw for term in ['agriculture', 'farmer', 'crop']) for kw in matched_keywords_lower):
                hashtags.append('#HaryanaAgriculture')
            elif any(any(term in kw for term in ['sports', 'athlete', 'medal']) for kw in matched_keywords_lower):
                hashtags.append('#HaryanaSports')
            elif any(any(term in kw for term in ['environment', 'green', 'tree']) for kw in matched_keywords_lower):
                hashtags.append('#HaryanaEnvironment')
            elif any(any(term in kw for term in ['governance', 'government', 'policy']) for kw in matched_keywords_lower):
                hashtags.append('#HaryanaGovernance')
            else:
                hashtags.append('#HaryanaNews')
        
        hashtag_text = ' '.join(hashtags) if hashtags else ''
        hashtag_length = len(hashtag_text) + 2 if hashtag_text else 0  # +2 for spacing
        
        # Calculate available space for content
        available_for_content = max_length - url_length - hashtag_length - 4  # -4 for spacing/newlines
        
        # Add custom message if provided
        if custom_message:
            # Keep custom message brief
            custom_message = custom_message[:80]
            tweet_parts = [custom_message]
            available_for_content -= len(custom_message) + 2
        else:
            tweet_parts = []
        
        # Add title (truncate if needed)
        if len(title) > available_for_content:
            # Smart truncation at word boundary
            truncated = title[:available_for_content-3].rsplit(' ', 1)[0] + '...'
            tweet_parts.append(truncated)
        else:
            tweet_parts.append(title)
        
        # Build final tweet (with URL shortening)
        display_url = url
        if url and self.use_url_shortening:
            display_url = URLShortener.shorten_url(url, self.url_shortener_service)
        
        tweet_components = []
        if tweet_parts:
            tweet_components.append('\n\n'.join(tweet_parts))
        if hashtag_text:
            tweet_components.append(hashtag_text)
        if display_url:
            tweet_components.append(display_url)
        
        tweet = '\n\n'.join(tweet_components)
        
        # Final safety check
        if len(tweet) > max_length:
            tweet = tweet[:max_length-3] + '...'
        
        return tweet
    
    def create_tweet_text(
        self, 
        article: Dict, 
        max_length: int = 280,
        include_hashtags: bool = True,
        custom_message: Optional[str] = None
    ) -> str:
        """
        Create tweet text from article
        
        Args:
            article: Article dictionary with title, url, etc.
            max_length: Maximum tweet length (default 280)
            include_hashtags: Whether to include hashtags
            custom_message: Optional custom message to prepend
        
        Returns:
            Formatted tweet text
        """
        title = article.get('title', '')
        url = article.get('url', '')
        
        # Build hashtags
        hashtags = []
        if include_hashtags:
            hashtags = ['#Haryana', '#HaryanaNews']
            
            # Add category-specific hashtags if available
            if article.get('category'):
                category = article['category'].replace(' ', '')
                hashtags.append(f'#{category}')
        
        # Build tweet components
        components = []
        
        if custom_message:
            components.append(custom_message)
        
        components.append(title)
        
        if hashtags:
            components.append(' '.join(hashtags))
        
        if url:
            components.append(url)
        
        # Join and truncate if needed
        tweet = '\n\n'.join(components)
        
        # Truncate title if tweet is too long
        if len(tweet) > max_length:
            # Calculate available space for title
            other_parts = '\n\n'.join([c for c in components if c != title])
            available = max_length - len(other_parts) - 10  # 10 for ellipsis and spacing
            
            if available > 50:  # Only truncate if we have reasonable space
                truncated_title = title[:available] + '...'
                tweet = '\n\n'.join([
                    c if c != title else truncated_title 
                    for c in components
                ])
        
        return tweet[:max_length]
    
    def post_tweet(
        self, 
        text: str,
        article_id: Optional[int] = None,
        media_ids: Optional[List[str]] = None
    ) -> Dict:
        """
        Post a tweet to Twitter with optional media
        
        Args:
            text: Tweet text
            article_id: Optional article ID for tracking
            media_ids: Optional list of media IDs to attach
        
        Returns:
            Dictionary with success status and tweet info
        """
        if not self.is_configured():
            return {
                'success': False,
                'error': 'Twitter API not configured',
                'message': 'Please set Twitter API credentials in environment variables'
            }
        
        try:
            # Post the tweet with optional media
            response = self.client.create_tweet(
                text=text,
                media_ids=media_ids if media_ids else None
            )
            
            tweet_id = response.data['id']
            tweet_url = f"https://twitter.com/user/status/{tweet_id}"
            
            media_info = f" with {len(media_ids)} image(s)" if media_ids else ""
            logger.info(f"✅ Tweet posted successfully{media_info}: {tweet_url}")
            
            return {
                'success': True,
                'tweet_id': tweet_id,
                'tweet_url': tweet_url,
                'article_id': article_id,
                'posted_at': datetime.utcnow().isoformat(),
                'message': f'Tweet posted successfully{media_info}',
                'has_media': bool(media_ids)
            }
            
        except tweepy.TweepyException as e:
            logger.error(f"❌ Twitter API error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'article_id': article_id,
                'message': f'Failed to post tweet: {str(e)}'
            }
        except Exception as e:
            logger.error(f"❌ Unexpected error posting tweet: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'article_id': article_id,
                'message': f'Unexpected error: {str(e)}'
            }
    
    def post_article_to_twitter(
        self,
        article: Dict,
        custom_message: Optional[str] = None,
        include_hashtags: bool = True,
        include_images: bool = True,
        use_premium: bool = True  # Default to premium format
    ) -> Dict:
        """
        Post an article to Twitter with optimized text and images
        
        Args:
            article: Article dictionary
            custom_message: Optional custom message
            include_hashtags: Whether to include hashtags
            include_images: Whether to try to include images from article
            use_premium: Whether to use premium long-form format (default: True)
        
        Returns:
            Dictionary with post result
        """
        # Create engaging tweet text (premium or standard)
        tweet_text = self.create_engaging_tweet(
            article=article,
            custom_message=custom_message,
            include_hashtags=include_hashtags,
            use_premium=use_premium
        )
        
        # Try to extract and upload images
        media_ids = []
        if include_images and article.get('url'):
            try:
                image_urls = self.extract_images_from_article(article['url'], max_images=1)
                for img_url in image_urls:
                    media_id = self.upload_media(img_url)
                    if media_id:
                        media_ids.append(media_id)
                        break  # For free tier, use 1 image
            except Exception as e:
                logger.warning(f"⚠️  Could not process images: {str(e)}")
        
        # Post to Twitter
        result = self.post_tweet(
            text=tweet_text,
            article_id=article.get('id'),
            media_ids=media_ids if media_ids else None
        )
        
        result['tweet_text'] = tweet_text
        result['images_attached'] = len(media_ids)
        
        return result
    
    def verify_credentials(self) -> Dict:
        """
        Verify Twitter API credentials
        
        Returns:
            Dictionary with verification status
        """
        if not self.is_configured():
            return {
                'success': False,
                'message': 'Twitter API not configured'
            }
        
        try:
            # Try to get authenticated user info
            me = self.client.get_me()
            
            return {
                'success': True,
                'user_id': me.data.id,
                'username': me.data.username,
                'name': me.data.name,
                'message': 'Twitter credentials verified successfully'
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to verify credentials: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to verify Twitter credentials'
            }


# Create singleton instance
twitter_service = TwitterService()

