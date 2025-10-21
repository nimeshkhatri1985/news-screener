# News Screener

A full-stack web application for monitoring news sources, filtering articles, and creating social media posts.

## Features

- **News Source Management**: Add and manage RSS feeds from various news sources
- **Advanced Filtering**: Filter articles by keywords, categories, date ranges, and sources
- **Article Browsing**: Search and browse articles with real-time filtering
- **Post Creation**: Create social media posts from curated articles
- **🌟 Haryana News Screener**: Specialized filtering for Haryana-specific news with:
  - 8 topic-based filter presets (Tourism, Infrastructure, Economy, Education, etc.)
  - Automatic sentiment analysis (Positive, Neutral, Negative)
  - Relevance scoring based on keywords and indicators
  - Location-aware filtering for all Haryana cities and regions
- **Responsive Design**: Modern UI with Tailwind CSS
- **Real-time Data**: Live updates with React Query

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Database (development)
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend
- **React 18**: Modern React with hooks
- **TypeScript**: Type-safe JavaScript
- **TanStack Query**: Data fetching and caching
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client

### Development Tools
- **Docker**: Containerization
- **Docker Compose**: Multi-service orchestration
- **ESLint**: Code linting
- **Prettier**: Code formatting

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Docker (optional)

### Manual Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd news-screener
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   # Set up Haryana news sources and filters
   python setup_haryana.py
   # Start the backend
   python main.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Haryana News: http://localhost:3000/haryana
   - API Documentation: http://localhost:8000/docs

### Docker Setup

1. **Start all services**
   ```bash
   docker-compose up
   ```

2. **Access the application**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000

## Project Structure

```
news-screener/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── scraper.py          # RSS feed scraper
│   ├── celery_tasks.py     # Background tasks
│   └── Dockerfile          # Backend container
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── index.tsx       # App entry point
│   ├── package.json        # Node dependencies
│   └── Dockerfile          # Frontend container
├── docker-compose.yml      # Multi-service setup
├── README.md              # This file
└── start.sh               # Quick start script
```

## API Endpoints

### Sources
- `GET /sources` - List all news sources
- `POST /sources` - Create new source

### Articles
- `GET /articles` - List articles with filtering
- `GET /search?q=term` - Search articles

### Filters
- `GET /filters` - List all filters
- `POST /filters` - Create new filter

### Posts
- `GET /posts` - List all posts
- `POST /posts` - Create new post

## Development

### Backend Development
```bash
cd backend
python main.py
```

### Frontend Development
```bash
cd frontend
npm start
```

### Testing
```bash
# Backend tests
python test_api.py

# Frontend tests
npm test
```

## Deployment

### Production Setup
1. Set up PostgreSQL database
2. Configure environment variables
3. Deploy with Docker or cloud platform

### Environment Variables
```bash
DATABASE_URL=postgresql://user:password@localhost/news_screener
REDIS_URL=redis://localhost:6379
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Roadmap

- [ ] Twitter API integration
- [ ] Real-time article scraping
- [ ] Post scheduling
- [ ] Analytics dashboard
- [ ] User authentication
- [ ] Multi-user support

## Support

For questions or issues, please open a GitHub issue or contact the development team.