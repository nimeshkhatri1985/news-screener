#!/bin/bash

# Cron script to run daily news scraping
# This script is called by cron daily at 7 AM Pacific time

cd /Users/nimeshkhatri/github/news-screener

# Activate virtual environment if it exists (optional)
# source venv/bin/activate

# Run the auto scrape script
python3 auto_scrape.py --quiet

# Exit with success code
exit 0

