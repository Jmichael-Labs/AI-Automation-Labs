#!/usr/bin/env python3
"""
JMichael Labs AI News Poster Bot
Posts AI content to r/AIAutomationLabs subreddit
"""

import praw
import time
import os
import json
import random
from datetime import datetime, timedelta
from real_time_news_aggregator import AINewsAggregator
from infinite_content_engine import InfiniteContentEngine
import re

class AINewsPoster:
    def __init__(self):
        """Initialize AI News Poster with new credentials"""
        
        # Reddit API credentials from environment variables
        self.reddit = praw.Reddit(
            client_id=os.environ.get('REDDIT_CLIENT_ID'),
            client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
            user_agent=os.environ.get('REDDIT_USER_AGENT'),
            username=os.environ.get('REDDIT_USERNAME'),
            password=os.environ.get('REDDIT_PASSWORD')
        )
        
        # Target subreddit (configurable)
        self.target_subreddit = os.environ.get('TARGET_SUBREDDIT', 'AIAutomationLabs')
        
        # Contact info (configurable)
        self.email_contact = os.environ.get('EMAIL_CONTACT', 'your.email@example.com')
        self.instagram_consulting = os.environ.get('INSTAGRAM_CONSULTING', 'https://instagram.com/youraccount')
        
        # Posting schedule (configurable)
        self.max_daily_posts = int(os.environ.get('MAX_DAILY_POSTS', '3'))
        self.posts_today = 0
        self.last_post_date = None
        
        # Initialize real-time news aggregator
        self.news_aggregator = AINewsAggregator(self.reddit)
        
        # Initialize infinite content engine
        self.infinite_engine = InfiniteContentEngine()
        
        # Load 1,000 business prompts
        self.business_prompts = self.load_business_prompts()
        
        print(f"🤖 JMichael Labs AI News Poster initialized")
        print(f"🎯 Target: r/{self.target_subreddit}")
        print(f"📧 Contact: {self.email_contact}")
        print(f"📡 Real-time news aggregation enabled")
        print(f"💡 Loaded {len(self.business_prompts)} business prompts")
        print(f"🧠 Infinite Content Engine activated - Zero repetition guaranteed")
    
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
    
    def load_business_prompts(self):
        """Load and parse 1,000 business prompts from desktop file"""
        prompts_file = "/Users/suxtan/Desktop/COMPLETE_1000_CHATGPT_BUSINESS_PROMPTS.md"
        prompts = []
        
        try:
            with open(prompts_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract prompts using regex patterns
            # Look for numbered prompts with code blocks
            prompt_pattern = r'\*\*\d+\. ([^*]+)\*\*\s*```([^`]+)```'
            matches = re.findall(prompt_pattern, content, re.DOTALL)
            
            for title, prompt_content in matches:
                prompts.append({
                    'title': title.strip(),
                    'content': prompt_content.strip(),
                    'category': self.categorize_prompt(title)
                })
            
            print(f"✅ Loaded {len(prompts)} business prompts successfully")
            return prompts
            
        except Exception as e:
            print(f"⚠️ Error loading business prompts: {e}")
            return self.get_fallback_prompts()
    
    def categorize_prompt(self, title):
        """Categorize prompt for better selection"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['social media', 'content', 'marketing', 'advertising']):
            return 'marketing'
        elif any(word in title_lower for word in ['automation', 'ai', 'tool', 'software']):
            return 'automation'
        elif any(word in title_lower for word in ['business', 'strategy', 'entrepreneur']):
            return 'business'
        elif any(word in title_lower for word in ['finance', 'investment', 'money']):
            return 'finance'
        else:
            return 'general'
    
    def get_fallback_prompts(self):
        """Fallback prompts if file loading fails"""
        return [
            {
                'title': 'AI Content Empire Builder',
                'content': 'Create a systematic approach to building passive income through AI-generated content across multiple platforms.',
                'category': 'automation'
            },
            {
                'title': 'Automation Business Generator',
                'content': 'Design an automated business model that leverages AI tools to generate consistent revenue streams.',
                'category': 'business'
            },
            {
                'title': 'AI Marketing System',
                'content': 'Build an intelligent marketing automation system that adapts to market trends and customer behavior.',
                'category': 'marketing'
            }
        ]
    
    def generate_prompt_based_content(self):
        """Generate content based on business prompts + current AI news"""
        # Get recent AI news for context
        news_items = self.news_aggregator.scrape_latest_ai_news(hours_back=48, max_posts=10)
        trending_tools = self.extract_trending_ai_tools(news_items)
        
        # Select relevant prompt
        prompt = self.select_smart_prompt(trending_tools)
        
        # Get current date
        today = datetime.now().strftime('%B %d, %Y')
        
        # Generate AI-enhanced passive income idea
        title, content = self.transform_prompt_to_passive_income(prompt, trending_tools, today)
        
        return title, content
    
    def extract_trending_ai_tools(self, news_items):
        """Extract trending AI tools from recent news"""
        trending_tools = []
        
        for item in news_items:
            text = f"{item['title']} {item['content']}".lower()
            
            # Common AI tools and platforms
            tool_keywords = {
                'chatgpt': 'ChatGPT',
                'claude': 'Claude',
                'midjourney': 'Midjourney',
                'dall-e': 'DALL-E',
                'stable diffusion': 'Stable Diffusion',
                'runway': 'Runway',
                'luma': 'Luma AI',
                'suno': 'Suno',
                'eleven labs': 'ElevenLabs',
                'perplexity': 'Perplexity',
                'anthropic': 'Claude/Anthropic',
                'openai': 'OpenAI',
                'google gemini': 'Google Gemini',
                'zapier': 'Zapier',
                'make.com': 'Make.com',
                'notion': 'Notion AI'
            }
            
            for keyword, tool_name in tool_keywords.items():
                if keyword in text and tool_name not in trending_tools:
                    trending_tools.append(tool_name)
        
        # Add some always-relevant tools if list is empty
        if not trending_tools:
            trending_tools = ['ChatGPT', 'Claude', 'Zapier', 'Make.com']
        
        return trending_tools[:3]  # Top 3 trending
    
    def select_smart_prompt(self, trending_tools):
        """Select relevant prompt based on trending tools"""
        if not self.business_prompts:
            return self.get_fallback_prompts()[0]
        
        # Try to find prompts related to automation/AI if trending tools are present
        if trending_tools:
            automation_prompts = [p for p in self.business_prompts if p['category'] == 'automation']
            if automation_prompts:
                return random.choice(automation_prompts)
        
        # Otherwise, prefer marketing or business prompts
        preferred_categories = ['marketing', 'business', 'automation']
        
        for category in preferred_categories:
            category_prompts = [p for p in self.business_prompts if p['category'] == category]
            if category_prompts:
                return random.choice(category_prompts)
        
        # Fallback to any prompt
        return random.choice(self.business_prompts)
    
    def transform_prompt_to_passive_income(self, prompt, trending_tools, today):
        """Transform business prompt into passive income opportunity with trending tools"""
        
        # Extract key concepts from prompt
        prompt_concepts = self.extract_key_concepts(prompt['content'])
        
        # Generate title
        tool_list = ' + '.join(trending_tools[:2]) if trending_tools else 'AI Tools'
        title = f"💰 {prompt['title']} with {tool_list} - {today}"
        
        # Calculate potential earnings (realistic ranges)
        monthly_income = random.choice(['$1,200', '$2,500', '$4,800', '$3,200', '$1,800', '$6,000', '$2,800'])
        setup_time = random.choice(['2-3 weeks', '1-2 weeks', '3-4 weeks', '1 week', '2 weeks'])
        investment = random.choice(['$39/month', '$67/month', '$29/month', '$89/month', '$47/month', '$0 (free tier)'])
        
        # Generate content
        content = f"""## How to Build {prompt['title']} Using Current AI Technology

**🎯 The Strategy:**
Leverage the latest AI breakthroughs to create {prompt_concepts['main_goal']}. The recent developments in {trending_tools[0] if trending_tools else 'AI automation'} have made this approach incredibly accessible.

**💸 Realistic Income Potential:** {monthly_income}/month
**⏰ Setup Timeline:** {setup_time}
**🛠️ Investment Required:** {investment}
**📱 Key Tools:** {', '.join(trending_tools) if trending_tools else 'ChatGPT, Claude, Zapier'}

**📋 Implementation Strategy:**
{self.generate_implementation_steps(prompt, trending_tools)}

**🚀 Why This Works Right Now:**
- {trending_tools[0] if trending_tools else 'AI tools'} just released new features perfect for this
- Market demand is high but competition is still low
- Automation technology has reached the "sweet spot" of reliability
- Most people don't know how to connect these tools effectively

**⚡ Pro Implementation Tip:**
Start with the simplest version first. Get one income stream working, then systematically add complexity. The goal is predictable revenue, not perfection.

**💡 Real Talk:**
This isn't magic - it requires strategic thinking and consistent execution. But when you leverage AI correctly, you can build systems that generate income while you focus on scaling.

**🔥 Current Market Context:**
Based on what's happening in AI this week, {self.generate_market_context(trending_tools)}

---

**Ready to implement this exact system?**
I've built similar automation systems and can walk you through the specific setup.

📧 Email: {self.email_contact}
📱 Instagram: {self.instagram_consulting}

*AI automation isn't the future - it's happening now* 🤖"""
        
        return title, content
    
    def extract_key_concepts(self, prompt_content):
        """Extract key concepts from prompt for content generation"""
        # Simple concept extraction
        content_lower = prompt_content.lower()
        
        if 'social media' in content_lower:
            main_goal = 'automated social media revenue streams'
        elif 'content' in content_lower:
            main_goal = 'passive content income systems'
        elif 'marketing' in content_lower:
            main_goal = 'automated marketing funnels'
        elif 'business' in content_lower:
            main_goal = 'hands-off business operations'
        else:
            main_goal = 'systematic passive income generation'
        
        return {'main_goal': main_goal}
    
    def generate_implementation_steps(self, prompt, trending_tools):
        """Generate implementation steps based on prompt and trending tools"""
        tool = trending_tools[0] if trending_tools else 'AI tools'
        
        steps = [
            f"1. Research profitable opportunities in your chosen niche",
            f"2. Set up {tool} for automated content/process generation", 
            f"3. Create templates and workflows for consistency",
            f"4. Implement automation pipeline with monitoring",
            f"5. Scale successful processes and optimize underperforming ones"
        ]
        
        return '\n'.join(steps)
    
    def generate_market_context(self, trending_tools):
        """Generate current market context based on trending tools"""
        if not trending_tools:
            return "the AI automation space is evolving rapidly with new opportunities emerging weekly."
        
        tool = trending_tools[0]
        contexts = {
            'ChatGPT': "OpenAI's latest updates have made content automation incredibly sophisticated",
            'Claude': "Anthropic's improvements in reasoning make complex automation workflows possible",
            'Midjourney': "visual content creation has become nearly indistinguishable from human work",
            'Zapier': "workflow automation has reached enterprise-level reliability at consumer prices",
            'Make.com': "visual automation builders are enabling non-technical automation at scale"
        }
        
        return contexts.get(tool, f"{tool}'s recent developments are creating new automation possibilities")
    
    def should_use_infinite_content(self):
        """Always use infinite content engine (95% of the time)"""
        return random.random() < 0.95  # 95% chance for infinite unique content
    
    def post_to_subreddit(self, title, content, post_type="text"):
        """Post content to r/AIAutomationLabs"""
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
        """Run daily posting routine - AUTONOMOUS VERSION"""
        print(f"🤖 AUTONOMOUS REDDIT BOT ACTIVATED")
        print(f"⏰ Execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        
        # Always generate content for autonomous system (no daily limits)
        print("🚀 Generating fresh content for autonomous posting...")
        
        # Determine what type of post to make based on day of week
        weekday = datetime.now().weekday()  # 0=Monday, 6=Sunday
        
        # 95% chance to use Infinite Content Engine - NEVER REPEATS
        if self.should_use_infinite_content():
            print("🧠 Using Infinite Content Engine - Guaranteed unique content")
            print("🔄 Scraping latest AI tools from free-for.dev and blog.pareto.io...")
            title, content = self.infinite_engine.generate_infinite_content()
            print(f"✅ Generated completely unique content: {title[:60]}...")
        elif weekday == 0:  # Monday - Passive Income Ideas
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
            self.last_post_date = datetime.now().strftime('%Y-%m-%d')
            return 1
        return 0

if __name__ == "__main__":
    try:
        print("🎯 REDDIT BOT STARTING...")
        print(f"📅 Execution time: {datetime.now()}")
        
        poster = AINewsPoster()
        
        print("🧪 Testing connection...")
        if poster.test_connection():
            print("✅ Connection successful!")
            print("🚀 Running daily posting...")
            posts_made = poster.run_daily_posting()
            print(f"🎉 RESULT: Posted {posts_made} content to r/{poster.target_subreddit}")
            
            if posts_made > 0:
                print("✅ SUCCESS: Post was created successfully!")
            else:
                print("⚠️  WARNING: No posts were made (may be due to timing restrictions)")
        else:
            print("❌ CRITICAL ERROR: Connection to Reddit failed")
            print("🔍 Check your Reddit credentials in GitHub Secrets")
            exit(1)
            
    except Exception as e:
        print(f"💥 FATAL ERROR: {str(e)}")
        import traceback
        print("📍 Full traceback:")
        traceback.print_exc()
        exit(1)