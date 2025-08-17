#!/usr/bin/env python3
"""
Test Bot - For immediate testing without time restrictions
"""

import os
from ai_news_poster import AINewsPoster

def test_bot_now():
    """Test bot immediately - ignores all time restrictions"""
    print("🧪 TESTING BOT - NO TIME RESTRICTIONS")
    print("="*50)
    
    # Override environment for testing
    os.environ.setdefault('TARGET_SUBREDDIT', 'AIAutomationLabs')
    os.environ.setdefault('EMAIL_CONTACT', 'jmichaeloficial@gmail.com')
    os.environ.setdefault('INSTAGRAM_CONSULTING', 'https://www.instagram.com/jmichaeloficial/')
    
    poster = AINewsPoster()
    
    print("🔍 Testing connection...")
    if poster.test_connection():
        print("✅ Connection successful!")
        
        print("🚀 Generating content with Infinite Engine...")
        
        # Force infinite content generation
        title, content = poster.infinite_engine.generate_infinite_content()
        
        print(f"📝 Title: {title}")
        print(f"📄 Content preview: {content[:200]}...")
        
        print("📤 Attempting to post...")
        success = poster.post_to_subreddit(title, content)
        
        if success:
            print("🎉 POST SUCCESSFUL!")
            print(f"✅ Posted to r/{poster.target_subreddit}")
            return True
        else:
            print("❌ Post failed")
            return False
    else:
        print("❌ Connection failed - check credentials")
        return False

if __name__ == "__main__":
    test_bot_now()