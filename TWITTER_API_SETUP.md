# 🐦 Twitter API Setup - Step-by-Step Guide

## Overview
This guide will walk you through setting up Twitter API access for your News Screener application.

## ⏱️ Estimated Time: 15-20 minutes

---

## 📋 Prerequisites
- A Twitter/X account (free account is sufficient)
- Email address for verification
- Your project description ready

---

## 🔑 Step 1: Create a Twitter Developer Account

### 1.1 Go to Twitter Developer Portal
1. Visit: **https://developer.twitter.com/en/portal/dashboard**
2. Click **"Sign in"** and log in with your Twitter account

### 1.2 Apply for Developer Access
If this is your first time:

1. Click **"Sign up for Free Account"** or **"Apply for Developer Account"**
2. Choose account type: **"Hobbyist"** → **"Making a bot"**
3. Fill out the application form:
   
   **Basic Info:**
   - Country: `Your country`
   - Use case: Select "Making a bot"
   
   **About You:**
   - App name: `Haryana News Screener` (or your choice)
   - Description: 
     ```
     I'm building an automated news curation tool that filters and posts 
     curated Haryana-related news articles to Twitter. The bot will help 
     share important news about infrastructure, tourism, education, and 
     other topics relevant to Haryana state.
     ```
   
   **Intended Use:**
   - Will your app use Tweet, Retweet, Like, Follow, or Direct Message functionality? `Yes`
   - Are you planning to analyze Twitter data? `No`
   - Will your product, service, or analysis make Twitter content or derived information available to a government entity? `No`
   
4. **Review and Accept** the Developer Agreement and Policy
5. **Verify your email address** (check your inbox)

---

## 🚀 Step 2: Create a Twitter App

### 2.1 Create a New Project
1. In the Developer Portal, click **"+ Create Project"**
2. Fill in the project details:
   - **Project name**: `haryana-news-screener` (or your choice)
   - **Use case**: Select "Making a bot"
   - **Project description**: 
     ```
     Automated news curation and posting system for Haryana state news
     ```

### 2.2 Create an App
1. After creating the project, click **"+ Add App"**
2. Choose: **"Create new App"**
3. **App name**: `haryana-news-bot` (must be unique - add numbers if taken)
4. Click **"Complete"**

---

## 🔐 Step 3: Get Your API Keys

### 3.1 Save Your API Keys
After creating the app, you'll immediately see:

```
✅ API Key (Consumer Key)
✅ API Key Secret (Consumer Secret)  
✅ Bearer Token
```

**⚠️ CRITICAL: Copy these NOW!** You won't be able to see the secrets again.

**Save them temporarily** in a text file (you'll add them to `.env` later):
```
API Key: [your key here]
API Secret: [your secret here]
Bearer Token: [your token here]
```

### 3.2 Generate Access Tokens
1. After saving the above, click **"App Settings"** (or go to your app in the dashboard)
2. Navigate to the **"Keys and tokens"** tab
3. Under **"Access Token and Secret"**, click **"Generate"**
4. Copy and save:
   ```
   Access Token: [your token here]
   Access Token Secret: [your secret here]
   ```

---

## ⚙️ Step 4: Configure App Permissions

### 4.1 Set Read and Write Permissions
1. In your app settings, go to **"Settings"** tab
2. Scroll down to **"App permissions"**
3. Click **"Edit"**
4. Select: **"Read and Write"** (required for posting tweets)
5. Click **"Save"**

### 4.2 Setup User Authentication (Optional but Recommended)
1. Still in **"Settings"** tab, scroll to **"User authentication settings"**
2. Click **"Set up"**
3. Configure:
   - **App permissions**: ✅ Read and Write
   - **Type of App**: Select "Web App, Automated App or Bot"
   - **App info**:
     - Callback URI: `http://localhost:3000/callback`
     - Website URL: `http://localhost:3000` (or your domain)
4. Click **"Save"**

**⚠️ Important:** After changing permissions, you must **regenerate your Access Tokens**:
1. Go back to **"Keys and tokens"** tab
2. Click **"Regenerate"** for Access Token and Secret
3. Save the new tokens (the old ones won't work anymore)

---

## 📝 Step 5: Add Credentials to Your App

### 5.1 Open the .env File
Navigate to your backend directory:
```bash
cd /Users/nimeshkhatri/github/news-screener/backend
```

### 5.2 Edit .env File
Open the `.env` file in your editor and replace the placeholder values:

```bash
# Replace these with your actual values from Step 3:

TWITTER_API_KEY=your_actual_api_key_here
TWITTER_API_SECRET=your_actual_api_secret_here
TWITTER_ACCESS_TOKEN=your_actual_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_actual_access_token_secret_here
TWITTER_BEARER_TOKEN=your_actual_bearer_token_here
```

**Example (with fake values):**
```bash
TWITTER_API_KEY=AbCdEfGhIjKlMnOpQrStUvWxYz
TWITTER_API_SECRET=1234567890AbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMn
TWITTER_ACCESS_TOKEN=1234567890-AbCdEfGhIjKlMnOpQrStUvWx
TWITTER_ACCESS_TOKEN_SECRET=AbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKl
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGh...
```

### 5.3 Save the File
Save and close the `.env` file.

**🔒 Security Note:** 
- Never commit this file to git (it's already in `.gitignore`)
- Never share these credentials publicly
- Keep a backup copy in a secure location

---

## ✅ Step 6: Test Your Configuration

### 6.1 Start the Backend Server
```bash
cd /Users/nimeshkhatri/github/news-screener/backend
python -m uvicorn main:app --reload --port 8000
```

### 6.2 Test Twitter Connection
Open a new terminal and run:
```bash
curl http://localhost:8000/twitter/status
```

**Expected Response (Success):**
```json
{
  "configured": true,
  "verified": true,
  "user_info": {
    "username": "your_twitter_handle",
    "name": "Your Display Name"
  },
  "message": "Twitter API credentials verified successfully"
}
```

**If you see `"configured": false`:**
- Check that your `.env` file has the correct values
- Make sure you replaced ALL placeholder values
- Verify there are no extra spaces or quotes around the values
- Restart the backend server

---

## 🎉 Step 7: Test Posting a Tweet

### 7.1 Start the Frontend
```bash
cd /Users/nimeshkhatri/github/news-screener/frontend
npm start
```

### 7.2 Test the Integration
1. Navigate to **Haryana News** page
2. Find any article
3. Click the **"Tweet"** button
4. Customize your message (optional)
5. Click **"Post to Twitter"**
6. ✅ Your tweet should be posted!

---

## 🐛 Troubleshooting

### Issue: "Twitter API not configured"
**Solution:**
- Verify all 5 credentials are in `.env` file
- Check for typos or extra spaces
- Restart the backend server after editing `.env`

### Issue: "403 Forbidden" or "401 Unauthorized"
**Solution:**
- Verify your app has "Read and Write" permissions
- Regenerate Access Token and Secret after permission change
- Make sure Access Token matches your current app

### Issue: "429 Too Many Requests"
**Solution:**
- You've hit the Twitter API rate limit
- Wait 15 minutes and try again
- Free tier limits: 50 tweets per 24 hours

### Issue: "Tweet appears truncated"
**Solution:**
- This is normal for long articles
- The system automatically shortens URLs
- Premium accounts can post longer tweets (up to 4000 chars)

---

## 📊 API Rate Limits (Free Tier)

| Action | Limit |
|--------|-------|
| Post tweets | 50 per 24 hours |
| Read tweets | 500 per 15 min |
| Search tweets | 450 per 15 min |

**Tip:** If you need higher limits, consider upgrading to Twitter API Pro ($100/month)

---

## 🔗 Useful Links

- **Twitter Developer Portal**: https://developer.twitter.com/en/portal/dashboard
- **API Documentation**: https://developer.twitter.com/en/docs/twitter-api
- **API Status**: https://api.twitterstat.us/
- **Support**: https://twittercommunity.com/

---

## 📞 Need Help?

If you encounter issues:
1. Check the backend logs: `backend/backend.log`
2. Review the Twitter Developer Console for errors
3. Verify your credentials are correct
4. Make sure your app permissions are "Read and Write"

---

## 🎓 Next Steps

Once your Twitter API is working:
- ✅ Post your first article to Twitter
- 📊 Monitor posted tweets in the Posts page
- 🎨 Customize tweet templates
- 📈 Analyze engagement metrics

**Happy tweeting! 🚀**

