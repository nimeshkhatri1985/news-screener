# 🚀 Quick Start: Twitter Integration

## ✅ Status: Integration Complete & Tested

Your Twitter integration is **fully functional** and ready to use! Just add your credentials.

---

## 📝 3-Minute Setup

### Step 1: Get Twitter API Credentials (10 min)

1. **Go to:** https://developer.twitter.com/en/portal/dashboard
2. **Sign in** with your Twitter account
3. **Create Project** → "Haryana News Screener"
4. **Create App** → "haryana-news-bot"
5. **Set Permissions** → "Read and Write" ⚠️ Important!
6. **Copy 5 credentials:**
   - API Key
   - API Secret  
   - Access Token
   - Access Token Secret
   - Bearer Token

📚 **Need help?** See `TWITTER_API_SETUP.md` for detailed step-by-step guide

---

### Step 2: Add Credentials (2 min)

Edit your `.env` file:
```bash
cd /Users/nimeshkhatri/github/news-screener/backend
nano .env  # or open in your editor
```

Replace these lines with your actual values:
```bash
TWITTER_API_KEY=your_actual_api_key_here
TWITTER_API_SECRET=your_actual_api_secret_here
TWITTER_ACCESS_TOKEN=your_actual_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_actual_access_token_secret_here
TWITTER_BEARER_TOKEN=your_actual_bearer_token_here
```

Save and close.

---

### Step 3: Restart Backend (1 min)

```bash
# Stop current backend (Ctrl+C if running in terminal)
# Or kill the process:
pkill -f "uvicorn main:app"

# Start backend
cd /Users/nimeshkhatri/github/news-screener/backend
python -m uvicorn main:app --reload --port 8000
```

---

### Step 4: Test It! (1 min)

**Check Status:**
```bash
curl http://localhost:8000/twitter/status
```

**Expected Response:**
```json
{
  "configured": true,
  "verified": true,
  "user_info": {
    "username": "your_twitter_handle",
    "name": "Your Name"
  }
}
```

---

## ✨ Start Posting!

### Via Frontend
1. Start frontend: `cd frontend && npm start`
2. Go to **Haryana News** page
3. Click **Tweet** button on any article
4. Customize message (optional)
5. Click **Post to Twitter**
6. ✅ Done! Check your Twitter!

### Via API (for testing)
```bash
# Preview tweet first
curl -X POST http://localhost:8000/twitter/preview \
  -H "Content-Type: application/json" \
  -d '{"article_id": 1, "use_premium": false}'

# Post to Twitter
curl -X POST http://localhost:8000/twitter/post \
  -H "Content-Type: application/json" \
  -d '{"article_id": 1, "include_hashtags": true, "use_premium": false}'
```

---

## 🎯 What Works Now

✅ **Tweet Preview** - See before you post  
✅ **Free Account Mode** - Concise tweets (280 chars)  
✅ **Premium Account Mode** - Detailed tweets (4000 chars)  
✅ **Custom Messages** - Add your commentary  
✅ **Auto URL Shortening** - Via TinyURL  
✅ **Hashtag Support** - #Haryana #HaryanaNews  
✅ **Post Tracking** - Saved to database  

---

## 🐛 Troubleshooting

**Backend showing "not configured"?**
- Check you replaced ALL 5 placeholder values in .env
- Restart backend after editing .env
- Verify no extra spaces around values

**"403 Forbidden" error?**
- Make sure app permissions are "Read and Write"
- Regenerate Access Token after changing permissions

**Backend won't start?**
- Check port: `lsof -i :8000`
- Install dependencies: `pip install -r requirements.txt`

---

## 📚 Full Documentation

- **TWITTER_INTEGRATION_COMPLETE.md** - Complete summary & test results
- **TWITTER_API_SETUP.md** - Detailed setup guide with screenshots
- **TWITTER_SETUP_GUIDE.md** - Original integration guide

---

## 🎉 You're All Set!

Once you add credentials, you can immediately start posting Haryana news to Twitter!

**Next Steps:**
1. Get Twitter credentials (10 min)
2. Add to .env file (2 min)
3. Restart backend (1 min)
4. Start tweeting! 🚀

---

*Need help? Check the troubleshooting sections in the documentation files.*

