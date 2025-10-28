#!/bin/bash
# Cron job script for daily news scraping
# Designed to run at 7:00 AM PDT (Pacific Daylight Time)
# 
# To install:
# 1. Make executable: chmod +x cron_scrape.sh
# 2. Edit crontab: crontab -e
# 3. Add line: 0 14 * * * /Users/nimeshkhatri/github/news-screener/cron_scrape.sh >> /Users/nimeshkhatri/github/news-screener/logs/cron.log 2>&1
#
# Note: PDT is UTC-7, so 7:00 AM PDT = 14:00 UTC (2:00 PM UTC)
#       PST is UTC-8, so 7:00 AM PST = 15:00 UTC (3:00 PM UTC)

# Set working directory
cd /Users/nimeshkhatri/github/news-screener

# Create logs directory if it doesn't exist
mkdir -p logs

# Log start time with timezone info
echo "=================================================="
echo "🕐 Cron Job Started: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "=================================================="

# Check current timezone
CURRENT_TZ=$(date '+%Z')
echo "📍 Current timezone: $CURRENT_TZ"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "🔧 Activating virtual environment..."
    source .venv/bin/activate
fi

# Verify Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: python3 not found!"
    exit 1
fi

echo "🐍 Python version: $(python3 --version)"

# Run the scraping script
echo ""
echo "🤖 Starting automatic news scraping..."
echo ""

python3 auto_scrape.py --quiet

# Capture exit status
EXIT_STATUS=$?

if [ $EXIT_STATUS -eq 0 ]; then
    echo ""
    echo "✅ Scraping completed successfully"
else
    echo ""
    echo "❌ Scraping failed with exit status: $EXIT_STATUS"
fi

# Log end time
echo ""
echo "=================================================="
echo "🏁 Cron Job Finished: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "=================================================="
echo ""

exit $EXIT_STATUS

