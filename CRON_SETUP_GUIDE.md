# Cron-Based Automatic News Scraping

This guide explains how to set up automatic daily news scraping at 7:00 AM Pacific Time using cron.

## 📋 Overview

The cron setup will automatically scrape news from all configured sources once per day at 7:00 AM PDT/PST. The scraped articles will be:
- Analyzed for Haryana relevance
- Categorized by topic (tourism, infrastructure, economy, etc.)
- Scored for relevance
- Made available immediately in the web interface

## 🚀 Quick Setup

### Option 1: Automatic Setup (Recommended)

Run the setup script which will guide you through the installation:

```bash
cd /Users/nimeshkhatri/github/news-screener
chmod +x setup_cron.sh
./setup_cron.sh
```

The script will:
1. Create necessary directories
2. Make scripts executable
3. Offer to install the cron job automatically
4. Provide manual installation instructions if preferred

### Option 2: Manual Setup

1. Make the cron script executable:
```bash
chmod +x /Users/nimeshkhatri/github/news-screener/cron_scrape.sh
```

2. Open your crontab:
```bash
crontab -e
```

3. Add ONE of the following lines:

**For automatic DST adjustment (RECOMMENDED):**
```cron
0 7 * * * TZ='America/Los_Angeles' /Users/nimeshkhatri/github/news-screener/cron_scrape.sh >> /Users/nimeshkhatri/github/news-screener/logs/cron.log 2>&1
```

**For fixed UTC time (14:00 UTC = 7 AM PDT during daylight saving):**
```cron
0 14 * * * /Users/nimeshkhatri/github/news-screener/cron_scrape.sh >> /Users/nimeshkhatri/github/news-screener/logs/cron.log 2>&1
```

**For fixed UTC time (15:00 UTC = 7 AM PST during standard time):**
```cron
0 15 * * * /Users/nimeshkhatri/github/news-screener/cron_scrape.sh >> /Users/nimeshkhatri/github/news-screener/logs/cron.log 2>&1
```

4. Save and exit (in vim: press `ESC`, type `:wq`, press `ENTER`)

5. Verify the cron job was installed:
```bash
crontab -l
```

## 🕐 Understanding Timezones

### PDT vs PST
- **PDT (Pacific Daylight Time)**: UTC-7 (March - November)
- **PST (Pacific Standard Time)**: UTC-8 (November - March)

### Why Use TZ='America/Los_Angeles'?
Using `TZ='America/Los_Angeles'` automatically handles DST changes, so your scraper always runs at 7:00 AM Pacific Time regardless of whether it's PDT or PST.

### Cron Time Format
```
* * * * * command
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, Sunday=0 or 7)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

Examples:
- `0 7 * * *` - Every day at 7:00 AM (in server's timezone)
- `0 14 * * *` - Every day at 14:00 (2:00 PM) UTC
- `0 7 * * 1` - Every Monday at 7:00 AM
- `0 7 1 * *` - First day of every month at 7:00 AM

## 📊 Monitoring and Maintenance

### View Cron Logs
```bash
# View all logs
cat /Users/nimeshkhatri/github/news-screener/logs/cron.log

# View last 50 lines
tail -50 /Users/nimeshkhatri/github/news-screener/logs/cron.log

# Follow logs in real-time
tail -f /Users/nimeshkhatri/github/news-screener/logs/cron.log

# View logs from today
grep "$(date +%Y-%m-%d)" /Users/nimeshkhatri/github/news-screener/logs/cron.log
```

### Test the Scraper Manually
```bash
# Run with full output
cd /Users/nimeshkhatri/github/news-screener
python3 auto_scrape.py

# Run with quiet mode (same as cron)
python3 auto_scrape.py --quiet

# Test the cron script
bash cron_scrape.sh
```

### Check Cron Status
```bash
# List all cron jobs
crontab -l

# Check if cron daemon is running (macOS)
sudo launchctl list | grep cron

# Check system logs for cron (macOS)
log show --predicate 'process == "cron"' --last 1h
```

### Modify Cron Schedule
```bash
# Edit crontab
crontab -e

# Example: Change to run every 6 hours
0 */6 * * * TZ='America/Los_Angeles' /Users/nimeshkhatri/github/news-screener/cron_scrape.sh >> /Users/nimeshkhatri/github/news-screener/logs/cron.log 2>&1

# Example: Run twice a day (7 AM and 7 PM)
0 7,19 * * * TZ='America/Los_Angeles' /Users/nimeshkhatri/github/news-screener/cron_scrape.sh >> /Users/nimeshkhatri/github/news-screener/logs/cron.log 2>&1
```

### Remove Cron Job
```bash
# Edit crontab and remove the line
crontab -e

# Or remove all cron jobs (careful!)
crontab -r
```

## 🔧 Troubleshooting

### Cron Job Not Running

1. **Check if cron is installed:**
```bash
which cron
# On macOS, cron is built-in
```

2. **Verify cron job is in crontab:**
```bash
crontab -l
```

3. **Check script permissions:**
```bash
ls -l /Users/nimeshkhatri/github/news-screener/cron_scrape.sh
# Should show: -rwxr-xr-x
```

4. **Check logs directory exists:**
```bash
ls -ld /Users/nimeshkhatri/github/news-screener/logs
```

5. **Give cron full disk access (macOS Catalina+):**
   - Go to System Preferences → Security & Privacy → Privacy → Full Disk Access
   - Add `/usr/sbin/cron` or `/bin/bash`

### Script Runs But Fails

1. **Check error logs:**
```bash
tail -100 /Users/nimeshkhatri/github/news-screener/logs/cron.log
```

2. **Test script manually:**
```bash
cd /Users/nimeshkhatri/github/news-screener
bash cron_scrape.sh
```

3. **Check Python environment:**
```bash
which python3
python3 --version
```

4. **Verify database exists:**
```bash
ls -l /Users/nimeshkhatri/github/news-screener/news_screener.db
```

### Wrong Timezone

1. **Check system timezone:**
```bash
date
# Should show your current timezone
```

2. **For macOS, set timezone:**
```bash
sudo systemsetup -settimezone America/Los_Angeles
```

3. **Verify cron uses correct timezone:**
```bash
# In crontab, use the TZ variable:
0 7 * * * TZ='America/Los_Angeles' /path/to/script.sh
```

## 📝 Log File Format

Each cron run creates a log entry like this:

```
==================================================
🕐 Cron Job Started: 2025-10-27 07:00:01 PDT
==================================================
📍 Current timezone: PDT
🔧 Activating virtual environment...
🐍 Python version: Python 3.11.5

🤖 Starting automatic news scraping...

[Scraping output from auto_scrape.py]

✅ Scraping completed successfully

==================================================
🏁 Cron Job Finished: 2025-10-27 07:05:23 PDT
==================================================
```

## 🎯 Next Steps

After setting up cron:

1. **Wait for first run** or test manually:
```bash
bash cron_scrape.sh
```

2. **Check logs after scheduled time:**
```bash
tail -50 logs/cron.log
```

3. **View scraped articles:**
   - Open http://localhost:3000/haryana
   - Make sure backend is running: `cd backend && python3 main.py`

4. **Set up log rotation** (optional, prevents logs from growing too large):
```bash
# Create /etc/newsyslog.d/news-scraper.conf (requires sudo)
/Users/nimeshkhatri/github/news-screener/logs/*.log {
    rotate 7
    daily
    compress
    missingok
    notifempty
}
```

## 🔄 Alternative Scheduling Options

### Using launchd (macOS Alternative to Cron)

Create a plist file for more reliable scheduling on macOS:

```bash
# See LAUNCHD_SETUP.md for detailed instructions
# (We can create this file if you prefer launchd over cron)
```

### Using systemd timers (Linux)

For production Linux servers:

```bash
# See SYSTEMD_SETUP.md for detailed instructions
# (We can create this file if you need Linux deployment)
```

## 📚 Resources

- [Crontab Guru](https://crontab.guru/) - Interactive cron schedule expressions
- [Cron Format Reference](https://man7.org/linux/man-pages/man5/crontab.5.html)
- [macOS Cron Guide](https://ole.michelsen.dk/blog/schedule-jobs-with-crontab-on-mac-osx/)

## ⚙️ Configuration

To modify scraping behavior, edit `auto_scrape.py`:

```python
# Change sources to scrape
sources = db.query(Source).filter(Source.is_active == True).all()

# Adjust delays between sources
time.sleep(1)  # Wait 1 second between sources

# Enable verbose output in cron
# Modify cron_scrape.sh: python3 auto_scrape.py (remove --quiet)
```

## 🎉 Success!

Your news scraper is now running automatically every day at 7:00 AM Pacific Time. New articles will be available in your web interface shortly after each scrape completes.

