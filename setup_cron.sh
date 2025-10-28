#!/bin/bash
# Setup script for cron-based news scraping
# This script helps you configure automatic daily scraping at 7:00 AM PDT

echo "=================================================="
echo "🤖 NEWS SCRAPER - CRON SETUP"
echo "=================================================="
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CRON_SCRIPT="$SCRIPT_DIR/cron_scrape.sh"
LOG_FILE="$SCRIPT_DIR/logs/cron.log"

echo "📁 Project directory: $SCRIPT_DIR"
echo ""

# Create logs directory
mkdir -p "$SCRIPT_DIR/logs"
echo "✅ Created logs directory: $SCRIPT_DIR/logs"

# Make cron script executable
chmod +x "$CRON_SCRIPT"
echo "✅ Made cron_scrape.sh executable"
echo ""

# Explain timezone
echo "🕐 TIMEZONE INFORMATION"
echo "=================================================="
echo "Current time: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "Current timezone: $(date '+%Z')"
echo ""
echo "⚠️  IMPORTANT: PDT vs PST"
echo "   • PDT (Pacific Daylight Time) = UTC-7"
echo "   • PST (Pacific Standard Time) = UTC-8"
echo ""
echo "For 7:00 AM Pacific Time:"
echo "   • During DST (Mar-Nov): Use 14:00 UTC (2 PM UTC)"
echo "   • During Standard (Nov-Mar): Use 15:00 UTC (3 PM UTC)"
echo ""

# Provide cron schedule options
echo "📅 CRON SCHEDULE OPTIONS"
echo "=================================================="
echo ""
echo "Option 1: Always 7:00 AM PDT (adjusts for DST automatically)"
echo "   Add this to crontab:"
echo "   0 7 * * * TZ='America/Los_Angeles' $CRON_SCRIPT >> $LOG_FILE 2>&1"
echo ""
echo "Option 2: Fixed UTC time - 14:00 UTC (7 AM PDT during DST)"
echo "   Add this to crontab:"
echo "   0 14 * * * $CRON_SCRIPT >> $LOG_FILE 2>&1"
echo ""
echo "Option 3: Fixed UTC time - 15:00 UTC (7 AM PST during standard time)"
echo "   Add this to crontab:"
echo "   0 15 * * * $CRON_SCRIPT >> $LOG_FILE 2>&1"
echo ""

# Check if cron is already set up
echo "🔍 Checking current crontab..."
if crontab -l 2>/dev/null | grep -q "cron_scrape.sh"; then
    echo "✅ Cron job already exists:"
    crontab -l | grep "cron_scrape.sh"
else
    echo "⚠️  No existing cron job found"
fi
echo ""

# Ask if user wants to install
echo "=================================================="
echo "📝 INSTALLATION OPTIONS"
echo "=================================================="
echo ""
echo "Choose an option:"
echo "  1) Install with automatic DST adjustment (RECOMMENDED)"
echo "  2) Install with fixed UTC time (14:00 UTC / 7 AM PDT)"
echo "  3) Show manual installation instructions"
echo "  4) Test the scraper now"
echo "  5) Exit"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo ""
        echo "Installing cron job with DST adjustment..."
        (crontab -l 2>/dev/null | grep -v "cron_scrape.sh"; echo "0 7 * * * TZ='America/Los_Angeles' $CRON_SCRIPT >> $LOG_FILE 2>&1") | crontab -
        echo "✅ Cron job installed!"
        echo ""
        echo "Your scraper will run daily at 7:00 AM Pacific Time"
        echo "Log file: $LOG_FILE"
        ;;
    2)
        echo ""
        echo "Installing cron job with fixed UTC time..."
        (crontab -l 2>/dev/null | grep -v "cron_scrape.sh"; echo "0 14 * * * $CRON_SCRIPT >> $LOG_FILE 2>&1") | crontab -
        echo "✅ Cron job installed!"
        echo ""
        echo "Your scraper will run daily at 14:00 UTC (7:00 AM PDT during DST)"
        echo "Log file: $LOG_FILE"
        ;;
    3)
        echo ""
        echo "=================================================="
        echo "📖 MANUAL INSTALLATION INSTRUCTIONS"
        echo "=================================================="
        echo ""
        echo "1. Open your crontab:"
        echo "   crontab -e"
        echo ""
        echo "2. Add ONE of these lines:"
        echo ""
        echo "   For automatic DST adjustment:"
        echo "   0 7 * * * TZ='America/Los_Angeles' $CRON_SCRIPT >> $LOG_FILE 2>&1"
        echo ""
        echo "   For fixed UTC time (14:00 UTC):"
        echo "   0 14 * * * $CRON_SCRIPT >> $LOG_FILE 2>&1"
        echo ""
        echo "3. Save and exit (in vim: press ESC, type :wq, press ENTER)"
        echo ""
        echo "4. Verify installation:"
        echo "   crontab -l"
        echo ""
        ;;
    4)
        echo ""
        echo "🧪 Running test scrape..."
        echo ""
        bash "$CRON_SCRIPT"
        echo ""
        echo "✅ Test complete! Check output above for results."
        echo ""
        ;;
    5)
        echo ""
        echo "Setup cancelled."
        echo ""
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "=================================================="
echo "📊 USEFUL COMMANDS"
echo "=================================================="
echo ""
echo "View crontab:        crontab -l"
echo "Edit crontab:        crontab -e"
echo "Remove all cron:     crontab -r"
echo "View logs:           tail -f $LOG_FILE"
echo "Test scraper:        bash $CRON_SCRIPT"
echo ""
echo "=================================================="
echo "✨ Setup Complete!"
echo "=================================================="
echo ""

