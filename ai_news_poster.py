#!/usr/bin/env python3
"""
JMichael Labs AI News Poster Bot
Posts AI content to r/jmichaelLabs subreddit
"""

import praw
import time
import os
import json
import random
from datetime import datetime, timedelta
from real_time_news_aggregator import AINewsAggregator

class AINewsPoster:
    def __init__(self):
        """Initialize AI News Poster with new credentials"""
        
        # New working credentials
        self.reddit = praw.Reddit(
            client_id=os.environ.get('REDDIT_CLIENT_ID', 'WWPlll5usdslxz9bQqEvZg'),
            client_secret=os.environ.get('REDDIT_CLIENT_SECRET', 'c7gBvHnTuQO1v3eiHLt8IotVuSVhyQ'),
            user_agent=os.environ.get('REDDIT_USER_AGENT', 'JMichaelLabsBot:v1.0 (by /u/theinnovationla)'),
            username=os.environ.get('REDDIT_USERNAME', 'theinnovationla'),
            password=os.environ.get('REDDIT_PASSWORD', 'Suxtan20@')
        )
        
        # Target subreddit
        self.target_subreddit = "jmichaelLabs"
        
        # Contact info
        self.email_contact = os.environ.get('EMAIL_CONTACT', 'jmichaeloficial@gmail.com')
        self.instagram_consulting = os.environ.get('INSTAGRAM_CONSULTING', 'https://www.instagram.com/jmichaeloficial/')
        
        # Posting schedule
        self.max_daily_posts = 1  # Conservative start
        self.posts_today = 0
        self.last_post_date = None
        
        # Initialize real-time news aggregator
        self.news_aggregator = AINewsAggregator(self.reddit)
        
        print(f"🤖 JMichael Labs AI News Poster initialized")
        print(f"🎯 Target: r/{self.target_subreddit}")
        print(f"📧 Contact: {self.email_contact}")
        print(f"📡 Real-time news aggregation enabled")
    
    def test_connection(self):
        """Test Reddit connection with new credentials"""
        try:
            user = self.reddit.user.me()
            print(f"✅ Connected as: u/{user.name}")
            print(f"📊 Comment Karma: {user.comment_karma}")
            print(f"📊 Link Karma: {user.link_karma}")
            
            # Test subreddit access
            subreddit = self.reddit.subreddit(self.target_subreddit)
            print(f"📍 Testing r/{self.target_subreddit} access...")
            print(f"✅ Subreddit: {subreddit.display_name} - {subreddit.subscribers} subscribers")
            
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def generate_daily_ai_news(self):
        """Generate daily passive income focused AI post"""
        print("Generating AI passive income content...")
        
        passive_income_ideas = [
            {
                "title": "Build a $2K/Month AI Content Farm (Zero Programming)",
                "tool": "Claude + Zapier + WordPress",
                "investment": "$47/month",
                "timeframe": "2-4 weeks setup",
                "method": "AI writes articles → Auto-publish → Ad revenue + affiliates",
                "steps": "1. Pick profitable niche 2. Setup WordPress + ads 3. Connect Claude API 4. Create content pipeline"
            },
            {
                "title": "AI Product Review Empire ($1.5K/Month Passive)",
                "tool": "ChatGPT + Shopify + Amazon Affiliate",
                "investment": "$29/month",
                "timeframe": "3-5 weeks",
                "method": "AI generates product reviews → Auto-post → Affiliate commissions",
                "steps": "1. Choose product category 2. Setup review site 3. AI content generation 4. Affiliate link automation"
            },
            {
                "title": "Automated YouTube Shorts Channel ($3K/Month)",
                "tool": "Pictory + DALL-E + TikTok API",
                "investment": "$67/month",
                "timeframe": "1-3 weeks",
                "method": "AI creates videos → Auto-upload → Ad revenue + sponsorships",
                "steps": "1. Research viral niches 2. Setup automation tools 3. Content pipeline 4. Monetization setup"
            },
            {
                "title": "AI Newsletter Empire ($4K/Month Subscription)",
                "tool": "GPT-4 + ConvertKit + Substack",
                "investment": "$39/month",
                "timeframe": "4-6 weeks",
                "method": "AI curates + writes newsletter → Auto-send → Paid subscriptions",
                "steps": "1. Choose expertise niche 2. Setup email platform 3. AI content curation 4. Subscription funnel"
            },
            {
                "title": "Etsy Digital Products on Autopilot ($2.5K/Month)",
                "tool": "Midjourney + Printful + Etsy API",
                "investment": "$55/month",
                "timeframe": "2-3 weeks",
                "method": "AI designs products → Auto-list → Print-on-demand fulfillment",
                "steps": "1. Research trending designs 2. AI art generation 3. Listing automation 4. Order fulfillment setup"
            }
        ]
        
        idea = random.choice(passive_income_ideas)
        today = datetime.now().strftime('%B %d, %Y')
        
        title = f"💰 {idea['title']} - {today}"
        
        content = f"""## How to Build {idea['title'].split('(')[0].strip()}

**🎯 The Opportunity:**
{idea['method']}

**💸 Investment Required:** {idea['investment']}
**⏰ Setup Time:** {idea['timeframe']}
**🛠️ Tools Needed:** {idea['tool']}

**📋 Action Steps:**
{idea['steps']}

**🚀 Why This Works in 2025:**
- AI tools have matured (quality + reliability)
- Automation platforms are user-friendly
- Market demand for AI-generated content is huge
- Most people still don't know how to implement this

**⚡ Pro Tip:**
Start with one income stream, perfect it, then scale to multiple. The key is consistency and letting AI handle the heavy lifting while you focus on optimization.

**💡 Real Talk:**
This isn't "get rich quick" - it's "get rich smart." AI does the work, you reap the rewards, but you still need to set it up correctly.

---

**Need help setting up your AI passive income stream?**
I've built multiple systems like this and can show you the exact implementation.

📧 Email: {self.email_contact}
📱 Instagram: {self.instagram_consulting}

*AI + Automation = Your Time Freedom* 🤖"""

        return title, content
    
    def generate_tool_tuesday(self):
        """Generate Tool Tuesday post - Passive Income Tools"""
        tools = [
            {
                "name": "Vercept",
                "use_case": "E-commerce Automation",
                "roi": "$2,000/month",
                "cost": "$47/month",
                "description": "Natural language e-commerce automation. Tell it what to do, it does it automatically.",
                "setup": "Connect to Etsy/Shopify → Give commands in plain English → Watch it work"
            },
            {
                "name": "Make.com + ChatGPT",
                "use_case": "Content Pipeline Automation",
                "roi": "$1,500/month",
                "cost": "$29/month",
                "description": "AI content creation + automatic publishing across multiple platforms.",
                "setup": "Design workflow → Connect AI tools → Set publishing schedule"
            },
            {
                "name": "Zapier + Claude",
                "use_case": "Newsletter Automation",
                "roi": "$3,000/month",
                "cost": "$39/month",
                "description": "AI curates content and writes newsletters automatically.",
                "setup": "Connect data sources → AI content creation → Email automation"
            }
        ]
        
        tool = random.choice(tools)
        
        title = f"🛠️ Tool Tuesday: {tool['name']} for {tool['use_case']}"
        
        content = f"""## Tool Spotlight: **{tool['name']}**

**What it does:**
{tool['description']}

**Passive Income Potential:** {tool['roi']}
**Monthly Cost:** {tool['cost']}

**How to set it up:**
{tool['setup']}

**Why this tool wins in 2025:**
- No coding required
- Works while you sleep
- Scales automatically
- AI handles the complexity

**Real implementation example:**
I set this up for a client who went from 5 hours/week manual work to completely automated income generation. They're now pulling in consistent monthly revenue with minimal oversight.

**Your next steps:**
1. Sign up for free trial
2. Follow the setup process
3. Start with one simple automation
4. Scale once you see results

**Pro tip:** Don't try to automate everything at once. Pick one income stream, perfect it, then expand.

---

**Want me to walk you through the exact setup?**
I've implemented these systems multiple times and can show you the shortcuts.

📧 Email: {self.email_contact}
📱 Instagram: {self.instagram_consulting}

*The right tool can generate passive income* 💰"""

        return title, content
    
    def generate_case_study(self):
        """Generate case study post"""
        title = "📊 Case Study: How I Automated My Entire E-commerce Workflow"
        
        content = f"""## Real Implementation: $0 Investment → Complete Automation

### 🎯 **The Challenge:**
Manual product uploads to Etsy were consuming 10+ hours per week. Each listing required:
- Product photos editing
- SEO-optimized descriptions  
- Pricing research
- Tag optimization
- Publishing across platforms

### 🛠️ **The Solution Stack:**
1. **Vercept** - Main automation engine
2. **Claude** - Content generation
3. **GitHub Actions** - Scheduling
4. **Render.com** - 24/7 hosting

**Total cost:** $0 (using free tiers)

### ⚡ **Implementation Process:**

**Week 1:** Tool research and testing
- Tested 15+ automation platforms
- Vercept emerged as the clear winner
- Simple natural language commands

**Week 2:** Workflow design  
- Mapped entire product upload process
- Created templates for consistency
- Built fallback procedures

**Week 3:** Full automation deployment
- Connected all platforms
- Set up monitoring systems
- Implemented error handling

### 📈 **Results After 30 Days:**

**Time Savings:**
- **Before:** 10 hours/week manual work
- **After:** 30 minutes/week monitoring
- **Savings:** 9.5 hours/week = 38 hours/month

**Quality Improvements:**
- **Zero human errors** in listings
- **Consistent SEO optimization**
- **24/7 operation** capability

**Business Impact:**
- **3x more products** listed per month
- **Better consistency** across platforms
- **Freedom to focus** on strategy vs operations

### 💡 **Key Learnings:**

1. **Start simple** - Automate one process completely before adding more
2. **Monitor closely** - First month requires attention to catch edge cases  
3. **Document everything** - You'll forget the setup details
4. **Plan for failures** - Always have manual backup procedures

### 🎯 **Next Steps:**
Now working on automating customer service and inventory management using the same principles.

### 💬 **Questions for the community:**
- What processes are eating your time?
- What's stopping you from implementing automation?
- Want me to document any specific implementation?

---

**Want me to help you design your automation strategy?**  
📧 Email: {self.email_contact}  
📱 Instagram: {self.instagram_consulting}

*Automation isn't about replacing humans - it's about freeing humans to do what they do best* 🚀"""

        return title, content
    
    def generate_discussion_post(self):
        """Generate discussion post for community engagement"""
        discussions = [
            {
                "title": "🤔 What's the biggest AI myth you've encountered?",
                "content": "I keep hearing people say 'AI will replace all jobs' or 'You need to be a programmer to use AI effectively.'\n\nWhat misconceptions about AI do you encounter most often? Let's debunk them together! 👇"
            },
            {
                "title": "💡 Share your AI automation win (no matter how small!)",
                "content": "Whether you automated sending emails, generating content, or organizing files - every win counts!\n\nWhat's one thing you've successfully automated recently? Inspire others with your success! 🚀"
            },
            {
                "title": "🎯 What would you automate if you knew it was possible?",
                "content": "Dream big! If you could wave a magic wand and automate any part of your work or life, what would it be?\n\nSometimes the 'impossible' is just one tool discovery away. Share your automation wishlist! ✨"
            }
        ]
        
        discussion = random.choice(discussions)
        
        full_content = f"""{discussion['content']}

### 💬 **Discussion Guidelines:**
- Share specific examples when possible
- Ask follow-up questions  
- Help others with implementation ideas
- No tool is too simple to mention!

### 🏆 **Community Value:**
Your experience might be exactly what someone else needs to hear. Every automation journey starts with inspiration from others who've walked the path.

---

**Got questions about AI implementation?**  
📧 Email: {self.email_contact}  
📱 Instagram: {self.instagram_consulting}

*Building the future together* 🌟"""

        return discussion['title'], full_content
    
    def post_to_subreddit(self, title, content, post_type="text"):
        """Post content to r/jmichaelLabs"""
        try:
            subreddit = self.reddit.subreddit(self.target_subreddit)
            
            # Submit post
            submission = subreddit.submit(title=title, selftext=content)
            
            print(f"✅ Posted: {title[:50]}...")
            print(f"🔗 URL: {submission.url}")
            
            self.posts_today += 1
            return True
            
        except Exception as e:
            print(f"❌ Error posting: {e}")
            return False
    
    def run_daily_posting(self):
        """Run daily posting routine with duplicate prevention"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Check if already posted today
        if self.last_post_date == today:
            print(f"📊 Already posted today ({today})")
            return 0
            
        if self.posts_today >= self.max_daily_posts:
            print(f"📊 Daily limit reached: {self.posts_today}/{self.max_daily_posts}")
            return 0
        
        # Determine what type of post to make based on day of week
        weekday = datetime.now().weekday()  # 0=Monday, 6=Sunday
        
        if weekday == 0:  # Monday - Passive Income Ideas
            title, content = self.generate_daily_ai_news()
        elif weekday == 1:  # Tuesday - Tool Spotlight  
            title, content = self.generate_tool_tuesday()
        elif weekday == 2:  # Wednesday - Case Study
            title, content = self.generate_case_study()
        elif weekday == 4:  # Friday - Discussion
            title, content = self.generate_discussion_post()
        else:  # Other days - Passive Income Ideas
            title, content = self.generate_daily_ai_news()
        
        success = self.post_to_subreddit(title, content)
        if success:
            self.last_post_date = today
            return 1
        return 0

if __name__ == "__main__":
    poster = AINewsPoster()
    
    print("🧪 Testing connection...")
    if poster.test_connection():
        print("🚀 Running daily posting...")
        posts_made = poster.run_daily_posting()
        print(f"✅ Posted {posts_made} content to r/jmichaelLabs")
    else:
        print("❌ Connection failed")