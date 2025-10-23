"""
Test Twitter Integration
Run this to verify Twitter API setup without posting
"""
import sys
import os

# Add backend to path
sys.path.append('backend')

# Set test environment variables if not set
if not os.getenv('TWITTER_API_KEY'):
    print("⚠️  Twitter credentials not found in environment")
    print("This is expected if you haven't set them up yet.")
    print("\nTo test with real credentials, create backend/.env with:")
    print("  TWITTER_API_KEY=your_key")
    print("  TWITTER_API_SECRET=your_secret")
    print("  TWITTER_ACCESS_TOKEN=your_token")
    print("  TWITTER_ACCESS_TOKEN_SECRET=your_token_secret")
    print("  TWITTER_BEARER_TOKEN=your_bearer_token")
    print("\nSee TWITTER_SETUP_GUIDE.md for detailed instructions.")
    print()

try:
    from twitter_service import twitter_service
    
    print("=" * 70)
    print("🐦 TWITTER INTEGRATION TEST")
    print("=" * 70)
    print()
    
    # Check if configured
    is_configured = twitter_service.is_configured()
    print(f"✓ Twitter Service Loaded: Yes")
    print(f"✓ API Configured: {'Yes' if is_configured else 'No'}")
    print()
    
    if is_configured:
        print("🔍 Verifying credentials...")
        verification = twitter_service.verify_credentials()
        
        if verification['success']:
            print(f"✅ Credentials Verified!")
            print(f"   Username: @{verification['username']}")
            print(f"   Name: {verification['name']}")
            print()
        else:
            print(f"❌ Verification Failed: {verification.get('message')}")
            print()
    else:
        print("ℹ️  Twitter API not configured (this is okay for testing)")
        print()
    
    # Test tweet generation
    print("-" * 70)
    print("📝 Testing Tweet Generation")
    print("-" * 70)
    print()
    
    test_article = {
        'id': 1,
        'title': 'New Heritage Walk Inaugurated in Kurukshetra to Boost Tourism',
        'url': 'https://example.com/haryana/tourism/1',
        'content': 'The Haryana Tourism Department launched a new heritage walk...'
    }
    
    tweet_text = twitter_service.create_tweet_text(
        article=test_article,
        include_hashtags=True
    )
    
    print(f"Generated Tweet ({len(tweet_text)} characters):")
    print()
    print("┌" + "─" * 68 + "┐")
    for line in tweet_text.split('\n'):
        print(f"│ {line:<66} │")
    print("└" + "─" * 68 + "┘")
    print()
    
    # Test with custom message
    tweet_with_message = twitter_service.create_tweet_text(
        article=test_article,
        custom_message="🌟 Great news for Haryana tourism!",
        include_hashtags=True
    )
    
    print(f"With Custom Message ({len(tweet_with_message)} characters):")
    print()
    print("┌" + "─" * 68 + "┐")
    for line in tweet_with_message.split('\n'):
        print(f"│ {line:<66} │")
    print("└" + "─" * 68 + "┘")
    print()
    
    print("=" * 70)
    print("✅ TWITTER INTEGRATION TEST COMPLETE")
    print("=" * 70)
    print()
    
    if is_configured:
        print("🎉 Your Twitter integration is ready to use!")
        print()
        print("Next steps:")
        print("  1. Start the backend: cd backend && python3 main.py")
        print("  2. Test the API: curl http://localhost:8000/twitter/status")
        print("  3. Preview a tweet: curl -X POST http://localhost:8000/twitter/preview \\")
        print("       -H 'Content-Type: application/json' \\")
        print("       -d '{\"article_id\": 1}'")
    else:
        print("📚 To enable Twitter posting:")
        print("  1. Follow the setup guide in TWITTER_SETUP_GUIDE.md")
        print("  2. Get your Twitter API credentials")
        print("  3. Add them to backend/.env")
        print("  4. Restart the backend")
    print()

except ImportError as e:
    print(f"❌ Error importing twitter_service: {e}")
    print()
    print("Make sure you've installed tweepy:")
    print("  pip3 install tweepy==4.14.0")
    print()
    sys.exit(1)

except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

