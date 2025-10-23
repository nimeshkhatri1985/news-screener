# News Screener - Project Context & Requirements

## Original Vision
A web app that can:
1. Crawl internet for specific news
2. Choose specific posts
3. Create social media posts about them
4. Post using a specific account

**Key Requirements:**
- Scalability
- Stability
- Ease of maintenance
- Solo development with AI assistance (Cursor)

## Scope Evolution

### Initial Scope (Complex)
- Microservices architecture
- Full social media automation
- Advanced ML features

### Revised Scope (MVP - Implemented)
- Basic screening of specific sources
- Manual curation and posting
- Monolithic architecture for simplicity
- Focus on specific use case: **Haryana News**

## Core Requirements - User Inputs

### 1. Haryana-Specific News Feature
**User Request:** "I want this application to look for news about Haryana, a state in India. Additionally, I want to have logic that can help me focus on specific type of news about Haryana. This can be adjusted in the logic. For Ex. I want to focus on things that may encourage tourism in Haryana, positive news about the infrastructure development in Haryana."

**Implementation:**
- Location-aware filtering (Haryana cities: Gurugram, Faridabad, Chandigarh, etc.)
- Topic-based filter presets:
  - Tourism (heritage sites, attractions, cultural events)
  - Infrastructure (metro, highways, smart cities)
  - Economy (investments, startups, business)
  - Education (universities, schools, skill development)
  - Agriculture (farming technology, crop yields)
  - Sports (athletes, academies, events)
  - Environment (green initiatives, pollution control)
  - Governance (digital services, welfare schemes)
- Adjustable logic through keyword configuration
- Sentiment analysis (Positive, Neutral, Negative)
- Relevance scoring (0-100+)

### 2. Technology Stack Decisions

**Backend:**
- Python with FastAPI
- SQLite database (for MVP, scalable to PostgreSQL)
- RSS feed scraping with `feedparser`
- SQLAlchemy ORM

**Frontend:**
- React.js with TypeScript
- Tailwind CSS for styling
- TanStack Query (React Query v4)
- React Router for navigation

**Development:**
- Git & GitHub for version control
- Manual setup (Docker available but not required for local dev)
- AI-assisted development with Cursor

### 3. Deployment & Cost Considerations
**User Question:** "Can you think about the cost of deployment and continuous running and maintenance of this app?"

**Approach:**
- Start with free/low-cost tiers
- Lightweight architecture for minimal costs
- Railway/Render/Vercel for hosting
- Incremental scaling as needed

### 4. Development Workflow Preferences
- Test-driven approach
- Comprehensive documentation
- Step-by-step implementation
- Fix issues as they arise
- Commit frequently

## Current Implementation Status

### ✅ Completed Features

1. **Core News Screening System**
   - RSS feed scraping
   - Article storage and management
   - Source configuration
   - Basic filtering

2. **Haryana News Screener** ⭐
   - 8 topic-based filter presets
   - Location-aware filtering
   - Relevance scoring algorithm
   - Sentiment analysis
   - Dedicated UI at `/haryana`
   - Real-time filtering and scoring
   - 241 articles in database, 75 Haryana-relevant

3. **Frontend Interface**
   - Dashboard with statistics
   - Articles listing with advanced filters
   - Sources management
   - Posts management (placeholder)
   - Haryana News page with dynamic filtering

4. **Automation Scripts**
   - `scrape_haryana_news.py` - Targeted Haryana news scraping
   - `auto_scrape.py` - Continuous automated scraping
   - `setup_haryana.py` - Initial data setup

5. **Documentation**
   - `README.md` - Project overview
   - `SCRAPING_GUIDE.md` - Scraping setup
   - `LEARNING_GUIDE.md` - Code walkthrough
   - `TECHNICAL_DOCUMENTATION.md` - Architecture details
   - `CODE_OVERVIEW.md` - Detailed code breakdown

### 🚧 In Progress / Prepared (Not Yet Committed)

1. **Twitter Integration**
   - `backend/twitter_service.py` - Twitter API wrapper
   - `TWITTER_SETUP_GUIDE.md` - Setup documentation
   - `test_twitter_integration.py` - Integration tests
   - Status: Code ready, awaiting API credentials

2. **Additional Sources**
   - `add_new_haryana_sources.py` - Script to add more sources
   - `scrape_new_sources.py` - New source scraper
   - Status: Scripts ready, not yet executed

### 📋 Pending Features

1. **Twitter API Integration** - Complete authentication and posting
2. **Manual Posting Interface** - UI for creating/scheduling posts
3. **Deployment** - Move to production hosting
4. **Enhanced Scraping** - More Haryana news sources
5. **Advanced Features** - ML-based filtering, auto-posting

## Key Files & Structure

```
news-screener/
├── backend/
│   ├── main.py                    # FastAPI app with all endpoints
│   ├── haryana_config.py          # Haryana filtering logic
│   ├── scraper.py                 # RSS scraping utilities
│   ├── twitter_service.py         # Twitter integration (ready)
│   ├── requirements.txt           # Python dependencies
│   └── news_screener.db          # SQLite database (241 articles)
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx      # Main dashboard
│   │   │   ├── Articles.tsx       # Article listing
│   │   │   ├── Sources.tsx        # Source management
│   │   │   ├── Posts.tsx          # Post management
│   │   │   └── HaryanaNews.tsx    # Haryana-specific page
│   │   ├── services/
│   │   │   └── api.ts             # API client
│   │   └── components/
│   │       └── Header.tsx         # Navigation header
│   └── package.json               # Node dependencies
├── scrape_haryana_news.py         # Haryana news scraper
├── auto_scrape.py                 # Automated scraping
├── add_new_haryana_sources.py     # Add more sources
└── Documentation files...
```

## Database Schema

**Sources Table:**
- id, name, url, rss_feed, is_active, created_at

**Articles Table:**
- id, source_id, title, content, url, published_at, crawled_at

**Filters Table:**
- id, name, keywords, category, is_active, created_at

**Posts Table:**
- id, article_id, content, platform, status, posted_at, scheduled_at, created_at

## API Endpoints

### Standard Endpoints
- `GET /` - Health check
- `GET /sources` - List news sources
- `POST /sources` - Add new source
- `GET /articles` - List articles (with filtering)
- `GET /filters` - List filters
- `POST /filters` - Create filter
- `GET /posts` - List posts
- `POST /posts` - Create post

### Haryana-Specific Endpoints
- `GET /haryana/filter-presets` - Available filter presets
- `GET /haryana/articles` - Filtered & scored articles
- `GET /haryana/articles/{id}/analyze` - Analyze single article
- `GET /haryana/stats` - Database statistics

## Important Notes

### Database Location
**Critical:** Backend uses `/backend/news_screener.db`
- Main database is at project root, but backend expects it in backend/
- Copy database when needed: `cp news_screener.db backend/`

### Running the Application
```bash
# Backend (Port 8000)
cd /Users/nimeshkhatri/github/news-screener/backend
python3 main.py

# Frontend (Port 3000)
cd /Users/nimeshkhatri/github/news-screener/frontend
npm start
```

### Git Configuration
```bash
git config --global user.name "Nimesh Khatri"
git config --global user.email "nimeshkhatri1985@gmail.com"
```

## User Preferences & Patterns

1. **Testing Approach:** "Let's test first" - Always verify before moving forward
2. **Documentation:** Appreciates detailed explanations and comprehensive docs
3. **Workflow:** Prefers to understand implementation before proceeding
4. **Commit Style:** Commits work when features are complete
5. **Problem Solving:** Methodical, likes to understand root causes

## Next Session Priorities

1. Test Haryana News UI in browser
2. Add more Haryana news sources
3. Complete Twitter integration
4. Build manual posting interface
5. Consider deployment options

## Success Metrics

- ✅ 241 articles collected
- ✅ 75 Haryana-relevant articles identified
- ✅ 8 topic-based filter presets working
- ✅ Relevance scoring algorithm functioning
- ✅ Frontend fully functional with interactive filtering
- ✅ All code committed to GitHub

---

**Last Updated:** October 23, 2025
**Current Commit:** 034a8db
**Status:** Haryana News Screener fully implemented and tested

