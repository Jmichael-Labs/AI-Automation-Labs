#!/usr/bin/env python3
"""
Quick test to post immediately to Reddit
"""
import praw
import os
from datetime import datetime

# Set your credentials directly here for immediate testing
import os

reddit = praw.Reddit(
    client_id=os.environ.get('REDDIT_CLIENT_ID'),
    client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
    user_agent=os.environ.get('REDDIT_USER_AGENT', 'AIAutomationLabsBot:v1.0 (by /u/AIAutomationLabs)'),
    username=os.environ.get('REDDIT_USERNAME'),
    password=os.environ.get('REDDIT_PASSWORD')
)

def post_immediately():
    """Post to r/AIAutomationLabs right now"""
    try:
        # Test connection first
        user = reddit.user.me()
        print(f"✅ Connected as: u/{user.name}")
        
        # Generate today's content
        today = datetime.now().strftime('%B %d, %Y')
        title = f"🚀 Welcome to JMichael Labs - AI Automation Hub | {today}"
        
        content = f"""## Welcome to the Future of AI Automation! 🤖

Hey Reddit! I'm excited to launch **JMichael Labs** - your new go-to community for practical AI automation insights.

### 🎯 **What You'll Find Here:**

**Daily AI Updates** 📅
- Latest tools and breakthroughs that actually matter
- Real-world implementation stories (no fluff)
- Cost-effective solutions for businesses of all sizes

**Tool Spotlights** 🔧
- Deep dives into automation platforms like Vercept
- Honest reviews of what works (and what doesn't)
- Free alternatives to expensive enterprise solutions

**Case Studies** 📊
- How I automated my entire e-commerce workflow with $0 investment
- Real results: time saved, errors eliminated, revenue increased
- Step-by-step breakdowns you can copy

**Community Discussions** 💬
- Share your automation wins
- Get help with implementation challenges
- Connect with other AI enthusiasts

### 🚀 **My Background:**
I've been working with AI automation systems for years, helping businesses implement practical solutions that deliver real ROI. From e-commerce automation to content generation, I focus on tools that work today, not theoretical future tech.

### 💡 **Today's Quick Tip:**
The biggest AI automation mistake? Trying to automate everything at once. Start with ONE repetitive task that costs you 2+ hours per week. Master that, then expand.

### 🎯 **What's Coming Next:**
- **Monday:** Daily AI roundups
- **Tuesday:** Tool spotlights and reviews  
- **Wednesday:** Case studies with real numbers
- **Friday:** Community discussions and Q&A

### 💬 **Let's Connect:**
What's the most time-consuming task in your workflow? Drop a comment - I might feature your automation solution in an upcoming post!

---

**Need personalized AI automation guidance?**  
📧 Email: jmichaeloficial@gmail.com  
📱 Instagram: https://www.instagram.com/jmichaeloficial/

*Building the future, one automation at a time* ⚡

Welcome to the community! 🌟"""

        # Post to subreddit
        subreddit = reddit.subreddit('AIAutomationLabs')
        submission = subreddit.submit(title=title, selftext=content)
        
        print(f"🎉 SUCCESSFULLY POSTED!")
        print(f"📱 Title: {title}")
        print(f"🔗 URL: {submission.url}")
        print(f"📍 Posted to: r/AIAutomationLabs")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Posting to Reddit immediately...")
    post_immediately()