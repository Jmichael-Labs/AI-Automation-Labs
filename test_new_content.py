#!/usr/bin/env python3
"""
Test new content format without posting
"""

from ai_news_poster import AINewsPoster

# Create bot instance
bot = AINewsPoster()

# Test new passive income content
print("🧪 TESTING NEW AI PASSIVE INCOME FORMAT:")
print("=" * 60)

title, content = bot.generate_daily_ai_news()

print(f"TITLE: {title}")
print("=" * 60)
print(f"CONTENT:\n{content}")
print("=" * 60)

print(f"\n📊 CONTENT STATS:")
print(f"Title length: {len(title)} characters")
print(f"Content length: {len(content)} characters")
print(f"Content lines: {len(content.split(chr(10)))} lines")

# Check if content is English-only and focused
if "ES:" in content or "EN:" in content:
    print("❌ WARNING: Bilingual content detected")
else:
    print("✅ English-only content confirmed")

if "$" in title and ("passive" in content.lower() or "income" in content.lower()):
    print("✅ Passive income focus confirmed")
else:
    print("❌ WARNING: Not clearly focused on passive income")

if len(content) < 1500:
    print("✅ Concise format confirmed")
else:
    print("❌ WARNING: Content might be too long")