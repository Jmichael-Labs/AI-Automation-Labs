#!/usr/bin/env python3
"""
Check posts in r/AIAutomationLabs
"""
import praw

reddit = praw.Reddit(
    client_id='WWPlll5usdslxz9bQqEvZg',
    client_secret='c7gBvHnTuQO1v3eiHLt8IotVuSVhyQ',
    user_agent='AIAutomationLabsBot:v1.0 (by /u/theinnovationla)',
    username='theinnovationla',
    password='Suxtan20@'
)

def check_subreddit_posts():
    """Check what posts exist in r/AIAutomationLabs"""
    try:
        subreddit = reddit.subreddit('AIAutomationLabs')
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
            print("❌ NO POSTS FOUND in r/AIAutomationLabs")
        else:
            print(f"\n✅ Found {post_count} posts total")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_subreddit_posts()