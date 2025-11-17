"""
Cleanup script to purge old articles and optionally posts
Run this before re-scraping with new relaxed location requirements
"""
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from main import SessionLocal, Article, Post

def cleanup_articles(delete_all=False, days_to_keep=0, delete_posts=False):
    """
    Clean up articles from database
    
    Args:
        delete_all: If True, delete all articles. If False, delete articles older than days_to_keep
        days_to_keep: Number of days to keep (only used if delete_all=False)
        delete_posts: If True, also delete related posts
    """
    db = SessionLocal()
    
    try:
        # Count before deletion
        total_articles = db.query(Article).count()
        total_posts = db.query(Post).count()
        
        print("=" * 70)
        print("DATABASE CLEANUP")
        print("=" * 70)
        print(f"Current articles: {total_articles}")
        print(f"Current posts: {total_posts}")
        print()
        
        if delete_all:
            print("Mode: DELETE ALL ARTICLES")
            articles_to_delete = db.query(Article).all()
            cutoff_date = None
        else:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
            print(f"Mode: DELETE ARTICLES OLDER THAN {days_to_keep} DAYS")
            print(f"Cutoff date: {cutoff_date}")
            articles_to_delete = db.query(Article).filter(
                Article.published_at < cutoff_date
            ).all()
        
        print(f"Articles to delete: {len(articles_to_delete)}")
        
        if not articles_to_delete:
            print("\n✅ No articles to delete")
            db.close()
            return
        
        # Get article IDs for post deletion
        article_ids = [a.id for a in articles_to_delete]
        
        # Delete posts first (if requested and if they exist)
        if delete_posts and article_ids:
            posts_to_delete = db.query(Post).filter(
                Post.article_id.in_(article_ids)
            ).all()
            if posts_to_delete:
                print(f"\nDeleting {len(posts_to_delete)} related posts...")
                for post in posts_to_delete:
                    db.delete(post)
                db.commit()
                print("✅ Posts deleted")
        
        # Delete articles
        print(f"\nDeleting {len(articles_to_delete)} articles...")
        for article in articles_to_delete:
            db.delete(article)
        db.commit()
        
        # Count after deletion
        remaining_articles = db.query(Article).count()
        remaining_posts = db.query(Post).count()
        
        print("✅ Articles deleted")
        print()
        print("=" * 70)
        print("CLEANUP COMPLETE")
        print("=" * 70)
        print(f"Articles deleted: {len(articles_to_delete)}")
        print(f"Articles remaining: {remaining_articles}")
        print(f"Posts remaining: {remaining_posts}")
        print()
        print("✅ Ready for fresh scraping with new location requirements!")
        
    except Exception as e:
        print(f"\n❌ Error during cleanup: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Clean up old articles from database')
    parser.add_argument('--all', action='store_true', help='Delete all articles')
    parser.add_argument('--days', type=int, default=0, help='Keep articles newer than N days (default: 0 = delete all)')
    parser.add_argument('--posts', action='store_true', help='Also delete related posts')
    
    args = parser.parse_args()
    
    if args.all:
        print("\n⚠️  WARNING: This will delete ALL articles!")
        response = input("Are you sure? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            sys.exit(0)
        cleanup_articles(delete_all=True, delete_posts=args.posts)
    else:
        days = args.days if args.days > 0 else 0
        if days == 0:
            print("\n⚠️  WARNING: This will delete ALL articles!")
            response = input("Are you sure? (yes/no): ")
            if response.lower() != 'yes':
                print("Cancelled.")
                sys.exit(0)
        cleanup_articles(delete_all=(days == 0), days_to_keep=days, delete_posts=args.posts)

