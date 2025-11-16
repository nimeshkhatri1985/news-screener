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
        "description": "Positive news about tourism development, heritage sites, cultural events",
        "keywords": [
            "tourism", "tourist", "heritage", "monument", "temple", "fort",
            "cultural", "festival", "museum", "archaeological",
            # Removed location names - they should only be used for Haryana relevance, not category matching
            # "surajkund", "kurukshetra", "panchkula", "morni hills", "sultanpur",
            "bird sanctuary", "kingdom of dreams", "damdama lake", "vintage car museum", "craft mela",
            "adventure", "hotel", "resort", "pilgrim", "pilgrimage", "visitor",
            "destination", "attraction", "site", "tour", "travel", "experience"
        ],
        "positive_indicators": [
            "inaugurate", "inaugurated", "launch", "launched", "unveil", "unveiled",
            "new", "develop", "developed", "development", "promote", "promoted",
            "boost", "boosted", "attract", "attracted", "improve", "improved",
            "enhance", "enhanced", "popular", "growing", "increase", "increased",
            "record", "milestone", "award", "recognition", "world-class", "state-of-the-art",
            "restore", "restored", "renovation", "renovated", "beautify", "beautified",
            "expand", "expanded", "upgrade", "upgraded", "modern", "modernize",
            "success", "successful", "thriving", "flourishing", "vibrant", "celebrate"
        ],
        "negative_indicators": [
            "close", "closed", "shutdown", "decline", "declined", "decrease", "decreased",
            "protest", "damage", "damaged", "vandal", "theft", "stolen", "neglect",
            "deteriorate", "deteriorating", "poor", "bad", "worst", "fail", "failed",
            "cancel", "cancelled", "delay", "delayed", "problem", "issue", "concern"
        ]
    },
    "infrastructure": {
        "name": "Infrastructure Development",
        "description": "Positive news about infrastructure projects, development works, modernization",
        "keywords": [
            "infrastructure", "development", "project", "construction", "road",
            "highway", "metro", "railway", "airport", "bridge", "flyover",
            "expressway", "smart city", "urban", "rural", "water supply",
            "electricity", "power", "sewage", "drainage", "public transport",
            "bus", "connectivity", "network", "modernization", "upgrade",
            "corridor", "terminal", "station",
            # Removed generic "facility" - use specific terms instead
            "infrastructure facility", "transport facility", "public facility",
            "complex"
        ],
        "positive_indicators": [
            "complete", "completed", "inaugurate", "inaugurated", "launch", "launched",
            "approve", "approved", "sanction", "sanctioned", "fund", "funded",
            "allocate", "allocated", "start", "started", "begin", "began",
            "improve", "improved", "enhance", "enhanced", "upgrade", "upgraded",
            "modernize", "modernized", "expand", "expanded", "extend", "extended",
            "new", "state-of-the-art", "world-class", "cutting-edge", "advanced",
            "milestone", "record", "fast-track", "accelerate", "accelerated",
            "transform", "transformed", "revolutionize", "revolutionized",
            "boost", "boosted", "strengthen", "strengthened", "efficient"
        ],
        "negative_indicators": [
            "delay", "delayed", "stall", "stalled", "halt", "halted",
            "cancel", "cancelled", "poor", "deteriorate", "deteriorating",
            "damage", "damaged", "collapse", "collapsed", "accident", "crash",
            "protest", "oppose", "opposition", "problem", "issue", "concern",
            "fail", "failed", "failure", "inadequate", "insufficient"
        ]
    },
    "economy": {
        "name": "Economic Development",
        "description": "Positive news about business growth, industry expansion, investment, job creation",
        "keywords": [
            "economy", "economic", "business", "industry", "investment", "startup",
            "manufacturing", "factory", "plant", "company", "enterprise", "trade",
            "export", "import", "GDP", "growth", "jobs", "employment", "industrial",
            "technology park", "IT", "software", "innovation", "entrepreneur",
            "IMT", "HSIIDC", "sector", "zone", "hub", "incubator", "unicorn",
            "funding", "venture", "capital", "market", "revenue", "profit"
        ],
        "positive_indicators": [
            "growth", "growing", "grow", "increase", "increased", "boost", "boosted",
            "expand", "expanded", "expansion", "launch", "launched", "invest", "invested",
            "create", "created", "generate", "generated", "attract", "attracted",
            "improve", "improved", "rise", "rising", "raises", "raised", "raise",
            "surge", "surged", "soar", "soared",
            "record", "record-breaking", "milestone", "achievement", "achieve", "achieved",
            "success", "successful", "profitable", "profit", "revenue", "thriving",
            "flourishing", "prosperous", "prosperity", "boom", "booming", "robust",
            "strong", "strengthen", "strengthened", "scale", "scaling", "multiply",
            "double", "triple", "breakthrough", "pioneer", "pioneering", "innovative",
            "world-class", "leading", "leader", "first", "best", "top", "premier"
        ],
        "negative_indicators": [
            "decline", "declined", "decrease", "decreased", "loss", "lose", "lost",
            "shutdown", "shut down", "close", "closed", "layoff", "lay off", "retrench",
            "crisis", "recession", "slowdown", "slump", "fall", "fell", "drop", "dropped",
            "fail", "failed", "failure", "bankruptcy", "bankrupt", "debt", "struggle",
            "struggling", "poor", "worst", "bad", "negative", "problem", "concern"
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
            "training", "coach", "player", "sports facility", "sports academy",
            "sports complex", "sports infrastructure", "sports center", "sports centre"
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

# Cities, districts, and regions in Haryana for location-based filtering
# English-only list (state, all districts, major towns, regions, and key landmarks)
HARYANA_LOCATIONS = [
    # State name
    "Haryana",

    # All 22 Districts (English)
    "Ambala",
    "Bhiwani",
    "Charkhi Dadri",
    "Faridabad",
    "Fatehabad",
    "Gurugram", "Gurgaon",
    "Hisar",
    "Jhajjar",
    "Jind",
    "Kaithal",
    "Karnal",
    "Kurukshetra",
    "Mahendragarh",
    "Nuh",
    "Palwal",
    "Panchkula",
    "Panipat",
    "Rewari",
    "Rohtak",
    "Sirsa",
    "Sonipat",
    "Yamunanagar",

    # Major Cities and Towns (English)
    "Chandigarh",
    "Manesar",
    "Sohna",
    "Bahadurgarh",
    "Bawal",
    "Dharuhera",
    "Hansi",
    "Narnaul",
    "Tohana",
    "Narwana",
    "Ellenabad",
    "Barwala",
    "Ratia",
    "Ladwa",
    "Shahbad",
    "Pehowa",
    "Pundri",
    "Nilokheri",
    "Indri",
    "Gharaunda",
    "Assandh",
    "Samalkha",
    "Gohana",
    "Ganaur",
    "Kharkhoda",
    "Rai",
    "Murthal",
    "Kundli",
    "Badshahpur",

    # Regions and Areas
    "Mewat",
    "Ahirwal",
    "Bagri",
    "Haryanvi",

    # Important Landmarks/Areas (that indicate Haryana)
    "Surajkund",
    "Damdama Lake",
    "Sultanpur",
    "Pinjore",
    "Kalesar",
    "Morni Hills",
    "Brahma Sarovar"
]

# Sentiment scoring weights
# HEAVILY penalize negative content to show ONLY positive progress news
SENTIMENT_WEIGHTS = {
    "positive_indicator": 3.0,      # Increased from 2.0
    "negative_indicator": -10.0,    # Increased penalty from -2.0 to -10.0
    "positive_context": 1.5,        # Increased from 1.0
    "negative_context": -5.0,       # Increased penalty from -1.0
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
    
    # CRITICAL FIX: Filter out violent/crime articles immediately - BEFORE any category matching
    # These should NEVER appear in ANY category, regardless of keywords
    violent_keywords = [
        "kill", "kills", "killed", "killing", "murder", "murdered", "murderer",
        "assault", "violence", "violent", "attack", "attacked", "arrest", "arrested",
        "crime", "criminal", "throat", "slitting", "stab", "stabbing", "shoot",
        "shooting", "dead", "death", "died", "dies", "suicide", "rape", "raped",
        "robbery", "theft", "burglary", "abuse", "abused", "victim", "victims",
        "homicide", "manslaughter", "assassination", "terrorism", "terrorist",
        "bomb", "explosion", "explosive", "weapon", "weapons", "gun", "guns"
    ]
    
    article_lower = article_text.lower()
    title = article_text.split('.')[0].split('\n')[0].lower()  # First sentence or first line
    
    # Check for violent keywords in title (most reliable indicator)
    for violent_kw in violent_keywords:
        if violent_kw in title:
            return {
                "score": -10000,  # Massive penalty to ensure it's completely filtered out
                "matched_keywords": [],
                "positive_matches": [],
                "negative_matches": [violent_kw],
                "sentiment": "negative"
            }
    
    # Also check first 300 chars of content for violent keywords (to catch violent news)
    content_start = article_lower[:300]
    violent_matches_in_content = [kw for kw in violent_keywords if kw in content_start]
    if len(violent_matches_in_content) >= 2:  # Multiple violent keywords = likely violent news
        return {
            "score": -10000,
            "matched_keywords": [],
            "positive_matches": [],
            "negative_matches": violent_matches_in_content[:3],  # Return first 3 matches
            "sentiment": "negative"
        }
    
    preset = HARYANA_FILTER_PRESETS[filter_preset_key]
    
    # Check for keywords
    matched_keywords = []
    for keyword in preset["keywords"]:
        if keyword.lower() in article_lower:
            matched_keywords.append(keyword)
    
    # CRITICAL FIX: Require at least one keyword match before applying positive indicators
    # This prevents generic positive words from scoring articles in wrong categories
    if len(matched_keywords) == 0:
        # No keywords matched - article is not relevant to this category
        # Only apply negative penalties (to filter out clearly negative content)
        negative_matches = []
        for indicator in preset["negative_indicators"]:
            if indicator.lower() in article_lower:
                negative_matches.append(indicator)
        
        if len(negative_matches) > 0:
            return {
                "score": -100,
                "matched_keywords": [],
                "positive_matches": [],
                "negative_matches": negative_matches,
                "sentiment": "negative"
            }
        else:
            # No keywords, no negative indicators - not relevant to this category
            return {
                "score": 0,
                "matched_keywords": [],
                "positive_matches": [],
                "negative_matches": [],
                "sentiment": "neutral"
            }
    
    # Base score from keyword matches (only reached if keywords matched)
    keyword_score = len(matched_keywords) * 10
    
    # Check for positive indicators (only if keywords matched)
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
    # STRICT POSITIVE FILTERING: Require positive sentiment or heavily penalize
    if sentiment_score > 2:  # Raised threshold from 1 to 2
        sentiment = "positive"
    elif sentiment_score < -1:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    # Total score calculation (only reached if keywords matched)
    # HEAVILY penalize negative and neutral content
    if sentiment == "negative":
        # Negative articles get massive penalty - essentially filtered out
        total_score = keyword_score + (sentiment_score * 10) - 100
    elif sentiment == "neutral":
        # Neutral articles get moderate penalty to prioritize positive news
        total_score = keyword_score + (sentiment_score * 5) - 20
    else:  # positive
        # Positive articles get bonus (only if keywords matched)
        total_score = keyword_score + (sentiment_score * 8) + 20
    
    # Additional filter: If article has ANY negative indicators, heavily penalize
    if len(negative_matches) > 0:
        total_score -= (len(negative_matches) * 30)
    
    # Bonus for multiple positive indicators (only if keywords matched)
    if len(positive_matches) >= 3:
        total_score += 25
    
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


def is_article_positive(article_text):
    """Check if article has positive sentiment (filters out negative and neutral news)"""
    article_lower = article_text.lower()
    negative_keywords = ['murder', 'killed', 'dead', 'death', 'suicide', 'rape', 'attack', 'assault', 'robbery', 'theft', 'scam', 'fraud', 'corrupt', 'corruption', 'arrest', 'jail', 'prison', 'gang', 'crime', 'violence', 'abuse', 'accident', 'fire', 'explosion', 'protest', 'strike', 'chaos', 'crisis', 'collapse', 'disaster', 'flood', 'drought', 'unemployment', 'loss', 'bankruptcy', 'debate', 'controversy', 'row', 'allegation', 'charges', 'lawsuit', 'cancelled', 'shut down', 'closed', 'failed', 'decline', 'decrease']
    neutral_keywords = ['court', 'hc ', 'hc.', 'high court', 'judge', 'verdict', 'ruling', 'petition', 'plea', 'hearing', 'case', 'lawsuit', 'stay order', 'quash', 'quashed', 'sets aside', 'reinstates', 'approves', 'rejects', 'orders', 'directs', 'asks']
    positive_keywords = ['announces', 'announced', 'inaugurates', 'develops', 'developing', 'growth', 'rises', 'increases', 'boosts', 'success', 'achievement', 'victory', 'wins', 'celebrates', 'new initiative', 'investment', 'partnership', 'expansion', 'improves', 'improving', 'renewable', 'green', 'innovation', 'record', 'milestone', 'pioneering', 'leading', 'excellence', 'upgrades', 'modernizes', 'facilities', 'infrastructure', 'project']
    title = article_text.split('.')[0].split('\n')[0].lower()
    title_negative_count = sum(1 for keyword in negative_keywords if keyword in title)
    full_text_negative_count = sum(1 for keyword in negative_keywords if keyword in article_lower)
    title_neutral_count = sum(1 for keyword in neutral_keywords if keyword in title)
    title_positive_count = sum(1 for keyword in positive_keywords if keyword in title)
    full_text_positive_count = sum(1 for keyword in positive_keywords if keyword in article_lower)
    if title_negative_count >= 1 or full_text_negative_count >= 3:
        return False
    if title_positive_count >= 1 or full_text_positive_count >= 2:
        return True
    if title_neutral_count >= 1 and title_positive_count == 0:
        return False
    return False
