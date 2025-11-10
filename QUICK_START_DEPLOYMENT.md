# Quick Start: Deploy News Screener in 1 Hour

This guide will get your News Screener app running autonomously in about 1 hour.

---

## Prerequisites

- [x] GitHub repository with your code
- [x] Twitter API credentials (already have these)
- [ ] Email for signing up to hosting platforms

---

## Step-by-Step Deployment

### Step 1: Set Up Database (15 minutes)

1. Go to https://supabase.com
2. Sign up with GitHub
3. Create new project
4. Wait for database to provision (2-3 minutes)
5. Go to Project Settings → Database
6. Copy the "Connection string" (looks like `postgresql://...`)
7. Save this as `SUPABASE_DB_URL`

---

### Step 2: Deploy Backend (20 minutes)

**Using Railway (Recommended)**

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `news-screener` repository
5. Select the root directory (not `backend` folder)
6. Railway will detect it's a Python app

**Configure Environment Variables:**
1. Click on your deployed service
2. Go to "Variables" tab
3. Add these variables:
   ```
   DATABASE_URL=<paste your SUPABASE_DB_URL>
   TWITTER_API_KEY=<your existing key>
   TWITTER_API_SECRET=<your existing secret>
   TWITTER_ACCESS_TOKEN=<your existing token>
   TWITTER_ACCESS_TOKEN_SECRET=<your existing secret>
   TWITTER_BEARER_TOKEN=<your existing bearer>
   URL_SHORTENER_SERVICE=tinyurl
   USE_URL_SHORTENING=true
   ```
4. Click "Deploy" or Railway will auto-deploy

**Get Backend URL:**
1. Click on your service
2. Find "DOMAIN" section
3. Copy the URL (e.g., `news-screener-production.up.railway.app`)
4. Add `/docs` to verify it works (e.g., `https://news-screener-production.up.railway.app/docs`)

---

### Step 3: Deploy Frontend (15 minutes)

**Using Vercel**

1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "Add New Project"
4. Import your GitHub repository
5. Configure build settings:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
6. Add Environment Variable:
   - Key: `REACT_APP_API_URL`
   - Value: Your Railway backend URL (from Step 2)
7. Click "Deploy"

Your frontend will be live at something like: `https://news-screener.vercel.app`

---

### Step 4: Set Up Automated Scraping (10 minutes)

1. Go to your GitHub repository
2. Create `.github/workflows/` directory if it doesn't exist
3. Add the file `daily-scrape-and-post.yml` (already created in this repo)
4. Go to GitHub repository settings → Secrets and variables → Actions
5. Click "New repository secret"
6. Add these secrets:
   - **Name**: `BACKEND_URL`
     **Value**: Your Railway backend URL (e.g., `https://news-screener-production.up.railway.app`)
   - **Name**: `API_KEY`
     **Value**: Create a random secure string (for API authentication)
7. Commit and push the workflow file

**Add Authentication to Backend:**

Modify `main.py` to add basic auth to the scrape endpoint:

```python
from fastapi import Depends, Header, HTTPException
import os

API_KEY = os.getenv("API_KEY", "your-secret-key")

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@app.post("/scrape/trigger")
async def trigger_scrape(db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    # ... existing code ...
```

---

### Step 5: Test Everything (5 minutes)

1. **Test Backend**: Visit your Railway URL + `/docs`
2. **Test Frontend**: Visit your Vercel URL
3. **Test Manual Scrape**: Call `POST /scrape/trigger` from the API docs
4. **Check Database**: Go to Supabase dashboard → Table Editor → Verify articles are being added

---

### Step 6: Enable Auto-Posting (Optional - 10 minutes)

1. Integrate the `auto_post_endpoint.py` into your `main.py`
2. Add the route to your FastAPI app
3. Update GitHub Actions to call `/haryana/auto-post`
4. Set your preferred parameters

---

## Final Setup

### Update CORS in Backend

In `main.py`, update CORS settings:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "https://your-frontend.vercel.app"  # Add your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Cost Summary

- Supabase: **FREE** (enough for this project)
- Railway: **FREE** tier → $5/month if you upgrade
- Vercel: **FREE** (generous free tier)
- GitHub Actions: **FREE** (2000 minutes/month)
- **Total Monthly Cost**: $0-$5

---

## What Happens Next?

1. **Every day at 2 AM UTC**: GitHub Actions triggers
2. **Scrapes news**: From configured sources
3. **Scores articles**: Using Haryana filter presets
4. **Posts to Twitter**: Top 3 positive articles
5. **You receive**: Tweets with news links

---

## Troubleshooting

### Backend won't deploy
- Check environment variables are set
- Look at Railway logs
- Verify Python version (should be 3.9+)

### Frontend shows errors
- Check REACT_APP_API_URL is set correctly
- Open browser console for errors
- Verify CORS is configured

### No articles appearing
- Check Supabase database
- Verify sources are active
- Check backend logs in Railway

### Twitter posting fails
- Verify Twitter credentials
- Check rate limits
- Review Twitter API v2 requirements

---

## Next Steps

1. **Monitor for 1 week**: Check logs daily
2. **Tune filters**: Adjust relevance scores
3. **Add more sources**: Expand news coverage
4. **Customize tweets**: Modify tweet generation
5. **Scale up**: If you need more capacity

---

## Support

- Check GitHub Issues for common problems
- Review deployment platform docs (Railway, Vercel)
- Check application logs in respective dashboards

**You now have a fully autonomous News Screener! 🎉**

