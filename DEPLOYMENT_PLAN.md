# Self-Sufficient Deployment Plan for News Screener

## Overview
Deploy the News Screener app on external hosting with fully automated daily scraping and Twitter posting, minimizing costs.

---

## Infrastructure Architecture

### **Option 1: VPS Hosting (Recommended for control + cost)**
- **Platform**: DigitalOcean, Linode, Vultr, or Hetzner
- **Specs**: 2GB RAM, 1 vCPU, 40GB SSD (~$6-12/month)
- **Why**: Full control, can run scheduled tasks, predictable pricing
- **OS**: Ubuntu 22.04 LTS

### **Option 2: Platform-as-a-Service (Easy deployment)**
- **Platform**: Railway ($5/month + usage) or Render (Free tier available)
- **Why**: Zero server management, automatic SSL, easy scaling
- **Limitation**: Scheduled jobs may need external scheduler

### **Option 3: Cloud Functions (Serverless)**
- **Platform**: Vercel (Frontend) + Railway/Render (Backend) + GitHub Actions (Scheduler)
- **Why**: Pay only for usage, free tier generous
- **Limitation**: Cold starts may affect performance

---

## Detailed Deployment Plan

### Phase 1: Database Migration (Cost: $0-7/month)

**Current**: SQLite (file-based, not production-ready)
**Target**: PostgreSQL database

**Options**:

1. **Supabase (Recommended - FREE)**
   - PostgreSQL hosted database
   - 500MB database size (enough for ~50K articles)
   - Free tier includes:
     - 2 projects
     - 500MB database
     - 2GB bandwidth/month
     - Auto backups
   - **Cost**: $0/month
   - **Setup**: Replace DATABASE_URL with Supabase connection string

2. **Neon (FREE tier available)**
   - Serverless PostgreSQL
   - Free tier: 0.5GB storage, 1 compute unit
   - **Cost**: $0/month initially, ~$5/month for production

3. **Self-hosted on VPS**
   - PostgreSQL on same VPS as backend
   - **Cost**: Included with VPS

**Implementation**:
```python
# Already supports PostgreSQL via environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./news_screener.db")
```

---

### Phase 2: Environment Variables & Secrets Management

**Required Environment Variables**:

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/news_screener

# Twitter API (you already have these)
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_TOKEN_SECRET=your_secret
TWITTER_BEARER_TOKEN=your_bearer
URL_SHORTENER_SERVICE=tinyurl
USE_URL_SHORTENING=true

# API URLs
REACT_APP_API_URL=https://your-backend-domain.com
```

**Storage**: Use platform's secrets management (Railway, Render, Heroku all have this)

---

### Phase 3: Automated Daily Scraping

**Option A: Cron Job on VPS (Simplest)**
```bash
# Create /etc/cron.daily/news-scraper
curl -X POST https://your-backend.com/scrape/trigger
```

**Option B: GitHub Actions (FREE)**
```yaml
# .github/workflows/daily-scrape.yml
name: Daily News Scraping
on:
  schedule:
    - cron: '0 2 * * *'  # Run at 2 AM UTC daily
jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Trigger Scrape
        run: |
          curl -X POST ${{ secrets.BACKEND_URL }}/scrape/trigger
```

**Option C: External Scheduler (FREE)**
- **Cron-job.org** - Free tier allows 1 job per day
- **EasyCron** - Free tier available
- **UptimeRobot** - Monitors + can trigger endpoints (free tier)

**Recommended**: GitHub Actions (FREE, reliable, version controlled)

---

### Phase 4: Twitter Posting Automation

**Current**: Manual posting through UI
**Target**: Auto-post top 3-5 articles daily

**Implementation Strategy**:

1. **Create new endpoint**: `/haryana/auto-post`
   ```python
   @app.post("/haryana/auto-post")
   async def auto_post_best_articles():
       # Get top 5 positive articles for today
       # Post to Twitter via API
       # Track posts to avoid duplicates
       pass
   ```

2. **Use same daily scheduler** to call this endpoint after scraping completes

3. **Deduplication**: Check `posts` table before posting to avoid reposting

---

### Phase 5: Frontend Deployment

**Option 1: Vercel (FREE)**
- Automatic deployments from Git
- Global CDN
- SSL included
- **Cost**: $0/month
- **Setup**: Connect GitHub repo, deploy

**Option 2: Netlify (FREE)**
- Similar to Vercel
- **Cost**: $0/month

**Option 3: Static hosting on VPS**
- Serve from Nginx
- More manual setup

---

## Recommended Complete Setup (Minimal Cost)

### **Configuration:**
1. **Frontend**: Vercel (FREE)
2. **Backend**: Railway or Render (FREE tier, ~$5-10/month for reliability)
3. **Database**: Supabase (FREE tier)
4. **Scheduler**: GitHub Actions (FREE)

### **Monthly Cost Estimate:**
- **Free Tier**: $0/month (testing phase)
- **Production**: $5-15/month
  - Backend: $5-10/month (Railway/Render paid tier)
  - Database: $0 (Supabase free tier sufficient)
  - Scheduler: $0 (GitHub Actions)
  - Frontend: $0 (Vercel)

### **Total Annual Cost**: ~$60-180/year

---

## Implementation Steps

### Step 1: Prepare for Production (Week 1)

1. **Update backend for production**
   ```bash
   # Add environment-based configuration
   # Update CORS to allow only production domain
   # Add rate limiting
   ```

2. **Database migration script**
   ```python
   # Create migration script to move from SQLite to PostgreSQL
   # Export data, import to Supabase
   ```

### Step 2: Deploy Backend (Week 1)

**Using Railway**:
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Using Render**:
```bash
# Create render.yaml
# Connect GitHub repo
# Auto-deploy on push
```

### Step 3: Deploy Frontend (Week 1)

```bash
# Vercel
npm i -g vercel
cd frontend
vercel deploy

# Or connect GitHub repo to Vercel dashboard
```

### Step 4: Setup Automated Scraping (Week 1)

1. **Create GitHub Actions workflow**
   - File: `.github/workflows/scrape-and-post.yml`
   - Trigger: Daily at 2 AM UTC
   - Action: Call backend `/scrape/trigger`

2. **Add secrets to GitHub**
   - `BACKEND_URL`: Your backend deployment URL
   - `POST_ENDPOINT`: Your auto-post endpoint

### Step 5: Test & Monitor (Week 2)

1. **Test scraping** manually triggers
2. **Verify** data appears in database
3. **Test** Twitter posting
4. **Monitor** logs for 1 week

---

## Security Considerations

1. **API Authentication**
   - Add API keys for `/scrape/trigger` endpoint
   - Use environment variables for secrets

2. **Rate Limiting**
   - Implement rate limiting (already in FastAPI with `slowapi`)
   - Prevent abuse

3. **Database Security**
   - Use SSL connections
   - Store credentials in secrets management

4. **CORS Configuration**
   - Only allow production frontend domain

---

## Monitoring & Maintenance

### **Free Monitoring Tools:**
1. **UptimeRobot** - Check if services are up (FREE tier: 50 monitors)
2. **Sentry** - Error tracking (FREE tier: 5K events/month)
3. **GitHub Actions logs** - Monitor scraping success

### **Manual Checks:**
- Weekly: Check Twitter posts are going out
- Monthly: Review database size
- Quarterly: Update dependencies

---

## Backup Strategy

1. **Database Backups**
   - Supabase: Automatic daily backups (included)
   - Or: Implement periodic exports to S3

2. **Code Backups**
   - Git repository on GitHub
   - Pull from GitHub periodically

---

## Cost Breakdown

### **Option 1: Minimum Cost (Free Tier)**
- Frontend (Vercel): $0
- Backend (Render free tier): $0 (limited)
- Database (Supabase free tier): $0
- Scheduler (GitHub Actions): $0
- **Total**: $0/month ⚠️ May hit limits

### **Option 2: Recommended (Stable)**
- Frontend (Vercel): $0
- Backend (Railway/Render): $5-10/month
- Database (Supabase): $0
- Scheduler (GitHub Actions): $0
- **Total**: $5-10/month ✅

### **Option 3: VPS (Full Control)**
- DigitalOcean droplet: $6-12/month
- Database: Included
- Frontend: Included (Nginx)
- Scheduler: Included (Cron)
- **Total**: $6-12/month ✅

---

## Timeline

**Week 1**: Setup database, deploy backend and frontend
**Week 2**: Implement automated scraping, test and debug
**Week 3**: Add auto-posting, monitor and optimize
**Week 4**: Documentation and handoff

**Total Time**: ~4 weeks for complete deployment

---

## Next Steps

1. Choose your hosting platform (recommend Railway + Vercel)
2. Set up Supabase database
3. Deploy backend
4. Deploy frontend
5. Create GitHub Actions for daily scraping
6. Test for 1 week
7. Add auto-posting feature
8. Go live!

---

## Questions to Answer Before Starting

1. **How many articles** do you expect per day? (determines database size)
2. **How many Twitter posts** per day? (Twitter API rate limits)
3. **Which news sources** to scrape? (current: 5 sources)
4. **Budget**: Free or willing to pay $10/month?
5. **Technical comfort**: VPS or Platform-as-a-Service?

Let me know your preferences and I can provide specific implementation steps!

