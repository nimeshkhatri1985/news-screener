# Haryana News Screener - Complete Guide

## Overview

The Haryana News Screener is a specialized module designed to intelligently filter and categorize news about Haryana, India. It uses topic-based filtering, keyword matching, and sentiment analysis to help you focus on specific types of news that matter most.

## Features

### 1. **Topic-Based Filter Presets**

The system includes 8 predefined filter categories:

#### 🌍 Tourism & Heritage
- **Focus**: Tourism development, heritage sites, cultural events
- **Examples**: New tourist attractions, heritage site inaugurations, cultural festivals, museum openings
- **Use Case**: Perfect for promoting Haryana's tourism potential and tracking positive developments in the tourism sector

#### 🏗️ Infrastructure Development
- **Focus**: Roads, highways, metro projects, construction, urban development
- **Examples**: New highway inaugurations, metro extensions, smart city projects, flyover completions
- **Use Case**: Track infrastructure improvements and development projects across the state

#### 💰 Economic Development
- **Focus**: Business, industry, investment, startups, manufacturing
- **Examples**: New factory openings, investment announcements, startup launches, industrial growth
- **Use Case**: Monitor economic progress and business opportunities in Haryana

#### 🎓 Education & Skill Development
- **Focus**: Schools, universities, skill training, educational achievements
- **Examples**: New college inaugurations, student achievements, educational reforms, scholarship programs
- **Use Case**: Track educational improvements and student success stories

#### 🌾 Agriculture & Rural Development
- **Focus**: Farming technology, crop yields, rural development, farmer welfare
- **Examples**: Bumper harvests, agricultural technology adoption, farmer subsidies, rural infrastructure
- **Use Case**: Monitor agricultural progress and rural development initiatives

#### 🏆 Sports & Recreation
- **Focus**: Sports achievements, athlete success, sports facilities
- **Examples**: Medal wins, new stadium openings, sports academy launches, athlete recognition
- **Use Case**: Track sports achievements and facility developments

#### 🌱 Environment & Sustainability
- **Focus**: Green initiatives, pollution control, renewable energy, conservation
- **Examples**: Tree plantation drives, pollution reduction, solar energy projects, wildlife conservation
- **Use Case**: Monitor environmental improvements and sustainability efforts

#### 🏛️ Governance & Public Services
- **Focus**: Government schemes, digital services, policy announcements
- **Examples**: New welfare schemes, e-governance initiatives, service improvements, policy reforms
- **Use Case**: Track government initiatives and public service improvements

### 2. **Sentiment Analysis**

Each article is automatically analyzed for sentiment:

- **Positive**: Articles with encouraging language, achievements, improvements, launches
- **Neutral**: Factual reporting without strong positive or negative indicators
- **Negative**: Articles about problems, setbacks, or challenges

**Sentiment Indicators**:
- Positive words: inaugurate, launch, improve, enhance, grow, achieve, success, award
- Negative words: decline, protest, damage, crisis, shutdown, controversy

### 3. **Relevance Scoring**

Articles are scored based on:
- **Keyword Matches**: Number of relevant keywords found (10 points each)
- **Positive Indicators**: Presence of positive action words (2 points each)
- **Negative Indicators**: Presence of negative words (-2 points each)
- **Location Relevance**: Mentions of Haryana cities and regions

**Example Scoring**:
```
Article: "New Tourism Complex Inaugurated in Kurukshetra"
- Keyword matches: tourism, inaugurated, Kurukshetra (30 points)
- Positive indicators: new, inaugurated (4 points)
- Total Score: 34
- Sentiment: Positive
```

### 4. **Location Detection**

The system automatically filters for articles mentioning Haryana locations:
- Major cities: Gurugram, Faridabad, Chandigarh, Panchkula, Ambala, Karnal, Panipat
- All 22 districts of Haryana
- Regional variations (e.g., Gurgaon/Gurugram)

## How to Use

### Step 1: Access Haryana News

1. Start the application (backend and frontend)
2. Click on **"Haryana News"** in the navigation menu
3. You'll see the Haryana News Screener dashboard

### Step 2: Select a Category

Choose one of the 8 filter preset categories based on your interest:
- Click on a category card (e.g., "Tourism & Heritage")
- The system will analyze all articles and show relevant ones

### Step 3: Refine Your Search

Use the advanced filters:

**Sentiment Filter**:
- Select "Positive Only" to see encouraging news
- Select "Neutral Only" for factual reporting
- Select "Negative Only" to be aware of challenges

**Minimum Relevance Score**:
- Set to 0 to see all matching articles
- Set to 20+ to see highly relevant articles
- Set to 50+ to see only the most relevant articles

### Step 4: Review Results

Each article shows:
- **Title and Content Preview**
- **Relevance Score**: How well it matches your selected category
- **Sentiment Badge**: Positive, Neutral, or Negative
- **Matched Keywords**: Keywords that triggered the match
- **Positive/Negative Indicators**: Specific words that influenced the sentiment

### Step 5: Read Full Details

Click on any article to see:
- Full article content
- Complete list of matched keywords
- All positive and negative indicators
- Link to original article

## Configuration & Customization

### Adding New Keywords

To customize the filter presets, edit `/backend/haryana_config.py`:

```python
HARYANA_FILTER_PRESETS = {
    "tourism": {
        "name": "Tourism & Heritage",
        "keywords": [
            # Add your custom keywords here
            "tourism", "tourist", "heritage", "temple",
            # ... more keywords
        ],
        "positive_indicators": [
            # Add positive action words
            "inaugurate", "launch", "improve",
            # ... more indicators
        ],
        "negative_indicators": [
            # Add negative words
            "close", "decline", "damage",
            # ... more indicators
        ]
    }
}
```

### Adjusting Sentiment Weights

Modify scoring weights in `haryana_config.py`:

```python
SENTIMENT_WEIGHTS = {
    "positive_indicator": 2.0,   # Increase for stronger positive scoring
    "negative_indicator": -2.0,  # Decrease for stronger negative scoring
    "positive_context": 1.0,
    "negative_context": -1.0,
    "neutral": 0.0
}
```

### Adding New Locations

Add new cities or regions to track:

```python
HARYANA_LOCATIONS = [
    "Haryana", "Chandigarh", "Gurugram",
    # Add new locations here
    "Your City", "Your Region"
]
```

## Use Cases

### 1. Tourism Promotion
**Goal**: Find positive news about tourism to promote on social media

**Steps**:
1. Select "Tourism & Heritage" category
2. Set Sentiment Filter to "Positive Only"
3. Set Minimum Score to 30
4. Review articles about new attractions, cultural events, heritage sites
5. Share the most relevant articles on social media

### 2. Infrastructure Tracking
**Goal**: Monitor infrastructure development progress

**Steps**:
1. Select "Infrastructure Development" category
2. Leave sentiment as "All Sentiments" to see both progress and challenges
3. Review articles about roads, metro, construction projects
4. Track completion milestones and new announcements

### 3. Investment Research
**Goal**: Identify economic opportunities and business growth

**Steps**:
1. Select "Economic Development" category
2. Set Sentiment Filter to "Positive Only"
3. Look for articles about new investments, factory openings, startup growth
4. Compile data for investment reports

### 4. Educational Achievements
**Goal**: Highlight educational success stories

**Steps**:
1. Select "Education & Skill Development" category
2. Set Sentiment Filter to "Positive Only"
3. Look for articles about student achievements, new institutions, educational reforms
4. Create social media posts celebrating successes

### 5. Environmental Monitoring
**Goal**: Track environmental initiatives and improvements

**Steps**:
1. Select "Environment & Sustainability" category
2. Review both positive and negative sentiment to understand challenges and progress
3. Focus on articles about green initiatives, pollution control, renewable energy
4. Advocate for environmental improvements

## API Endpoints

If you want to integrate programmatically:

### Get Filter Presets
```bash
GET http://localhost:8000/haryana/filter-presets
```

Returns all available filter categories and their descriptions.

### Get Filtered Articles
```bash
GET http://localhost:8000/haryana/articles?filter_preset=tourism&sentiment=positive&min_score=20
```

Parameters:
- `filter_preset`: tourism, infrastructure, economy, education, agriculture, sports, environment, governance
- `sentiment`: positive, neutral, negative (optional)
- `min_score`: minimum relevance score (optional, default: 0)
- `limit`: number of results (optional, default: 50)

### Analyze Specific Article
```bash
GET http://localhost:8000/haryana/articles/{article_id}/analyze?filter_preset=tourism
```

Returns detailed analysis of a specific article against a filter preset.

## News Sources

The system monitors these Haryana-focused news sources:

1. **The Tribune - Haryana**: Regional news coverage
2. **Times of India - Chandigarh**: Major city news
3. **Hindustan Times - Chandigarh**: Local and regional coverage
4. **Indian Express - Chandigarh**: In-depth reporting
5. **News18 - Haryana**: State-wide coverage

These sources were automatically added during setup and can be viewed in the "Sources" page.

## Tips for Best Results

### 1. **Start Broad, Then Narrow**
- Begin with no sentiment filter and low minimum score
- Review what types of articles appear
- Gradually increase the minimum score to focus on most relevant content

### 2. **Combine Multiple Searches**
- Use different categories to get a complete picture
- Example: Check both "Infrastructure" and "Economy" for development news

### 3. **Monitor Trends Over Time**
- Regular checks help you identify patterns
- Notice which types of news are more common
- Track sentiment changes over time

### 4. **Customize Keywords**
- If you're not finding relevant articles, check the keywords
- Add industry-specific terms or local place names
- Remove overly broad keywords that match too many articles

### 5. **Balance Positive and Negative**
- Don't ignore negative sentiment articles
- Understanding challenges helps create balanced content
- Use negative articles to identify areas needing attention

## Troubleshooting

### No Articles Found
- **Check if sources are active**: Go to Sources page
- **Verify database has articles**: Run the scraper to fetch news
- **Lower the minimum score**: Try setting it to 0
- **Check sentiment filter**: Try "All Sentiments"

### Irrelevant Articles Showing
- **Increase minimum score**: Set to 30 or higher
- **Review keywords**: Some keywords might be too broad
- **Check for location mentions**: Article should mention Haryana

### Sentiment Seems Wrong
- Review the positive/negative indicators shown
- The system uses keyword matching, not deep semantic analysis
- Consider adjusting indicator words in configuration

## Next Steps

After mastering the Haryana News Screener:

1. **Set up automated scraping**: Use Celery to fetch news regularly
2. **Integrate with social media**: Add Twitter posting capabilities
3. **Create custom reports**: Export filtered articles for analysis
4. **Build email alerts**: Get notified about high-scoring articles
5. **Add more sources**: Include regional newspapers and blogs

## Technical Details

### Architecture
- **Backend**: FastAPI with SQLAlchemy
- **Frontend**: React with TypeScript and TanStack Query
- **Scoring Engine**: Python-based keyword matching and sentiment detection
- **Database**: SQLite (development) / PostgreSQL (production)

### Performance
- Filters can process 1000+ articles in seconds
- Real-time scoring and sentiment analysis
- Efficient database queries with proper indexing

### Future Enhancements
- Machine learning-based sentiment analysis
- Multi-language support (Hindi, Punjabi)
- Image recognition for visual content
- Automated social media caption generation
- Trend analysis and visualization

## Conclusion

The Haryana News Screener is a powerful tool for discovering and filtering news about Haryana based on your specific interests. Whether you're promoting tourism, tracking infrastructure, monitoring economic growth, or highlighting achievements, this system helps you find the most relevant and impactful news stories.

Start by selecting a category that matches your goals, refine with sentiment and score filters, and discover the news that matters most to you!

