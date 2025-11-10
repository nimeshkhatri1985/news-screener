# Implementation Checklist

## Quick Decision Tree

### Budget: FREE (Testing Phase)
- [ ] Backend: Render free tier
- [ ] Database: Supabase free tier  
- [ ] Frontend: Vercel free tier
- [ ] Scheduler: GitHub Actions (free)
- **Total**: $0/month

### Budget: $10/month (Production)
- [ ] Backend: Railway starter plan ($5/month)
- [ ] Database: Supabase free tier (upgrade later if needed)
- [ ] Frontend: Vercel free tier
- [ ] Scheduler: GitHub Actions (free)
- **Total**: ~$5-10/month

### Budget: Full Control ($12/month)
- [ ] VPS: DigitalOcean $12/month
- [ ] Database: PostgreSQL on VPS (included)
- [ ] Frontend: Served from VPS
- [ ] Scheduler: Cron job on VPS
- **Total**: $12/month

---

## Implementation Tasks

### Phase 1: Database Migration

- [ ] Sign up for Supabase (https://supabase.com)
- [ ] Create new project
- [ ] Get connection string
- [ ] Create migration script (SQLite → PostgreSQL)
- [ ] Test migration locally
- [ ] Update DATABASE_URL in environment variables

**Estimated Time**: 2-3 hours

---

### Phase 2: Backend Deployment

**Using Railway (Recommended)**:
- [ ] Sign up for Railway (https://railway.app)
- [ ] Install Railway CLI
- [ ] Run `railway init`
- [ ] Add environment variables in Railway dashboard
- [ ] Deploy with `railway up`
- [ ] Test API endpoints
- [ ] Set up custom domain (optional)

**Estimated Time**: 1-2 hours

---

### Phase 3: Frontend Deployment

**Using Vercel**:
- [ ] Sign up for Vercel (https://vercel.com)
- [ ] Import GitHub repository
- [ ] Configure build settings:
  - Build command: `npm run build`
  - Output directory: `build`
- [ ] Add environment variable: `REACT_APP_API_URL`
- [ ] Deploy and test
- [ ] Verify CORS settings

**Estimated Time**: 30 minutes

---

### Phase 4: Automated Scraping

**Using GitHub Actions**:
- [ ] Create `.github/workflows/daily-scrape.yml`
- [ ] Add workflow file (see example below)
- [ ] Add BACKEND_URL secret to GitHub
- [ ] Test workflow manually
- [ ] Schedule daily run (2 AM UTC)
- [ ] Monitor first few runs

**Workflow Template**:
```yaml
name: Daily News Scraping
on:
  schedule:
    - cron: '0 2 * * *'
  workflow_dispatch: # Allow manual trigger

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Scraping
        run: |
          curl -X POST ${{ secrets.BACKEND_URL }}/scrape/trigger \
            -H "Authorization: Bearer ${{ secrets.API_KEY }}"
      
      - name: Auto-Post to Twitter
        run: |
          curl -X POST ${{ secrets.BACKEND_URL }}/haryana/auto-post
```

**Estimated Time**: 1-2 hours

---

### Phase 5: Twitter Auto-Posting

- [ ] Create new endpoint `/haryana/auto-post`
- [ ] Implement logic:
  - Query top 3-5 positive articles
  - Check if already posted
  - Post to Twitter
  - Store in database
- [ ] Add to GitHub Actions workflow
- [ ] Test manually
- [ ] Monitor for 1 week

**Estimated Time**: 3-4 hours

---

### Phase 6: Monitoring & Maintenance

- [ ] Set up UptimeRobot for backend health
- [ ] Add Sentry for error tracking
- [ ] Create monitoring dashboard (optional)
- [ ] Document maintenance procedures
- [ ] Set up alerts for failures

**Estimated Time**: 2-3 hours

---

## Priority Actions (Start Here)

1. **Today**: Sign up for Supabase and Railway
2. **This Week**: Deploy backend to Railway
3. **This Week**: Deploy frontend to Vercel
4. **Next Week**: Set up GitHub Actions for scraping
5. **Next Week**: Implement auto-posting

---

## Quick Start Commands

### Local Testing
```bash
# Start backend with production config
cd backend
export DATABASE_URL="your_supabase_url"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000

# Start frontend
cd frontend
export REACT_APP_API_URL="http://localhost:8000"
npm start
```

### Deploy to Railway
```bash
railway login
railway init
railway link
railway up
```

### Deploy to Vercel
```bash
cd frontend
vercel --prod
```

---

## Environment Variables Checklist

### Backend (.env)
- [ ] DATABASE_URL
- [ ] TWITTER_API_KEY
- [ ] TWITTER_API_SECRET
- [ ] TWITTER_ACCESS_TOKEN
- [ ] TWITTER_ACCESS_TOKEN_SECRET
- [ ] TWITTER_BEARER_TOKEN
- [ ] URL_SHORTENER_SERVICE
- [ ] USE_URL_SHORTENING

### Frontend (Vercel Dashboard)
- [ ] REACT_APP_API_URL

### GitHub Actions (Secrets)
- [ ] BACKEND_URL
- [ ] API_KEY (for authentication)

---

## Testing Checklist

### Pre-Deployment
- [ ] All tests pass locally
- [ ] Environment variables set correctly
- [ ] Database connection works
- [ ] Twitter API credentials valid

### Post-Deployment
- [ ] API returns expected responses
- [ ] Frontend loads correctly
- [ ] Articles display properly
- [ ] Scraping triggers successfully
- [ ] Twitter posting works
- [ ] No errors in logs

### Ongoing
- [ ] Check logs daily (first week)
- [ ] Verify scraping works daily
- [ ] Confirm Twitter posts are being sent
- [ ] Monitor database size

---

## Estimated Timeline

- **Week 1**: Database migration, backend deployment
- **Week 2**: Frontend deployment, automated scraping
- **Week 3**: Twitter auto-posting, testing
- **Week 4**: Monitoring, optimization, documentation

**Total**: 4 weeks to fully autonomous deployment

---

## Support & Troubleshooting

### Common Issues

1. **Database connection fails**
   - Check DATABASE_URL format
   - Verify SSL settings
   - Test connection string locally

2. **Twitter API errors**
   - Verify credentials
   - Check rate limits
   - Review API version compatibility

3. **Scraping fails**
   - Check source URLs
   - Verify network connectivity
   - Review error logs

4. **Frontend won't load**
   - Check REACT_APP_API_URL
   - Verify CORS settings
   - Clear browser cache

### Getting Help

- Check deployment platform docs
- Review GitHub Actions logs
- Check backend logs in Railway/Render dashboard
- Monitor Twitter API status

