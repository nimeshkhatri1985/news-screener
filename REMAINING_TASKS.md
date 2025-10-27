# 📋 Remaining Tasks & Future Roadmap

**Last Updated:** October 26, 2025  
**Project Status:** 85% Complete - MVP Functional

---

## 🔴 CRITICAL - Do First (Blockers)

### Task 1: Fix Database Schema ⚠️
**Priority:** IMMEDIATE  
**Time:** 5 minutes  
**Status:** Code ready, migration needed

**Problem:** Posts table missing 3 columns needed for Twitter integration

**Solution:**
```bash
cd /Users/nimeshkhatri/github/news-screener/backend
python3 << 'EOF'
import sqlite3
conn = sqlite3.connect('news_screener.db')
cursor = conn.cursor()
cursor.execute("ALTER TABLE posts ADD COLUMN platform VARCHAR DEFAULT 'twitter'")
cursor.execute("ALTER TABLE posts ADD COLUMN post_url VARCHAR")
cursor.execute("ALTER TABLE posts ADD COLUMN post_content TEXT")
conn.commit()
conn.close()
print("✅ Database updated!")
EOF
```

**Verification:** See DETAILED_STEPS.md Section 1

---

### Task 2: Test Twitter Posting
**Priority:** HIGH  
**Time:** 2 minutes  
**Depends On:** Task 1  
**Status:** Blocked by database schema

**Action:**
1. Fix database schema (Task 1)
2. Post first tweet via frontend or API
3. Verify on Twitter at @main_haryana
4. Check database for saved post record

**See:** DETAILED_STEPS.md Section 2 for complete instructions

---

## 🟡 HIGH PRIORITY - Core Functionality

### Task 3: Add More News Sources
**Priority:** HIGH  
**Time:** 30 minutes  
**Status:** Script ready, not executed

**Goal:** Increase from 5 to 15+ Haryana news sources

**Action:**
```bash
cd /Users/nimeshkhatri/github/news-screener
python3 add_new_haryana_sources.py
python3 scrape_haryana_news.py
```

**Sources to Add:**
- The Tribune (Chandigarh edition)
- Indian Express (Haryana)
- Hindustan Times (Haryana)
- Dainik Bhaskar (Haryana edition)
- Amar Ujala (Haryana)
- Local Haryana news portals
- Government press releases

**Expected Outcome:** 200+ new articles

---

### Task 4: Schedule Automated Scraping
**Priority:** HIGH  
**Time:** 15 minutes  
**Status:** Script ready, needs scheduling

**Options:**

**Option A: Cron Job (Linux/Mac)**
```bash
# Edit crontab
crontab -e

# Add these lines:
# Scrape every 6 hours
0 */6 * * * cd /Users/nimeshkhatri/github/news-screener && /usr/local/bin/python3 scrape_haryana_news.py >> logs/scrape.log 2>&1

# Clean up old articles (keep last 30 days)
0 2 * * * cd /Users/nimeshkhatri/github/news-screener && /usr/local/bin/python3 cleanup_old_articles.py
```

**Option B: Python Scheduler**
Create `scheduler.py`:
```python
import schedule
import time
import subprocess

def scrape_news():
    print("🔄 Starting news scrape...")
    subprocess.run(["python3", "scrape_haryana_news.py"])
    print("✅ Scrape complete!")

# Every 6 hours
schedule.every(6).hours.do(scrape_news)

print("📅 Scheduler started. Scraping every 6 hours...")
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

Run in background:
```bash
nohup python3 scheduler.py &
```

---

### Task 5: Improve Posts Management UI
**Priority:** MEDIUM  
**Time:** 2-3 hours  
**Status:** Placeholder exists

**Current:** Posts.tsx shows basic list  
**Needed:** Full-featured post management

**Features to Add:**
- [ ] View all posted tweets with previews
- [ ] Filter by date, platform, status
- [ ] Search posted content
- [ ] Analytics per post (if available from Twitter)
- [ ] Delete/edit draft posts
- [ ] Repost functionality
- [ ] Schedule future posts

**File to Edit:** `frontend/src/pages/Posts.tsx`

---

## 🟢 MEDIUM PRIORITY - Enhancements

### Task 6: Add More Filter Categories
**Priority:** MEDIUM  
**Time:** 1 hour  
**Status:** Easy to add

**New Categories to Add:**
1. **Health & Healthcare**
   - Hospitals, medical facilities
   - Health schemes, campaigns
   - Medical education

2. **Technology & Innovation**
   - Startups, tech parks
   - Digital initiatives
   - IT infrastructure

3. **Culture & Arts**
   - Festivals, traditions
   - Museums, galleries
   - Cultural events

4. **Social Development**
   - Women empowerment
   - Youth programs
   - Social welfare schemes

**Implementation:**
Edit `backend/haryana_config.py` and add new preset:
```python
"health": {
    "name": "Health & Healthcare",
    "description": "Medical facilities, health schemes, wellness",
    "keywords": ["hospital", "health", "medical", ...],
    "positive_indicators": ["new hospital", "health camp", ...],
    "negative_indicators": ["outbreak", "shortage", ...]
}
```

Then add icon in `frontend/src/pages/HaryanaNews.tsx`

---

### Task 7: Enhanced Tweet Templates
**Priority:** MEDIUM  
**Time:** 2 hours  
**Status:** Can improve current templates

**Current:** Basic templates with emojis  
**Needed:** Multiple template styles

**Templates to Add:**
- **News Style:** Formal, journalistic
- **Promotional:** Exciting, engaging
- **Question Style:** Interactive, discussion-starting
- **Quote Style:** Pull key quotes from article
- **Thread Style:** Multi-tweet threads for long content

**Implementation:**
Edit `backend/twitter_service.py` → `create_engaging_tweet()`

---

### Task 8: Database Backup System
**Priority:** MEDIUM  
**Time:** 30 minutes  
**Status:** Not implemented

**Create:** `backup_database.py`
```python
import shutil
from datetime import datetime
import os

def backup_database():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    src = "backend/news_screener.db"
    dst = f"backups/news_screener_{timestamp}.db"
    
    os.makedirs("backups", exist_ok=True)
    shutil.copy2(src, dst)
    print(f"✅ Backup created: {dst}")
    
    # Keep only last 7 backups
    cleanup_old_backups("backups", keep=7)

if __name__ == "__main__":
    backup_database()
```

**Schedule:** Daily at 2 AM via cron

---

## 🔵 LOW PRIORITY - Nice to Have

### Task 9: API Documentation with Examples
**Priority:** LOW  
**Time:** 1 hour  
**Status:** Auto-generated Swagger exists at /docs

**Enhancement:**
- Add detailed examples for each endpoint
- Create Postman collection
- Add authentication documentation (when added)
- Include rate limiting info

**Tool:** Use FastAPI's built-in schema + examples

---

### Task 10: Analytics Dashboard
**Priority:** LOW  
**Time:** 4-6 hours  
**Status:** Future feature

**Metrics to Track:**
- Articles scraped per day/week
- Most common topics
- Sentiment trends over time
- Tweet engagement (if available)
- Popular sources
- Keyword frequency analysis

**New Page:** `frontend/src/pages/Analytics.tsx`

---

### Task 11: Advanced Search Features
**Priority:** LOW  
**Time:** 2-3 hours  
**Status:** Basic search exists

**Enhancements:**
- [ ] Advanced filters (date range picker)
- [ ] Save search queries
- [ ] Search history
- [ ] Boolean operators (AND, OR, NOT)
- [ ] Fuzzy matching
- [ ] Search within results

---

## 🚀 PRODUCTION DEPLOYMENT

### Task 12: Choose Hosting Platform
**Priority:** When ready for production  
**Time:** Research 2 hours, setup 3-4 hours  
**Status:** Not started

**Options Comparison:**

| Platform | Backend | Frontend | Database | Cost/month | Pros |
|----------|---------|----------|----------|------------|------|
| **Railway** | ✅ | ✅ | ✅ | $5-10 | Easy, auto-deploy |
| **Render** | ✅ | ✅ | ✅ | $7-15 | Free tier, reliable |
| **Vercel + Railway** | ❌ | ✅ | ⚠️ | $0-10 | Great for frontend |
| **Heroku** | ✅ | ✅ | ✅ | $7-15 | Classic choice |
| **DigitalOcean** | ✅ | ✅ | ✅ | $12-20 | Full control |

**Recommended:** Railway (easiest for full-stack)

---

### Task 13: Production Database Setup
**Priority:** With deployment  
**Time:** 2 hours  
**Status:** Using SQLite locally

**Migration:** SQLite → PostgreSQL

**Why PostgreSQL:**
- Better for production
- More concurrent connections
- Better performance at scale
- Standard for hosted platforms

**Migration Script Needed:**
```bash
# Export SQLite data
sqlite3 news_screener.db .dump > backup.sql

# Import to PostgreSQL (after setup)
psql -U username -d news_screener -f backup.sql
```

---

### Task 14: Environment Configuration
**Priority:** Before deployment  
**Time:** 1 hour  
**Status:** Using .env locally

**Needed:**
- [ ] Production .env file
- [ ] Separate dev/staging/prod configs
- [ ] Secret management (not in git)
- [ ] Environment-specific URLs

**Files to Create:**
- `.env.production`
- `.env.staging`
- `config.py` (centralized config management)

---

### Task 15: CI/CD Pipeline
**Priority:** LOW (manual deploy OK for now)  
**Time:** 3-4 hours  
**Status:** Not implemented

**Setup GitHub Actions:**
- Automated testing on push
- Automated deployment on merge to main
- Database migrations
- Rollback capability

**File:** `.github/workflows/deploy.yml`

---

### Task 16: Domain & SSL Setup
**Priority:** With deployment  
**Time:** 1 hour  
**Status:** Not started

**Steps:**
1. Buy domain (e.g., haryana-news.com) - ~$12/year
2. Point DNS to hosting platform
3. Enable SSL (free with most hosts)
4. Configure CORS for production domain

---

### Task 17: Monitoring & Error Tracking
**Priority:** After deployment  
**Time:** 2 hours  
**Status:** Basic logging exists

**Tools to Add:**
- **Sentry:** Error tracking and monitoring (free tier available)
- **LogRocket:** Session replay for debugging
- **UptimeRobot:** Uptime monitoring (free)
- **Google Analytics:** Usage tracking

---

## 🔮 FUTURE FEATURES (Phase 2)

### Task 18: User Authentication
**Priority:** FUTURE  
**Time:** 6-8 hours  
**Status:** Not planned for MVP

**Why:** Allow multiple users, team collaboration

**Features:**
- User registration/login
- Role-based access (admin, editor, viewer)
- Personal dashboards
- Activity logging

**Stack:** JWT tokens + FastAPI security utils

---

### Task 19: Multi-Platform Support
**Priority:** FUTURE  
**Time:** 10+ hours per platform  
**Status:** Twitter only currently

**Platforms to Add:**
- Facebook
- Instagram
- LinkedIn
- Telegram channel

**Challenge:** Each platform has different APIs, limits, formats

---

### Task 20: ML-Based Content Classification
**Priority:** FUTURE  
**Time:** 20+ hours  
**Status:** Using keyword matching now

**Enhancement:** Replace keyword matching with ML model

**Approach:**
- Train on labeled Haryana news articles
- Use BERT or similar transformer model
- Better sentiment analysis
- Auto-categorization
- Relevance prediction

**Benefits:** More accurate, learns from data

---

### Task 21: Auto-Posting with Approval
**Priority:** FUTURE  
**Time:** 6-8 hours  
**Status:** Manual posting only

**Workflow:**
1. System identifies high-quality articles
2. Generates draft tweet
3. Sends for approval (email/dashboard)
4. Admin approves/edits/rejects
5. Auto-posts at scheduled time

**Features:**
- Approval queue UI
- Email notifications
- Scheduled posting
- Bulk approval

---

### Task 22: Image Generation for Posts
**Priority:** FUTURE  
**Time:** 8-10 hours  
**Status:** Text-only tweets currently

**Goal:** Generate eye-catching images for tweets

**Options:**
- **Template-based:** Use Pillow to generate from templates
- **AI-based:** Use DALL-E or Stable Diffusion
- **Screenshot:** Auto-capture article screenshots

**Benefits:** Better engagement, more professional look

---

### Task 23: API Rate Limiting
**Priority:** FUTURE  
**Time:** 2-3 hours  
**Status:** No limits currently

**Why:** Prevent abuse, control costs

**Implementation:**
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.get("/api/articles")
@limiter.limit("100/hour")
async def get_articles():
    ...
```

---

### Task 24: Mobile App
**Priority:** FUTURE  
**Time:** 40+ hours  
**Status:** Web only

**Options:**
- React Native (reuse React knowledge)
- Flutter (better performance)
- PWA (convert existing web app)

**Features:**
- Push notifications for new articles
- Offline reading
- Quick posting
- Mobile-optimized UI

---

## 📊 QUICK PRIORITY SUMMARY

### Do First (Next Session):
1. 🔴 Fix database schema (5 min)
2. 🔴 Test Twitter posting (2 min)
3. 🟡 Add more news sources (30 min)

### Do Soon (This Week):
4. 🟡 Schedule automated scraping
5. 🟡 Improve Posts UI
6. 🟢 Add filter categories

### Do Later (This Month):
7. Enhanced features
8. Better analytics
9. Production deployment prep

### Do Eventually (Future):
10. Advanced ML features
11. Multi-platform support
12. Mobile app

---

## 💡 MAINTENANCE TASKS

### Daily:
- Monitor scraping logs
- Check for errors
- Review new articles

### Weekly:
- Database backup
- Clean old articles (>90 days)
- Review Twitter analytics
- Add new sources if needed

### Monthly:
- Update dependencies
- Security audit
- Performance review
- User feedback review

---

## 📞 GETTING HELP

**If you get stuck:**
1. Check the relevant documentation file
2. Review error logs: `backend/backend.log`
3. Test endpoints at: `http://localhost:8000/docs`
4. Check Twitter developer console for API issues

**Documentation References:**
- Setup: `QUICK_START_TWITTER.md`
- Technical: `TECHNICAL_DOCUMENTATION.md`
- Learning: `LEARNING_GUIDE.md`
- Context: `PROJECT_CONTEXT.md`

---

**Last Updated:** October 26, 2025  
**Next Review:** After completing Tasks 1-3  
**Version:** 1.0

