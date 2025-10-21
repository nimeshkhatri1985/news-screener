"""
Haryana News Configuration
Specialized configuration for tracking Haryana-related news with topic-based filtering
"""

# Haryana-specific news sources (RSS feeds)
HARYANA_NEWS_SOURCES = [
    {
        "name": "The Tribune - Haryana",
        "url": "https://www.tribuneindia.com",
        "rss_feed": "https://www.tribuneindia.com/rss/haryana",
        "is_active": True
    },
    {
        "name": "Times of India - Chandigarh",
        "url": "https://timesofindia.indiatimes.com",
        "rss_feed": "https://timesofindia.indiatimes.com/rssfeeds/4118235.cms",
        "is_active": True
    },
    {
        "name": "Hindustan Times - Chandigarh",
        "url": "https://www.hindustantimes.com",
        "rss_feed": "https://www.hindustantimes.com/feeds/rss/chandigarh/rssfeed.xml",
        "is_active": True
    },
    {
        "name": "Indian Express - Chandigarh",
        "url": "https://indianexpress.com",
        "rss_feed": "https://indianexpress.com/section/cities/chandigarh/feed/",
        "is_active": True
    },
    {
        "name": "News18 - Haryana",
        "url": "https://www.news18.com",
        "rss_feed": "https://www.news18.com/rss/india.xml",
        "is_active": True
    }
]

# Topic-based filter configurations
HARYANA_FILTER_PRESETS = {
    "tourism": {
        "name": "Tourism & Heritage",
        "description": "News about tourism development, heritage sites, cultural events",
        "keywords": [
            "tourism", "tourist", "heritage", "monument", "temple", "fort",
            "cultural", "festival", "museum", "archaeological", "surajkund",
            "kurukshetra", "panchkula", "morni hills", "sultanpur", "bird sanctuary",
            "kingdom of dreams", "damdama lake", "vintage car museum", "craft mela",
            "adventure", "hotel", "resort", "pilgrim", "pilgrimage", "visitor"
        ],
        "positive_indicators": [
            "inaugurate", "launch", "new", "development", "promote", "boost",
            "attract", "improve", "enhance", "popular", "growing", "increase"
        ],
        "negative_indicators": [
            "close", "shutdown", "decline", "decrease", "protest", "damage"
        ]
    },
    "infrastructure": {
        "name": "Infrastructure Development",
        "description": "News about infrastructure projects, development works",
        "keywords": [
            "infrastructure", "development", "project", "construction", "road",
            "highway", "metro", "railway", "airport", "bridge", "flyover",
            "expressway", "smart city", "urban", "rural", "water supply",
            "electricity", "power", "sewage", "drainage", "public transport",
            "bus", "connectivity", "network", "modernization", "upgrade"
        ],
        "positive_indicators": [
            "complete", "inaugurate", "launch", "approve", "sanction", "fund",
            "allocate", "start", "begin", "improve", "enhance", "upgrade",
            "modernize", "expand", "extend", "new", "state-of-the-art"
        ],
        "negative_indicators": [
            "delay", "stall", "halt", "cancel", "poor", "deteriorate", "damage"
        ]
    },
    "economy": {
        "name": "Economic Development",
        "description": "Business, industry, investment, and economic growth news",
        "keywords": [
            "economy", "economic", "business", "industry", "investment", "startup",
            "manufacturing", "factory", "plant", "company", "enterprise", "trade",
            "export", "import", "GDP", "growth", "jobs", "employment", "industrial",
            "technology park", "IT", "software", "innovation", "entrepreneur",
            "IMT", "HSIIDC", "sector", "zone", "hub", "incubator"
        ],
        "positive_indicators": [
            "growth", "increase", "boost", "expand", "launch", "invest",
            "create", "generate", "attract", "improve", "rise", "surge",
            "record", "milestone", "achievement", "success", "profitable"
        ],
        "negative_indicators": [
            "decline", "decrease", "loss", "shutdown", "layoff", "crisis"
        ]
    },
    "education": {
        "name": "Education & Skill Development",
        "description": "News about education, schools, universities, skill development",
        "keywords": [
            "education", "school", "college", "university", "institute", "IIT",
            "NIT", "medical college", "engineering", "skill", "training",
            "student", "teacher", "professor", "research", "scholarship",
            "admission", "exam", "results", "campus", "academy", "learning",
            "vocational", "ITI", "polytechnic", "library", "laboratory"
        ],
        "positive_indicators": [
            "inaugurate", "establish", "launch", "rank", "award", "excellence",
            "improve", "enhance", "upgrade", "new", "modern", "digital",
            "achieve", "success", "recognition", "accreditation"
        ],
        "negative_indicators": [
            "close", "shutdown", "protest", "strike", "decline", "poor"
        ]
    },
    "agriculture": {
        "name": "Agriculture & Rural Development",
        "description": "Farming, agriculture technology, rural development news",
        "keywords": [
            "agriculture", "farming", "farmer", "crop", "wheat", "rice", "millet",
            "harvest", "irrigation", "rural", "village", "panchayat", "kisan",
            "agrarian", "agricultural", "horticulture", "dairy", "livestock",
            "organic", "seed", "fertilizer", "tractor", "technology", "subsidy",
            "MSP", "market", "mandi", "produce", "yield"
        ],
        "positive_indicators": [
            "increase", "improve", "boost", "support", "subsidy", "scheme",
            "benefit", "grow", "enhance", "modern", "technology", "innovation",
            "record", "bumper", "profitable", "success"
        ],
        "negative_indicators": [
            "decline", "loss", "damage", "protest", "crisis", "drought"
        ]
    },
    "sports": {
        "name": "Sports & Recreation",
        "description": "Sports facilities, achievements, events",
        "keywords": [
            "sport", "sports", "athlete", "medal", "olympic", "championship",
            "stadium", "tournament", "cricket", "hockey", "wrestling", "boxing",
            "kabaddi", "football", "badminton", "shooting", "fitness", "gym",
            "training", "coach", "player", "facility", "academy", "infrastructure"
        ],
        "positive_indicators": [
            "win", "medal", "gold", "silver", "bronze", "victory", "champion",
            "inaugurate", "launch", "new", "modern", "world-class", "achieve",
            "record", "milestone", "excellence", "recognition"
        ],
        "negative_indicators": [
            "lose", "defeat", "controversy", "scandal", "close", "poor"
        ]
    },
    "environment": {
        "name": "Environment & Sustainability",
        "description": "Environmental initiatives, green projects, sustainability",
        "keywords": [
            "environment", "green", "clean", "pollution", "air quality", "water",
            "tree", "forest", "plantation", "conservation", "wildlife", "solar",
            "renewable", "energy", "sustainable", "ecology", "biodiversity",
            "climate", "carbon", "emission", "recycling", "waste management",
            "park", "garden", "green belt", "eco-friendly"
        ],
        "positive_indicators": [
            "improve", "clean", "reduce", "plant", "protect", "conserve",
            "launch", "initiative", "green", "sustainable", "renewable",
            "award", "recognition", "achieve", "better", "enhance"
        ],
        "negative_indicators": [
            "pollute", "worsen", "deteriorate", "damage", "destroy", "illegal"
        ]
    },
    "governance": {
        "name": "Governance & Public Services",
        "description": "Government initiatives, public services, policy announcements",
        "keywords": [
            "government", "governance", "policy", "scheme", "initiative", "program",
            "service", "administration", "public", "welfare", "benefit", "portal",
            "digital", "e-governance", "online", "minister", "CM", "announcement",
            "launch", "reform", "transparency", "accountability", "citizen"
        ],
        "positive_indicators": [
            "launch", "introduce", "improve", "enhance", "benefit", "welfare",
            "efficient", "transparent", "digital", "online", "easy", "quick",
            "accessible", "innovative", "modern", "award", "recognition"
        ],
        "negative_indicators": [
            "corrupt", "scandal", "controversy", "delay", "inefficient", "poor"
        ]
    }
}

# Cities and regions in Haryana for location-based filtering
HARYANA_LOCATIONS = [
    "Haryana", "Chandigarh", "Gurugram", "Gurgaon", "Faridabad", "Panchkula",
    "Ambala", "Karnal", "Panipat", "Rohtak", "Hisar", "Sonipat", "Yamunanagar",
    "Kurukshetra", "Sirsa", "Bhiwani", "Jind", "Kaithal", "Rewari", "Mahendragarh",
    "Palwal", "Jhajjar", "Fatehabad", "Nuh", "Mewat"
]

# Sentiment scoring weights
SENTIMENT_WEIGHTS = {
    "positive_indicator": 2.0,
    "negative_indicator": -2.0,
    "positive_context": 1.0,
    "negative_context": -1.0,
    "neutral": 0.0
}

def calculate_relevance_score(article_text, filter_preset_key):
    """
    Calculate relevance score for an article based on filter preset
    
    Args:
        article_text: Combined title and content of article
        filter_preset_key: Key from HARYANA_FILTER_PRESETS
    
    Returns:
        dict with score, matched_keywords, and sentiment
    """
    if filter_preset_key not in HARYANA_FILTER_PRESETS:
        return {"score": 0, "matched_keywords": [], "sentiment": "neutral"}
    
    preset = HARYANA_FILTER_PRESETS[filter_preset_key]
    article_lower = article_text.lower()
    
    # Check for keywords
    matched_keywords = []
    for keyword in preset["keywords"]:
        if keyword.lower() in article_lower:
            matched_keywords.append(keyword)
    
    # Base score from keyword matches
    keyword_score = len(matched_keywords) * 10
    
    # Check for positive indicators
    positive_matches = []
    for indicator in preset["positive_indicators"]:
        if indicator.lower() in article_lower:
            positive_matches.append(indicator)
    
    # Check for negative indicators
    negative_matches = []
    for indicator in preset["negative_indicators"]:
        if indicator.lower() in article_lower:
            negative_matches.append(indicator)
    
    # Calculate sentiment score
    sentiment_score = (
        len(positive_matches) * SENTIMENT_WEIGHTS["positive_indicator"] +
        len(negative_matches) * SENTIMENT_WEIGHTS["negative_indicator"]
    )
    
    # Determine overall sentiment
    if sentiment_score > 1:
        sentiment = "positive"
    elif sentiment_score < -1:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    # Total score
    total_score = keyword_score + (sentiment_score * 5)
    
    return {
        "score": total_score,
        "matched_keywords": matched_keywords,
        "positive_matches": positive_matches,
        "negative_matches": negative_matches,
        "sentiment": sentiment
    }

def is_haryana_relevant(article_text):
    """
    Check if article is relevant to Haryana
    """
    article_lower = article_text.lower()
    for location in HARYANA_LOCATIONS:
        if location.lower() in article_lower:
            return True
    return False

