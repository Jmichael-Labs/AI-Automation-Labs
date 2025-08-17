#!/usr/bin/env python3
"""
Check posts in r/AIAutomationLabs
"""
import praw

import os

reddit = praw.Reddit(
    client_id=os.environ.get('REDDIT_CLIENT_ID'),
    client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
    user_agent=os.environ.get('REDDIT_USER_AGENT'),
    username=os.environ.get('REDDIT_USERNAME'),
    password=os.environ.get('REDDIT_PASSWORD')
)

def check_subreddit_posts():
    """Check what posts exist in target subreddit"""
    target_subreddit = os.environ.get('TARGET_SUBREDDIT', 'AIAutomationLabs')
    try:
        subreddit = reddit.subreddit(target_subreddit)
        print(f"📍 Checking r/{subreddit.display_name}")
        print(f"👥 Subscribers: {subreddit.subscribers}")
        print(f"📝 Description: {subreddit.public_description}")
        
        print("\n📋 POSTS IN SUBREDDIT:")
        post_count = 0
        
        for post in subreddit.new(limit=10):
            post_count += 1
            print(f"\n{post_count}. {post.title}")
            print(f"   Author: u/{post.author}")
            print(f"   Score: {post.score}")
            print(f"   Comments: {post.num_comments}")
            print(f"   URL: {post.url}")
            print(f"   Created: {post.created_utc}")
        
        if post_count == 0:
            print(f"❌ NO POSTS FOUND in r/{target_subreddit}")
        else:
            print(f"\n✅ Found {post_count} posts total")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_subreddit_posts()