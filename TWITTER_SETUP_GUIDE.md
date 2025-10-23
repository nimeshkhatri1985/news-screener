# 🐦 Twitter Integration Setup Guide

## Overview

The News Screener now includes Twitter integration, allowing you to post Haryana news articles directly to Twitter with one click!

## Features

✅ **Post Articles to Twitter** - Share news articles with customizable messages  
✅ **Tweet Preview** - See how your tweet will look before posting  
✅ **Custom Messages** - Add your own commentary to articles  
✅ **Hashtag Support** - Automatically adds #Haryana #HaryanaNews  
✅ **Character Limit Handling** - Automatically truncates long titles  
✅ **Post Tracking** - Keeps record of all posted tweets  

## 🔑 Step 1: Get Twitter API Credentials

### 1.1 Create a Twitter Developer Account

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Sign in with your Twitter account
3. Click "Sign up for Free Account" if you don't have developer access
4. Fill out the application form:
   - **Use case**: Content Publisher / News Bot
   - **Description**: "Automated posting of curated Haryana news articles"
5. Accept the Terms and Conditions
6. Verify your email address

### 1.2 Create a Twitter App

1. In the Developer Portal, click **"+ Create Project"**
2. **Project Name**: "Haryana News Screener" (or your choice)
3. **Use Case**: Select "Making a bot"
4. **Project Description**: "Automated news curation and posting for Haryana"
5. Click **"Create App"** within the project
6. **App Name**: "haryana-news-bot" (must be unique)

### 1.3 Get Your API Keys

After creating the app, you'll see your keys:

1. **API Key** (Consumer Key)
2. **API Key Secret** (Consumer Secret)
3. **Bearer Token**

⚠️ **IMPORTANT**: Save these immediately! You won't be able to see the secrets again.

### 1.4 Generate Access Tokens

1. Go to your app's **"Keys and tokens"** tab
2. Under **"Authentication Tokens"**, click **"Generate"** for Access Token and Secret
3. Save:
   - **Access Token**
   - **Access Token Secret**

### 1.5 Set App Permissions

1. Go to **"User authentication settings"**
2. Click **"Set up"**
3. **App permissions**: Select **"Read and write"** (required for posting)
4. **Type of App**: "Web App, Automated App or Bot"
5. **Callback URI**: `http://localhost:3000/callback` (for local development)
6. **Website URL**: Your website or `http://localhost:3000`
7. Save changes

## 🔧 Step 2: Configure Environment Variables

### 2.1 Create .env File

Create a `.env` file in the `/backend` directory:

```bash
cd /Users/nimeshkhatri/github/news-screener/backend
touch .env
```

### 2.2 Add Twitter Credentials

Add the following to your `.env` file:

```bash
# Twitter API Credentials
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

Replace the placeholder values with your actual credentials from Step 1.

### 2.3 Secure Your .env File

Make sure `.env` is in your `.gitignore`:

```bash
# Check if .env is ignored
grep "\.env" /Users/nimeshkhatri/github/news-screener/.gitignore
```

If not, add it:

```bash
echo ".env" >> /Users/nimeshkhatri/github/news-screener/.gitignore
```

## 🚀 Step 3: Test Twitter Integration

### 3.1 Restart Backend

```bash
# Kill existing backend
lsof -ti:8000 | xargs kill -9

# Start backend with new environment variables
cd /Users/nimeshkhatri/github/news-screener/backend
python3 main.py
```

### 3.2 Check Twitter Status

Test if credentials are working:

```bash
curl http://localhost:8000/twitter/status | python3 -m json.tool
```

Expected response:
```json
{
  "configured": true,
  "verified": true,
  "user_info": {
    "username": "your_twitter_handle",
    "name": "Your Display Name"
  },
  "message": "Twitter credentials verified successfully"
}
```

### 3.3 Preview a Tweet

```bash
curl -X POST http://localhost:8000/twitter/preview \
  -H "Content-Type: application/json" \
  -d '{"article_id": 1, "include_hashtags": true}' \
  | python3 -m json.tool
```

### 3.4 Post Your First Tweet (Optional)

⚠️ **This will actually post to Twitter!**

```bash
curl -X POST http://localhost:8000/twitter/post \
  -H "Content-Type: application/json" \
  -d '{"article_id": 1, "custom_message": "Check out this news from Haryana!", "include_hashtags": true}' \
  | python3 -m json.tool
```

## 📱 Step 4: Use the Frontend Interface

### 4.1 Access the Haryana News Page

1. Open http://localhost:3000/haryana
2. Browse articles with your preferred filters
3. Click the **"Post to Twitter"** button on any article
4. Preview your tweet
5. Customize the message if needed
6. Click **"Post"** to publish!

### 4.2 View Posted Tweets

- All posted tweets are tracked in the database
- View them in the **"Posts"** section
- Each post includes the tweet URL for easy access

## 🔒 Security Best Practices

1. **Never commit `.env` file** to Git
2. **Use environment variables** for production deployment
3. **Rotate keys regularly** (every 90 days recommended)
4. **Monitor API usage** in Twitter Developer Portal
5. **Set up rate limiting** to avoid hitting Twitter API limits
6. **Use separate accounts** for testing and production

## 📊 API Endpoints

### GET /twitter/status
Check Twitter API configuration and verify credentials

### POST /twitter/preview
Preview how a tweet will look without posting
```json
{
  "article_id": 1,
  "custom_message": "Optional message",
  "include_hashtags": true
}
```

### POST /twitter/post
Post an article to Twitter
```json
{
  "article_id": 1,
  "custom_message": "Optional message",
  "include_hashtags": true
}
```

### POST /twitter/post-custom
Post custom text to Twitter
```json
{
  "text": "Your custom tweet text here"
}
```

## 🐛 Troubleshooting

### Error: "Twitter API not configured"
- Check that all environment variables are set in `.env`
- Restart the backend after adding credentials
- Verify the `.env` file is in the `/backend` directory

### Error: "401 Unauthorized"
- Regenerate your Access Token and Secret
- Make sure app permissions are set to "Read and write"
- Check that credentials are copied correctly (no extra spaces)

### Error: "403 Forbidden"
- Your app may not have "Read and write" permissions
- Go to app settings → User authentication settings → Edit
- Change permissions to "Read and write" and regenerate tokens

### Error: "Rate limit exceeded"
- Twitter has rate limits (300 tweets per 3 hours for standard access)
- Wait for the rate limit window to reset
- Consider upgrading to Twitter API Pro for higher limits

## 💡 Tips for Better Tweets

1. **Keep titles concise** - Shorter titles work better on Twitter
2. **Use custom messages** - Add context or commentary
3. **Include hashtags** - Increases discoverability
4. **Post at optimal times** - Early morning and evening get more engagement
5. **Mix content types** - Don't just post links, add value
6. **Engage with responses** - Reply to comments on your tweets

## 📈 Twitter API Limits

### Free Tier (Essential Access)
- 500,000 tweets read per month
- 1,500 tweets write per month
- 300 tweets per 3-hour window

### Paid Tiers
- **Basic** ($100/month): 10,000 tweets/month
- **Pro** ($5,000/month): 1,000,000 tweets/month

## 🎯 Next Steps

1. ✅ Set up Twitter Developer Account
2. ✅ Get API credentials
3. ✅ Configure environment variables
4. ✅ Test the integration
5. 🔄 Start posting Haryana news!
6. 📊 Monitor engagement and adjust strategy

---

**Need Help?** Check the [Twitter API Documentation](https://developer.twitter.com/en/docs/twitter-api) or open an issue in the repository.

