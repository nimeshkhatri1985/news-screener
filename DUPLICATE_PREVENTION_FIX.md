# Duplicate Tweet Prevention Fix

## Problem
Currently, the same article can be posted to Twitter multiple times because there's no check if an article was already posted.

## Solution

### Option 1: Add Database Check (Recommended)

Edit `backend/main.py` in the `/twitter/post` endpoint:

```python
@app.post("/twitter/post")
async def post_to_twitter(request: TweetRequest, db: Session = Depends(get_db)):
    """Post an article to Twitter"""
    if not TWITTER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Twitter service not available")
    
    if not twitter_service.is_configured():
        raise HTTPException(
            status_code=400, 
            detail="Twitter API not configured. Please set environment variables."
        )
    
    # NEW: Check if article was already posted
    existing_post = db.query(Post).filter(
        Post.article_id == request.article_id,
        Post.platform == 'twitter',
        Post.status == 'posted'
    ).first()
    
    if existing_post:
        raise HTTPException(
            status_code=400, 
            detail=f"Article already posted on {existing_post.posted_at.strftime('%Y-%m-%d %H:%M')}. Tweet URL: {existing_post.post_url}"
        )
    
    # ... rest of the code stays the same
```

### Option 2: Add Frontend Warning

Edit `frontend/src/pages/HaryanaNews.tsx`:

```typescript
// Add a query to check if article was already posted
const { data: articlePosts } = useQuery({
  queryKey: ['article-posts', selectedArticle?.id],
  queryFn: () => api.getPostsByArticle(selectedArticle.id),
  enabled: !!selectedArticle
});

// Show warning in tweet modal
{articlePosts && articlePosts.length > 0 && (
  <div className="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded">
    <p className="text-yellow-800 text-sm">
      ⚠️ This article was already posted {articlePosts.length} time(s).
      Last posted: {formatDate(articlePosts[0].posted_at)}
    </p>
  </div>
)}
```

### Option 3: Add Backend API Endpoint

Add a new endpoint to check post history:

```python
@app.get("/posts/by-article/{article_id}")
async def get_posts_by_article(article_id: int, db: Session = Depends(get_db)):
    """Get all posts for a specific article"""
    posts = db.query(Post).filter(
        Post.article_id == article_id,
        Post.status == 'posted'
    ).order_by(Post.posted_at.desc()).all()
    
    return [{
        'id': post.id,
        'platform': post.platform,
        'posted_at': post.posted_at,
        'post_url': post.post_url,
        'status': post.status
    } for post in posts]
```

### Option 4: Add Database Unique Constraint

Prevent duplicates at database level:

```python
# Add to Post model in main.py
from sqlalchemy import UniqueConstraint

class Post(Base):
    __tablename__ = "posts"
    
    # ... existing columns ...
    
    __table_args__ = (
        UniqueConstraint('article_id', 'platform', 'status', name='unique_article_platform_posted'),
    )
```

**Note:** This will prevent posting same article twice, but requires database migration.

## Implementation Steps

### Quick Fix (5 minutes):

1. Add Option 1 (database check) to `backend/main.py`
2. Test by trying to post same article twice
3. Should show error message with previous post details

### Complete Solution (30 minutes):

1. Implement Option 1 (backend check)
2. Implement Option 2 (frontend warning)
3. Add Option 3 (API endpoint)
4. Update database with Option 4 (unique constraint)

## Testing

After implementing:

```bash
# Try posting same article twice
curl -X POST http://localhost:8000/twitter/post \
  -H "Content-Type: application/json" \
  -d '{"article_id": 1, "use_premium": false}'

# Second attempt should fail with:
# {"detail": "Article already posted on 2025-10-27 05:29. Tweet URL: https://..."}
```

## Benefits

✅ Prevents accidental duplicate tweets  
✅ Saves Twitter API quota  
✅ Better user experience  
✅ Maintains professional Twitter presence  
✅ Tracks posting history  

## Recommended Schedule

With duplicate prevention:
- **High Activity**: Scrape every 30-60 minutes
- **Normal Activity**: Scrape every 3-6 hours
- **Low Activity**: Scrape daily

Without worry about posting duplicates!

