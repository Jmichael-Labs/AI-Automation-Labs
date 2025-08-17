#!/usr/bin/env python3
"""
Debug Reddit connection step by step
"""
import praw

def test_reddit_auth():
    """Test each step of Reddit authentication"""
    
    print("🔍 Testing Reddit connection...")
    
    # AIAutomationLabs official credentials
    client_id = 'sVYH1t6xaF8j5MkfcTVxww'
    client_secret = '7kbuoA9Ct_X_LN5DyFJwcL3gKHVu3A'
    username = 'AIAutomationLabs'
    password = 'Suxtan20@'
    
    print(f"📱 Client ID: {client_id}")
    print(f"🔐 Username: {username}")
    
    try:
        # Test connection
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent='AIAutomationLabsBot:v2.0 (by /u/AIAutomationLabs)',
            username=username,
            password=password
        )
        
        print("🟡 Attempting connection...")
        
        # Test user authentication
        user = reddit.user.me()
        print(f"✅ SUCCESS! Connected as: u/{user.name}")
        print(f"📊 Comment Karma: {user.comment_karma}")
        print(f"📊 Link Karma: {user.link_karma}")
        
        # Test subreddit access
        print("🔍 Testing subreddit access...")
        subreddit = reddit.subreddit('AIAutomationLabs')
        print(f"✅ Subreddit access OK: r/{subreddit.display_name}")
        print(f"👥 Subscribers: {subreddit.subscribers}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"🔍 Error type: {type(e).__name__}")
        
        # Try to diagnose the specific issue
        if "invalid_grant" in str(e):
            print("🚨 DIAGNOSIS: Username/password issue")
            print("💡 SOLUTION: Verify Reddit login credentials")
            print("   - Try logging into reddit.com manually with these credentials")
            print("   - Check if account has 2FA enabled (disable for bot)")
            print("   - Make sure password is correct")
        
        return False

if __name__ == "__main__":
    test_reddit_auth()