#!/usr/bin/env python3
"""
Test Reddit connection with specific credentials
"""
import praw

# Set credentials directly for testing
reddit = praw.Reddit(
    client_id="2db6KZffvByzTGZCEntIqw",
    client_secret="5f1GO6oTWWJUf153NnhlfL1khE4osQ", 
    user_agent="AIAutomationLabsBot:v1.0 (by /u/theinnovationla)",
    username="theinnovationla",
    password="Suxtan20@"
)

try:
    print("🧪 Testing Reddit connection...")
    user = reddit.user.me()
    print(f"✅ SUCCESS: Connected as u/{user.name}")
    print(f"📊 Comment Karma: {user.comment_karma}")
    print(f"📊 Link Karma: {user.link_karma}")
    
    # Test subreddit access
    subreddit = reddit.subreddit("AIAutomationLabsBot")
    print(f"✅ Subreddit access: r/{subreddit.display_name}")
    print(f"👥 Subscribers: {subreddit.subscribers}")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    print("🔍 Possible issues:")
    print("- Wrong username/password")
    print("- Account suspended") 
    print("- App configured wrong")
    print("- Rate limiting")
