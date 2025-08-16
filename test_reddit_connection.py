#!/usr/bin/env python3
"""
Test Reddit Connection
Quick test to verify Reddit API works
"""

import praw
from reddit_credentials import *

def test_reddit_connection():
    """Test basic Reddit connection"""
    try:
        # Initialize Reddit
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
            username=REDDIT_USERNAME,
            password=REDDIT_PASSWORD
        )
        
        # Test connection
        user = reddit.user.me()
        print(f"✅ Connected as: u/{user.name}")
        print(f"📊 Comment Karma: {user.comment_karma}")
        print(f"📊 Link Karma: {user.link_karma}")
        
        # Test reading a subreddit
        ai_subreddit = reddit.subreddit("artificial")
        print(f"📍 Testing r/artificial access...")
        
        post_count = 0
        for post in ai_subreddit.new(limit=3):
            post_count += 1
            print(f"📝 Post {post_count}: {post.title[:50]}...")
        
        print(f"✅ Successfully read {post_count} posts from r/artificial")
        
        # Test AI problem detection
        print("\n🧠 Testing AI problem detection...")
        test_titles = [
            "How do I use ChatGPT for my business?",
            "Need help with machine learning project",
            "AI tools recommendation please",
            "What's the weather today?",  # Should NOT match
            "Help with prompt engineering"
        ]
        
        for title in test_titles:
            # Simple detection logic
            ai_keywords = ["chatgpt", "ai", "machine learning", "prompt"]
            help_keywords = ["help", "how do i", "recommendation", "need"]
            
            has_ai = any(keyword in title.lower() for keyword in ai_keywords)
            has_help = any(keyword in title.lower() for keyword in help_keywords)
            
            if has_ai and has_help:
                print(f"✅ MATCH: '{title}'")
            else:
                print(f"❌ SKIP: '{title}'")
        
        print("\n🚀 Reddit connection test successful!")
        print("\n📋 Next Steps:")
        print("1. Run: python3 reddit_ai_solver.py")
        print("2. Choose 'n' for test mode first")
        print("3. Review results before going continuous")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("- Check your Reddit credentials")
        print("- Verify Reddit app permissions")
        print("- Ensure account is verified")
        return False

if __name__ == "__main__":
    test_reddit_connection()