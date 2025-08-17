#!/usr/bin/env python3
"""
Force test post - bypasses duplicate prevention
"""

from ai_news_poster import AINewsPoster

# Create bot instance
bot = AINewsPoster()

print("🧪 FORCING TEST POST (bypassing duplicate prevention)")
print("=" * 60)

# Test connection first
if not bot.test_connection():
    print("❌ Connection failed!")
    exit(1)

# Force reset daily tracking
bot.last_post_date = None  # Reset to force new post
bot.posts_today = 0

# Generate content
title, content = bot.generate_daily_ai_news()

print(f"📝 TITLE: {title}")
print(f"📊 Content length: {len(content)} characters")
print("=" * 60)

print("\n🚨 About to post to r/AIAutomationLabs:")
print(f"Title: {title[:50]}...")

print("\n🚀 Posting to Reddit...")
success = bot.post_to_subreddit(title, content)

if success:
    print("✅ POST SUCCESSFUL!")
    print("🔗 Check: https://reddit.com/r/AIAutomationLabs/new")
else:
    print("❌ POST FAILED!")