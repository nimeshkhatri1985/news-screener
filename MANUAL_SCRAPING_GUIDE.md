# Manual Scraping Feature

## Overview

In addition to the automated cron-based scraping that runs daily at 7:00 AM PDT, you can now manually trigger news scraping on-demand directly from the web interface.

## How to Use

### 1. Access the Haryana News Page

Open your browser and navigate to:
```
http://localhost:3000/haryana
```

### 2. Locate the "Scrape Now" Button

In the header section of the page (top-right corner), you'll see a green button with a refresh icon labeled **"Scrape Now"**.

### 3. Trigger Manual Scraping

Click the **"Scrape Now"** button to start scraping immediately.

**What happens:**
- The button changes to **"Scraping..."** with a spinning animation
- The scraper fetches news from all active sources
- Articles are analyzed for Haryana relevance
- New articles are categorized and scored
- Results are saved to the database

### 4. View Results

After scraping completes (typically 30 seconds to 2 minutes):

**Success message shows:**
- Number of articles found
- Number of new articles added
- Automatic page refresh to show new content

**Example:**
```
✅ Scraping complete! Found 45 articles, 12 new. Refresh page to see updates.
```

The page will automatically reload after 3 seconds to display the newly scraped articles.

## When to Use Manual Scraping

Use the manual scraping feature when:

✅ **Breaking News**: Major events occur and you want immediate updates  
✅ **Testing**: Verify that sources are configured correctly  
✅ **On-Demand**: Need fresh content outside the scheduled 7 AM scraping  
✅ **After Adding Sources**: Immediately fetch articles from newly added sources  
✅ **Quality Check**: Ensure the scraping and filtering system is working

## Technical Details

### Backend API Endpoints

#### Trigger Scraping
```
POST /scrape/trigger
```

**Response:**
```json
{
  "success": true,
  "message": "Scraping completed successfully",
  "results": {
    "sources_scraped": 5,
    "articles_found": 45,
    "new_articles": 12,
    "errors": []
  }
}
```

#### Get Scraping Status
```
GET /scrape/status
```

**Response:**
```json
{
  "total_articles": 487,
  "last_24h": 32,
  "last_hour": 12,
  "latest_article": {
    "title": "Haryana launches new tourism initiative",
    "crawled_at": "2025-10-27T14:30:00Z"
  },
  "active_sources": 5
}
```

### Frontend Implementation

The scraping button is implemented using:
- React Query `useMutation` for API calls
- State management for success/error messages
- Automatic page reload after successful scraping
- Loading states with spinner animation
- Error handling with user-friendly messages

### Scraping Process

When you click "Scrape Now":

1. **Fetch RSS Feeds** - Gets latest articles from all active sources
2. **Parse Content** - Extracts title, content, URL, and publish date
3. **Check Duplicates** - Skips articles already in database
4. **Analyze Relevance** - Scores articles for Haryana relevance
5. **Categorize** - Assigns topics (tourism, infrastructure, etc.)
6. **Save to Database** - Stores new articles with metadata
7. **Return Results** - Shows statistics and refreshes UI

## Performance

### Typical Duration
- **Small sources (5 sources)**: 30-60 seconds
- **Medium sources (10 sources)**: 1-2 minutes
- **Large sources (20+ sources)**: 2-4 minutes

### Resource Usage
- **CPU**: Moderate during scraping
- **Memory**: ~50-100 MB
- **Network**: Depends on RSS feed sizes
- **Database**: Adds 5-50 articles per scrape (varies)

## Troubleshooting

### Button is Disabled
**Issue:** The "Scrape Now" button is grayed out and won't click

**Solutions:**
- Scraping is already in progress - wait for it to complete
- Check browser console for JavaScript errors
- Refresh the page and try again

### Error: "Failed to trigger scraping"
**Issue:** Red error message appears after clicking

**Solutions:**
1. **Check Backend Status**:
```bash
# Make sure backend is running
cd backend
python3 main.py
```

2. **Check Network Connection**:
   - Verify `http://localhost:8000` is accessible
   - Check browser network tab for failed requests

3. **Check Logs**:
```bash
# Check backend terminal for error messages
```

### No New Articles
**Issue:** Scraping completes but shows "0 new articles"

**Reasons (Normal):**
- All articles are already in the database
- Sources haven't published new content
- RSS feeds are up to date

**Not an error** - This is expected behavior when everything is current.

### Scraping Takes Too Long
**Issue:** Scraping runs for more than 5 minutes

**Solutions:**
1. **Check Source URLs**:
   - Some RSS feeds may be slow or unresponsive
   - Remove slow/broken sources

2. **Check Network**:
   - Slow internet connection
   - DNS resolution issues

3. **Check Logs**:
```bash
# Backend will show which source is stuck
```

## Comparison: Manual vs Automated Scraping

| Feature | Manual Scraping | Automated (Cron) |
|---------|----------------|------------------|
| **Trigger** | User clicks button | Scheduled (7 AM PDT) |
| **Timing** | On-demand anytime | Once per day |
| **Use Case** | Breaking news, testing | Regular updates |
| **Feedback** | Immediate UI feedback | Logged to file |
| **Duration** | Same (30s-2min) | Same (30s-2min) |
| **Results** | Auto page refresh | Available next visit |

## Best Practices

### ✅ DO:
- Use manual scraping for breaking news or urgent updates
- Wait for scraping to complete before clicking again
- Check the results message for statistics
- Use during testing and development

### ❌ DON'T:
- Click the button repeatedly (it's disabled during scraping)
- Scrape too frequently (sources may rate-limit)
- Expect instant results (scraping takes time)
- Worry about "0 new articles" (means you're up to date)

## Integration with Cron

Manual scraping and automated cron scraping work together:

1. **Cron Scraping**: Runs automatically at 7 AM PDT daily
2. **Manual Scraping**: Available anytime via the button
3. **No Conflicts**: Both use the same code and duplicate detection
4. **Complementary**: Cron for routine, manual for urgent updates

### Example Workflow

**Morning (7:00 AM PDT)**
- Cron job runs automatically
- Fetches overnight news
- Articles ready when you start work

**Afternoon (2:00 PM PDT)**
- Breaking news: Major infrastructure announcement
- Click "Scrape Now" to get latest articles
- New content appears immediately

**No Double Work**: If you manually scrape at 6:30 AM and cron runs at 7:00 AM, the cron job will only add articles published after 6:30 AM.

## API Usage Examples

### Using cURL

```bash
# Trigger scraping
curl -X POST http://localhost:8000/scrape/trigger

# Check status
curl http://localhost:8000/scrape/status
```

### Using Python

```python
import requests

# Trigger scraping
response = requests.post('http://localhost:8000/scrape/trigger')
results = response.json()
print(f"New articles: {results['results']['new_articles']}")

# Check status
status = requests.get('http://localhost:8000/scrape/status').json()
print(f"Total articles: {status['total_articles']}")
print(f"Added in last 24h: {status['last_24h']}")
```

### Using JavaScript/Fetch

```javascript
// Trigger scraping
fetch('http://localhost:8000/scrape/trigger', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' }
})
.then(res => res.json())
.then(data => {
  console.log(`Found ${data.results.articles_found} articles`);
  console.log(`New: ${data.results.new_articles}`);
});

// Check status
fetch('http://localhost:8000/scrape/status')
.then(res => res.json())
.then(data => {
  console.log(`Total: ${data.total_articles}`);
  console.log(`Recent: ${data.last_24h}`);
});
```

## Future Enhancements

Potential improvements to the manual scraping feature:

- **Progress Bar**: Show real-time progress during scraping
- **Source Selection**: Choose specific sources to scrape
- **Background Processing**: Don't block the UI while scraping
- **Notifications**: Desktop/browser notifications when complete
- **Scheduling**: Schedule a scrape for a specific time
- **Webhooks**: Trigger scraping from external events

## Related Documentation

- **CRON_QUICK_START.md** - Setting up automated daily scraping
- **CRON_SETUP_GUIDE.md** - Detailed cron configuration
- **auto_scrape.py** - Python scraper implementation
- **backend/scraper.py** - RSS feed scraping logic
- **frontend/src/services/api.ts** - Frontend API integration

## Summary

The manual scraping feature provides flexibility and control:

✅ **On-Demand Updates**: Get fresh news anytime  
✅ **User-Friendly**: Simple one-click operation  
✅ **Reliable**: Same proven scraping logic as cron  
✅ **Informative**: Clear feedback on results  
✅ **Complementary**: Works alongside automated scraping  

Combined with the automated cron scheduling, you now have complete control over when and how news is collected!

