# Quick Start: Automated Daily News Scraping

## 🚀 One-Command Setup

Run this command to set up automatic daily scraping at 7:00 AM PDT:

```bash
cd /Users/nimeshkhatri/github/news-screener
./setup_cron.sh
```

The setup script will guide you through the installation process with interactive prompts.

## ⚡ What This Does

Once configured, your news scraper will:
- ✅ Run automatically every day at 7:00 AM Pacific Time
- ✅ Scrape all active news sources
- ✅ Analyze articles for Haryana relevance
- ✅ Categorize by topics (tourism, infrastructure, economy, etc.)
- ✅ Make new articles immediately available in your web interface
- ✅ Log all activity to `logs/cron.log`

## 📋 Files Created

1. **`cron_scrape.sh`** - Main cron execution script
   - Handles environment setup
   - Runs the scraper
   - Logs results

2. **`setup_cron.sh`** - Interactive setup wizard
   - Guides you through installation
   - Offers automatic or manual setup
   - Includes testing options

3. **`CRON_SETUP_GUIDE.md`** - Comprehensive documentation
   - Detailed setup instructions
   - Timezone explanations
   - Troubleshooting guide
   - Monitoring commands

4. **`logs/`** - Log directory
   - Stores cron execution logs
   - One log file: `cron.log`

## 🎯 Quick Commands

### Install Cron Job
```bash
./setup_cron.sh
# Choose option 1 for automatic DST adjustment
```

### Test Scraper Now
```bash
# Full test with output
python3 auto_scrape.py

# Or test the cron script
bash cron_scrape.sh
```

### View Logs
```bash
# View last 50 lines
tail -50 logs/cron.log

# Follow logs in real-time
tail -f logs/cron.log
```

### Check Cron Status
```bash
# List installed cron jobs
crontab -l
```

### Remove Cron Job
```bash
# Edit and remove the line
crontab -e
```

## ⏰ Schedule Details

The cron job runs at **7:00 AM Pacific Time** daily.

**Cron Expression (recommended):**
```cron
0 7 * * * TZ='America/Los_Angeles' /Users/nimeshkhatri/github/news-screener/cron_scrape.sh >> /Users/nimeshkhatri/github/news-screener/logs/cron.log 2>&1
```

This automatically handles:
- ✅ Daylight Saving Time transitions
- ✅ PDT (UTC-7) and PST (UTC-8)
- ✅ Always runs at 7:00 AM local Pacific Time

## 📊 What Happens During a Cron Run

1. **Start** (7:00 AM PDT)
   - Logs start time and timezone
   - Activates Python environment

2. **Scraping** (7:00-7:05 AM PDT)
   - Fetches RSS feeds from all active sources
   - Extracts article content
   - Checks for duplicates

3. **Processing** (happens automatically)
   - Analyzes Haryana relevance
   - Categorizes by topic
   - Scores articles
   - Saves to database

4. **Complete** (~7:05 AM PDT)
   - Logs summary and statistics
   - New articles available in web interface

## 🔍 Monitoring Your Scraper

### View Today's Scraping Results
```bash
grep "$(date +%Y-%m-%d)" logs/cron.log
```

### Check for Errors
```bash
grep "ERROR\|Error\|❌" logs/cron.log
```

### Count Successful Runs
```bash
grep "✅ Scraping completed successfully" logs/cron.log | wc -l
```

### See Database Statistics
```bash
sqlite3 news_screener.db "SELECT COUNT(*) as total_articles FROM articles;"
```

## 🎨 Example Log Output

```
==================================================
🕐 Cron Job Started: 2025-10-27 07:00:01 PDT
==================================================
📍 Current timezone: PDT
🐍 Python version: Python 3.11.5

🤖 Starting automatic news scraping...

✅ Sources scraped: 5
✅ Articles checked: 45
✅ New articles saved: 12

✅ Scraping completed successfully

==================================================
🏁 Cron Job Finished: 2025-10-27 07:04:23 PDT
==================================================
```

## 🚨 Troubleshooting

### Cron Not Running?
1. Verify cron job is installed: `crontab -l`
2. Check script permissions: `ls -l cron_scrape.sh`
3. Test manually: `bash cron_scrape.sh`
4. Check system logs (macOS): `log show --predicate 'process == "cron"' --last 1h`

### No New Articles?
- Articles might already be in database
- RSS feeds might not have new content
- Check logs for errors: `tail -50 logs/cron.log`

### Wrong Time?
- Verify timezone: `date`
- Use `TZ='America/Los_Angeles'` in cron expression
- See CRON_SETUP_GUIDE.md for timezone details

## 📱 Viewing Scraped Articles

After scraping completes:

1. **Start the backend** (if not already running):
```bash
cd backend
python3 main.py
```

2. **Open the web interface**:
```
http://localhost:3000/haryana
```

3. **Browse by category**:
   - Tourism
   - Infrastructure
   - Economy
   - Education
   - Agriculture
   - Sports
   - Environment
   - Governance

## 🔄 Changing the Schedule

Edit your crontab to change when scraping runs:

```bash
crontab -e
```

**Examples:**

```cron
# Twice a day (7 AM and 7 PM)
0 7,19 * * * TZ='America/Los_Angeles' /path/to/cron_scrape.sh >> /path/to/logs/cron.log 2>&1

# Every 6 hours
0 */6 * * * TZ='America/Los_Angeles' /path/to/cron_scrape.sh >> /path/to/logs/cron.log 2>&1

# Every Monday at 7 AM
0 7 * * 1 TZ='America/Los_Angeles' /path/to/cron_scrape.sh >> /path/to/logs/cron.log 2>&1

# First day of month at 7 AM
0 7 1 * * TZ='America/Los_Angeles' /path/to/cron_scrape.sh >> /path/to/logs/cron.log 2>&1
```

## 📚 More Information

For detailed documentation, see:
- **CRON_SETUP_GUIDE.md** - Complete setup and troubleshooting guide
- **auto_scrape.py** - Scraper implementation
- **backend/scraper.py** - RSS feed scraping logic
- **backend/haryana_config.py** - Relevance filtering configuration

## ✨ Success!

Your automated news scraping is ready! The system will now collect fresh news every day at 7:00 AM Pacific Time without any manual intervention.

New articles will appear automatically in your web interface after each scraping run.

