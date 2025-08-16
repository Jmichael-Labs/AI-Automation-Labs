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
        
        print(f"🤖 JMichael Labs AI News Poster initialized")
        print(f"🎯 Target: r/{self.target_subreddit}")
        print(f"📧 Contact: {self.email_contact}")
    
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
        """Generate daily AI news post"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        title = f"🚀 Daily AI Roundup - {datetime.now().strftime('%B %d, %Y')}"
        
        content = f"""## Today's AI Developments & Insights

### 🔥 **Trending in AI Today:**

**1. Autonomous Systems Revolution**
- New breakthroughs in AI automation are changing how we work
- Tools like Vercept are enabling no-code automation at scale
- The shift from manual to autonomous workflows is accelerating

**2. Latest AI Tool Discoveries**
- Advanced prompt engineering techniques showing 300% efficiency gains
- Integration platforms simplifying complex AI implementations  
- Cost-effective alternatives to expensive enterprise solutions

**3. Real-World Implementation Stories**
- Small businesses seeing immediate ROI from AI adoption
- Creative professionals augmenting workflows with AI assistants
- E-commerce automation reducing manual work by 80%

### 💡 **JMichael Labs Insight:**
*"The real advantage isn't in having the most advanced AI, but in knowing how to implement the right tools for your specific use case. Focus on problems that cost you time or money - that's where AI delivers immediate value."*

### 🛠️ **Tool Spotlight:**
**This Week:** Vercept.com for e-commerce automation
- No-code solution for Etsy, Shopify, Amazon
- Natural language commands for complex workflows
- Perfect for entrepreneurs who want results without programming

### 💬 **Discussion Question:**
What's the biggest manual task in your workflow that you wish you could automate? Drop your thoughts below! 👇

---

**Want personalized AI implementation guidance?**  
📧 Email: {self.email_contact}  
📱 Instagram: {self.instagram_consulting}

*Building the future, one automation at a time* ⚡"""

        return title, content
    
    def generate_tool_tuesday(self):
        """Generate Tool Tuesday post"""
        tools = [
            {
                "name": "Vercept",
                "use_case": "E-commerce Automation",
                "description": "Tell it what to do, it does it automatically. Perfect for Etsy sellers.",
                "url": "vercept.com"
            },
            {
                "name": "Claude Code",
                "use_case": "Development Automation", 
                "description": "AI-powered coding assistant that understands complex project contexts.",
                "url": "claude.ai/code"
            },
            {
                "name": "Zapier AI",
                "use_case": "Workflow Automation",
                "description": "Connect apps with natural language. No coding required.",
                "url": "zapier.com"
            }
        ]
        
        tool = random.choice(tools)
        
        title = f"🔧 Tool Tuesday: {tool['name']} for {tool['use_case']}"
        
        content = f"""## Tool Spotlight: **{tool['name']}**

### 🎯 **What it does:**
{tool['description']}

### ⚡ **Why I recommend it:**
- **Zero learning curve:** Natural language interface
- **Immediate results:** Start seeing value within hours
- **Cost effective:** Saves more than it costs
- **Scales with you:** Works for solo entrepreneurs to teams

### 🏆 **Real-world use case:**
I've personally used this for automating product uploads to Etsy. What used to take 2 hours now happens automatically while I sleep.

### 📊 **Results:**
- **80% time savings** on repetitive tasks
- **Zero errors** vs manual process
- **24/7 operation** without my involvement

### 🔗 **Try it yourself:**
Check out {tool['name']} at {tool['url']}

### 💬 **Your turn:**
What tools are you using for automation? Share your favorites below! 👇

---

**Need help choosing the right AI stack for your business?**  
📧 Email: {self.email_contact}  
📱 Instagram: {self.instagram_consulting}

*The right tool can change everything* 🚀"""

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
        """Run daily posting routine"""
        if self.posts_today >= self.max_daily_posts:
            print(f"📊 Daily limit reached: {self.posts_today}/{self.max_daily_posts}")
            return 0
        
        # Determine what type of post to make based on day of week
        weekday = datetime.now().weekday()  # 0=Monday, 6=Sunday
        
        if weekday == 0:  # Monday - Daily AI News
            title, content = self.generate_daily_ai_news()
        elif weekday == 1:  # Tuesday - Tool Spotlight  
            title, content = self.generate_tool_tuesday()
        elif weekday == 2:  # Wednesday - Case Study
            title, content = self.generate_case_study()
        elif weekday == 4:  # Friday - Discussion
            title, content = self.generate_discussion_post()
        else:  # Other days - AI News
            title, content = self.generate_daily_ai_news()
        
        success = self.post_to_subreddit(title, content)
        return 1 if success else 0

if __name__ == "__main__":
    poster = AINewsPoster()
    
    print("🧪 Testing connection...")
    if poster.test_connection():
        print("🚀 Running daily posting...")
        posts_made = poster.run_daily_posting()
        print(f"✅ Posted {posts_made} content to r/jmichaelLabs")
    else:
        print("❌ Connection failed")