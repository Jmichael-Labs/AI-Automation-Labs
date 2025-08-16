#!/usr/bin/env python3
"""
Quick test of Reddit AI bot without AGI calls
"""

import praw
from reddit_credentials import *

def quick_test():
    """Quick test without calling AGI nuclei"""
    
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD
    )
    
    print(f"🤖 Connected as: u/{reddit.user.me().name}")
    
    # Quick scan for AI problems
    ai_problems_found = 0
    total_posts_scanned = 0
    
    for subreddit_name in ["ChatGPT", "artificial", "MachineLearning"]:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            print(f"📍 Scanning r/{subreddit_name}...")
            
            for post in subreddit.new(limit=5):
                total_posts_scanned += 1
                title_lower = post.title.lower()
                
                # Simple AI problem detection
                ai_keywords = ["help", "how", "problem", "question", "need"]
                if any(keyword in title_lower for keyword in ai_keywords):
                    ai_problems_found += 1
                    print(f"  🎯 OPPORTUNITY: {post.title[:60]}...")
                    
        except Exception as e:
            print(f"  ❌ Error with r/{subreddit_name}: {e}")
    
    print(f"\n📊 SCAN RESULTS:")
    print(f"   Posts scanned: {total_posts_scanned}")
    print(f"   AI problems found: {ai_problems_found}")
    print(f"   Success rate: {(ai_problems_found/total_posts_scanned)*100:.1f}%")
    
    if ai_problems_found > 0:
        print(f"\n✅ BOT READY! Found {ai_problems_found} opportunities to help people with AI")
        print(f"💰 Each response includes your contact: {EMAIL_CONTACT}")
        print(f"📱 Instagram consulting: {INSTAGRAM_CONSULTING}")
    else:
        print(f"\n⏳ No immediate opportunities, but bot is ready to find them!")

if __name__ == "__main__":
    quick_test()