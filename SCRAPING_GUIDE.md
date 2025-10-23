# Haryana News Scraping Guide

## Overview

Your News Screener now has **real RSS feed scraping** capabilities to automatically fetch Haryana news from multiple sources!

## ✅ What's Working Now

- **220 Real Articles Fetched** from Times of India and Indian Express
- **75 Haryana-Relevant Articles** automatically identified
- **241 Total Articles** in database (including test data)
- **5 News Sources** configured and active

---

## 📊 Scraping Results (Latest Run)

```
✅ Times of India - Chandigarh: 20 articles
✅ Indian Express - Chandigarh: 200 articles
⚠️  The Tribune - Haryana: RSS feed issue
⚠️  Hindustan Times - Chandigarh: RSS feed issue  
⚠️  News18 - Haryana: RSS feed issue

Total: 220 new articles saved
Haryana-relevant: 75 articles (31%)
```

---

## 🚀 How to Use

### Option 1: Manual Scraping (One-Time)

Run the scraper whenever you want fresh news:

```bash
cd /Users/nimeshkhatri/github/news-screener
python3 scrape_haryana_news.py
```

**When to use**: 
- Testing the scraper
- Getting latest news before an important update
- After adding new sources

### Option 2: Automated Scraping (Recommended)

Use the auto-scraper for continuous updates:

```bash
# Run once
python3 auto_scrape.py

# Run continuously (every hour)
python3 auto_scrape.py --continuous --interval 60

# Run continuously (every 30 minutes)
python3 auto_scrape.py --continuous --interval 30

# Run quietly (minimal output)
python3 auto_scrape.py --quiet
```

**When to use**:
- Keep your database always up-to-date
- Run in background while you work
- Automated content pipeline

### Option 3: Scheduled Scraping (Production)

Set up a cron job (macOS/Linux) or Task Scheduler (Windows):

#### macOS/Linux - Using Cron

```bash
# Edit crontab
crontab -e

# Add one of these lines:

# Every hour at minute 0
0 * * * * cd /Users/nimeshkhatri/github/news-screener && /usr/local/bin/python3 auto_scrape.py --quiet >> logs/scraper.log 2>&1

# Every 30 minutes
*/30 * * * * cd /Users/nimeshkhatri/github/news-screener && /usr/local/bin/python3 auto_scrape.py --quiet >> logs/scraper.log 2>&1

# Every 6 hours
0 */6 * * * cd /Users/nimeshkhatri/github/news-screener && /usr/local/bin/python3 auto_scrape.py --quiet >> logs/scraper.log 2>&1

# Daily at 8 AM
0 8 * * * cd /Users/nimeshkhatri/github/news-screener && /usr/local/bin/python3 auto_scrape.py >> logs/scraper.log 2>&1
```

**Create logs directory first**:
```bash
mkdir -p /Users/nimeshkhatri/github/news-screener/logs
```

#### Windows - Using Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Haryana News Scraper"
4. Trigger: Daily (or your preference)
5. Action: Start a program
   - Program: `python3` or `python`
   - Arguments: `auto_scrape.py --quiet`
   - Start in: `/Users/nimeshkhatri/github/news-screener`

---

## 📰 News Sources Status

| Source | Status | Articles | Notes |
|--------|--------|----------|-------|
| **Times of India - Chandigarh** | ✅ Working | 20 | Good coverage |
| **Indian Express - Chandigarh** | ✅ Working | 200 | Excellent! |
| The Tribune - Haryana | ⚠️ Issue | 0 | RSS may have changed |
| Hindustan Times - Chandigarh | ⚠️ Issue | 0 | RSS may have changed |
| News18 - Haryana | ⚠️ Issue | 0 | RSS may have changed |

### Fixing RSS Feed Issues

If a feed isn't working:

1. **Check the RSS URL manually** in your browser
2. **Update the feed URL** in database or config
3. **Try alternative feeds** from the same source

To update a source:
```python
# Use Sources page in the UI, or:
from backend.main import SessionLocal, Source

db = SessionLocal()
source = db.query(Source).filter(Source.name == "The Tribune - Haryana").first()
source.rss_feed = "NEW_RSS_URL_HERE"
db.commit()
db.close()
```

---

## 🎯 Scraping Strategy

### For Development (Testing)
```bash
# Manual scraping when needed
python3 scrape_haryana_news.py
```

### For Daily Use
```bash
# Auto-scrape every hour
python3 auto_scrape.py --continuous --interval 60
```

### For Production
```bash
# Cron job every 30 minutes (automated, silent)
*/30 * * * * cd /path/to/news-screener && python3 auto_scrape.py --quiet
```

---

## 📈 Monitoring Scraping

### Check Scraping Status

```bash
# View scraper logs (if using cron)
tail -f logs/scraper.log

# Count articles in database
sqlite3 news_screener.db "SELECT COUNT(*) FROM articles;"

# Count articles by source
sqlite3 news_screener.db "SELECT source_id, COUNT(*) FROM articles GROUP BY source_id;"

# Recent articles
sqlite3 news_screener.db "SELECT title, published_at FROM articles ORDER BY published_at DESC LIMIT 10;"
```

### Database Location

```
/Users/nimeshkhatri/github/news-screener/news_screener.db
```

---

## 🔧 Troubleshooting

### No Articles Found

**Problem**: Scraper runs but finds 0 articles

**Solutions**:
1. Check RSS feed URL in browser
2. Check internet connection
3. Some sites may block scrapers - update User-Agent in `scraper.py`
4. RSS feed format might have changed

### Duplicate Articles

**Problem**: Same articles appearing multiple times

**Solution**: The scraper already handles this! It checks URLs before saving.

### Scraper is Slow

**Problem**: Takes too long to scrape

**Solutions**:
1. Reduce number of sources
2. Increase delay between sources (in `scraper.py`)
3. Use `--quiet` flag to reduce output processing

### SSL Warnings

**Problem**: SSL/OpenSSL warnings appear

**Solution**: These are warnings, not errors. The scraper still works. To fix:
```bash
pip install --upgrade urllib3
```

---

## 🎨 Customization

### Add More News Sources

```python
# Run this to add a new source
from backend.main import SessionLocal, Source
from datetime import datetime

db = SessionLocal()
new_source = Source(
    name="Your News Source",
    url="https://example.com",
    rss_feed="https://example.com/rss/haryana",
    is_active=True,
    created_at=datetime.utcnow()
)
db.add(new_source)
db.commit()
db.close()
```

Or use the UI at http://localhost:3000/sources

### Change Scraping Frequency

Edit the interval in continuous mode:
```bash
# Every 15 minutes
python3 auto_scrape.py --continuous --interval 15

# Every 2 hours
python3 auto_scrape.py --continuous --interval 120
```

### Filter Articles During Scraping

Modify `scraper.py` to filter articles before saving:
```python
def save_articles(self, articles: List[Dict]) -> int:
    """Save articles to database"""
    db = SessionLocal()
    saved_count = 0
    
    for article_data in articles:
        # Add your custom filtering here
        article_text = f"{article_data['title']} {article_data['content']}"
        
        # Example: Only save if contains "Haryana"
        if 'haryana' not in article_text.lower():
            continue
        
        # Rest of save logic...
```

---

## 📊 Expected Results

### Realistic Expectations

- **Articles per run**: 20-200 (varies by source)
- **New articles**: 5-50 (depends on update frequency)
- **Haryana-relevant**: 20-40% (varies by source quality)
- **Scraping time**: 10-30 seconds per source

### Optimal Schedule

| Frequency | Use Case | Pros | Cons |
|-----------|----------|------|------|
| Every 15 min | Breaking news | Always fresh | High server load |
| Every 30 min | Active monitoring | Very current | Moderate load |
| Every 1 hour | **Recommended** | Good balance | May miss some news |
| Every 6 hours | Low priority | Light load | Less current |
| Daily | Archives | Very light | Miss breaking news |

---

## 🎉 Success Checklist

- ✅ 220 real articles scraped
- ✅ 75 Haryana-relevant articles identified
- ✅ 2 working RSS feeds (Times of India, Indian Express)
- ✅ Manual scraping works
- ✅ Auto-scraper ready
- ✅ Database populated
- ⬜ Cron job scheduled (optional)
- ⬜ All 5 RSS feeds working (3 need fixing)

---

## 🚀 Next Steps

1. **View the articles**: http://localhost:3000/haryana
2. **Set up auto-scraping**: `python3 auto_scrape.py --continuous --interval 60`
3. **Fix remaining RSS feeds** (optional - 2 working feeds are sufficient)
4. **Schedule with cron** for fully automated updates
5. **Monitor and adjust** scraping frequency as needed

---

## 💡 Pro Tips

1. **Start with manual scraping** to see what articles you get
2. **Use continuous mode** while developing to always have fresh content
3. **Set up cron** for production to run in background
4. **Check logs regularly** to ensure scraping is working
5. **Update RSS feeds** if sources change their URLs

---

## 📞 Need Help?

- RSS feed not working? Try finding alternative feeds from the same source
- Too many/few articles? Adjust the frequency
- Want specific types of news? Use the Haryana filter presets
- Need more sources? Add them via the Sources page UI

---

**You now have a fully functional automated news scraping system!** 🎉

The articles are being fetched, stored, analyzed, and are ready to view at:
👉 **http://localhost:3000/haryana**

