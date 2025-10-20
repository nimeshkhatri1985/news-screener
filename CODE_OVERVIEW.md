# Code Overview - News Screener App

## File Structure & Purpose

```
news-screener/
├── README.md                           # Project overview and setup instructions
├── TECHNICAL_DOCUMENTATION.md          # Detailed technical documentation
├── docker-compose.yml                  # Multi-service development environment
├── start.sh                           # Automated startup script
├── test_setup.py                      # Setup verification script
├── env.example                        # Environment variables template
│
├── backend/                           # FastAPI Backend Application
│   ├── main.py                        # Core API application and routes
│   ├── scraper.py                     # RSS feed scraping logic
│   ├── celery_tasks.py               # Background job definitions
│   ├── setup_initial_data.py         # Database initialization script
│   ├── requirements.txt               # Python dependencies
│   └── Dockerfile                    # Backend container configuration
│
└── frontend/                          # React Frontend Application
    ├── package.json                   # Node.js dependencies and scripts
    ├── Dockerfile                    # Frontend container configuration
    ├── tailwind.config.js            # Tailwind CSS configuration
    └── src/
        ├── index.tsx                  # React application entry point
        ├── index.css                  # Global styles and Tailwind imports
        ├── App.tsx                    # Main application component
        ├── components/
        │   └── Header.tsx            # Navigation header component
        ├── pages/
        │   ├── Dashboard.tsx         # Main dashboard page
        │   ├── Sources.tsx           # News sources management
        │   ├── Articles.tsx          # Articles browsing and filtering
        │   └── Posts.tsx             # Social media posts management
        └── services/
            └── api.ts                # API client and type definitions
```

---

## Core Components Breakdown

### 1. Backend (`backend/`)

#### `main.py` - Core API Application
**Purpose**: Main FastAPI application with all API endpoints
**Key Features**:
- Database models (Source, Article, Filter, Post)
- RESTful API endpoints
- Pydantic request/response models
- CORS middleware configuration
- Database session management

**Key Functions**:
```python
# Database Models
class Source(Base):          # News source management
class Article(Base):         # Scraped articles storage
class Filter(Base):          # Content filtering rules
class Post(Base):           # Social media posts

# API Endpoints
@app.get("/sources")        # List/create news sources
@app.get("/articles")       # Browse articles with filtering
@app.get("/posts")          # Manage social media posts
@app.get("/filters")        # Content filtering rules
```

#### `scraper.py` - News Scraping Engine
**Purpose**: RSS feed parsing and article extraction
**Key Features**:
- RSS feed parsing with feedparser
- HTML content extraction with BeautifulSoup
- Date parsing for multiple formats
- Error handling and logging
- Rate limiting and respectful scraping

**Key Functions**:
```python
class NewsScraper:
    def scrape_rss_feed()           # Parse RSS feeds
    def _parse_date()              # Handle various date formats
    def _extract_content()         # Extract clean text content
    def scrape_article_content()   # Full article scraping
    def save_articles()           # Database persistence
    def scrape_all_sources()      # Batch processing
```

#### `celery_tasks.py` - Background Jobs
**Purpose**: Scheduled and asynchronous task processing
**Key Features**:
- Celery task definitions
- Scheduled scraping (every 30 minutes)
- Redis backend for task queue
- Task monitoring and error handling

**Key Functions**:
```python
@celery_app.task
def scrape_news_sources()    # Scheduled news scraping

# Beat schedule configuration
celery_app.conf.beat_schedule = {
    "scrape-news-every-30-minutes": {
        "task": "celery_tasks.scrape_news_sources",
        "schedule": 30.0 * 60.0,
    },
}
```

#### `setup_initial_data.py` - Database Initialization
**Purpose**: Populate database with initial news sources
**Key Features**:
- Pre-configured popular tech news sources
- Duplicate prevention
- Test data for development

**Initial Sources**:
- TechCrunch
- The Verge
- Ars Technica
- Wired
- Hacker News

### 2. Frontend (`frontend/`)

#### `App.tsx` - Main Application Component
**Purpose**: Application root with routing and global providers
**Key Features**:
- React Router for navigation
- React Query for data management
- Global layout structure
- Route definitions

**Route Structure**:
```typescript
<Routes>
  <Route path="/" element={<Dashboard />} />
  <Route path="/sources" element={<Sources />} />
  <Route path="/articles" element={<Articles />} />
  <Route path="/posts" element={<Posts />} />
</Routes>
```

#### `components/Header.tsx` - Navigation Component
**Purpose**: Application navigation and branding
**Key Features**:
- Responsive navigation menu
- Active route highlighting
- Icon integration (Heroicons)
- Mobile-friendly design

#### `pages/Dashboard.tsx` - Main Dashboard
**Purpose**: Overview of application activity and statistics
**Key Features**:
- Statistics cards (articles, sources, posts)
- Recent articles preview
- Quick action buttons
- Loading states and error handling

**Statistics Displayed**:
- Total Articles count
- Active Sources count
- Posts Created count
- Success Rate percentage

#### `pages/Sources.tsx` - Source Management
**Purpose**: Add and manage news sources
**Key Features**:
- Add new RSS sources form
- List active sources
- Source status management
- Form validation and error handling

#### `pages/Articles.tsx` - Article Browser
**Purpose**: Browse and filter scraped articles
**Key Features**:
- Article listing with pagination
- Source-based filtering
- Search functionality
- External link integration
- Post creation from articles

#### `pages/Posts.tsx` - Post Management
**Purpose**: Create and manage social media posts
**Key Features**:
- Post creation form
- Article selection dropdown
- Character count tracking
- Post status management
- Posting history

#### `services/api.ts` - API Client
**Purpose**: Centralized API communication and type definitions
**Key Features**:
- TypeScript interfaces for all data models
- Axios HTTP client configuration
- Type-safe API methods
- Error handling

**API Methods**:
```typescript
// Sources
getSources()              // Fetch all sources
createSource()            // Add new source

// Articles
getArticles()            // Fetch articles with filtering

// Posts
getPosts()               // Fetch all posts
createPost()             // Create new post

// Filters
getFilters()             // Fetch filtering rules
createFilter()           // Add new filter
```

### 3. Configuration Files

#### `docker-compose.yml` - Development Environment
**Purpose**: Multi-service development setup
**Services**:
- PostgreSQL database
- Redis cache
- Backend API service
- Frontend React app

#### `requirements.txt` - Python Dependencies
**Core Dependencies**:
- FastAPI (web framework)
- SQLAlchemy (ORM)
- PostgreSQL driver (psycopg2)
- Celery (task queue)
- Redis (cache)
- Requests (HTTP client)
- BeautifulSoup (HTML parsing)
- Feedparser (RSS parsing)

#### `package.json` - Node.js Dependencies
**Core Dependencies**:
- React (UI framework)
- TypeScript (type safety)
- React Router (navigation)
- React Query (data fetching)
- Axios (HTTP client)
- Tailwind CSS (styling)
- Heroicons (icons)

---

## Data Flow Architecture

### 1. News Scraping Flow
```
RSS Feeds → NewsScraper → Database → API → Frontend
```

**Process**:
1. Celery scheduler triggers scraping task
2. NewsScraper fetches RSS feeds from all active sources
3. Articles are parsed and cleaned
4. New articles are saved to PostgreSQL
5. Frontend displays articles via API

### 2. Content Curation Flow
```
Articles → User Selection → Post Creation → Social Media
```

**Process**:
1. User browses articles on frontend
2. User selects article for posting
3. User creates curated post content
4. Post is saved to database
5. Post can be published to social media (future)

### 3. API Communication Flow
```
Frontend → API Client → FastAPI → Database → Response
```

**Process**:
1. React components make API calls
2. Axios client sends HTTP requests
3. FastAPI processes requests
4. SQLAlchemy queries database
5. Pydantic models serialize responses
6. React Query caches and updates UI

---

## Key Design Patterns

### 1. Repository Pattern
```python
# Database operations centralized in models
class Source(Base):
    # Model definition with relationships
    
# API endpoints use dependency injection
def get_sources(db: Session = Depends(get_db)):
    return db.query(Source).all()
```

### 2. Service Layer Pattern
```typescript
// API service layer abstracts HTTP communication
export const getSources = async (): Promise<Source[]> => {
  const response = await api.get('/sources');
  return response.data;
};
```

### 3. Component Composition
```typescript
// Reusable components with clear interfaces
const Dashboard: React.FC = () => {
  // Component logic
  return (
    <div>
      <StatsCards stats={stats} />
      <RecentArticles articles={articles} />
      <QuickActions />
    </div>
  );
};
```

### 4. Error Boundary Pattern
```typescript
// React Query provides error boundaries
const { data, error, isLoading } = useQuery(
  'articles',
  () => api.getArticles(),
  {
    retry: 3,
    onError: (error) => console.error(error)
  }
);
```

---

## Development Workflow

### 1. Local Development
```bash
# Start all services
./start.sh

# Or manually:
docker-compose up -d
```

### 2. Code Organization
- **Backend**: Domain-driven structure (models, services, tasks)
- **Frontend**: Feature-based structure (pages, components, services)
- **Shared**: Common types and interfaces

### 3. Testing Strategy
- **Backend**: Unit tests for scraper logic
- **Frontend**: Component testing with React Testing Library
- **Integration**: API endpoint testing
- **E2E**: Full workflow testing

### 4. Deployment Pipeline
- **Development**: Docker Compose
- **Staging**: Cloud platform (Railway/Vercel)
- **Production**: Kubernetes or managed services

---

## Security Considerations

### 1. Input Validation
- Pydantic models validate all API inputs
- SQLAlchemy ORM prevents SQL injection
- TypeScript prevents type-related errors

### 2. CORS Configuration
- Restricted origins for production
- Development-friendly for local testing
- Credential support for authentication

### 3. Environment Security
- Sensitive data in environment variables
- No secrets in code repository
- Database credentials externalized

---

## Performance Optimizations

### 1. Database
- Indexed columns for common queries
- Pagination for large result sets
- Connection pooling for scalability

### 2. Frontend
- React Query caching reduces API calls
- Memoized components prevent re-renders
- Lazy loading for large datasets

### 3. Backend
- Async/await for non-blocking operations
- Background tasks for heavy operations
- Efficient data serialization

---

## Future Enhancements

### 1. Immediate (Week 2-3)
- Keyword filtering system
- Advanced search functionality
- Twitter API integration
- Post scheduling

### 2. Medium-term (Month 2-3)
- Multiple social media platforms
- AI-powered content analysis
- Advanced analytics dashboard
- User authentication

### 3. Long-term (Month 4-6)
- Microservices architecture
- Real-time notifications
- Mobile application
- Enterprise features

---

This codebase represents a solid foundation for a scalable news monitoring and social media curation platform, built with modern technologies and following industry best practices.
