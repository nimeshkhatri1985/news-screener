#!/usr/bin/env python3
"""
Test script to verify tweet format without Key Highlights section
"""
import sys
sys.path.append('backend')

from twitter_service import TwitterService

# Sample Haryana article with positive matches
sample_article = {
    "id": 1,
    "title": "New Heritage Walk Inaugurated in Kurukshetra to Boost Tourism",
    "content": """The Haryana Tourism Department inaugurated a new heritage walk in Kurukshetra yesterday, 
    featuring ancient temples and the historic Brahma Sarovar. The initiative aims to attract more tourists 
    and showcase the rich cultural heritage of Haryana. Local guides will be available to explain the 
    historical significance of each site. The project received an investment of Rs 50 crore and is expected 
    to benefit local businesses significantly.""",
    "url": "https://example.com/haryana/tourism/1",
    "matched_keywords": ["tourism", "heritage", "kurukshetra", "temple"],
    "positive_matches": ["Launch", "Launched", "New", "inaugurate", "boost"],  # These should be filtered
    "relevance_score": 120.0,
    "sentiment": "positive"
}

# Initialize service
twitter_service = TwitterService()

print("=" * 80)
print("TESTING TWEET FORMAT (Premium/Long-form)")
print("=" * 80)

# Test premium format
tweet_text = twitter_service.create_engaging_tweet_premium(
    article=sample_article,
    include_hashtags=True,
    include_summary=True,
    max_length=4000
)

print("\n📝 GENERATED TWEET:\n")
print(tweet_text)
print("\n" + "=" * 80)
print(f"Tweet Length: {len(tweet_text)} characters")
print("=" * 80)

# Check if unwanted text is present
unwanted_phrases = ["✅ Key Highlights:", "Launch", "Launched", "New"]
found_issues = []

for phrase in unwanted_phrases:
    if phrase in tweet_text:
        found_issues.append(phrase)

if found_issues:
    print(f"\n❌ FOUND UNWANTED TEXT: {', '.join(found_issues)}")
else:
    print(f"\n✅ SUCCESS: No unwanted text found!")

print("\n" + "=" * 80)

