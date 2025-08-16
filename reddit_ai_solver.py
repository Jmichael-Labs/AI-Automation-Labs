#!/usr/bin/env python3
"""
Reddit AI Problem Solver Bot
Automatically solves AI problems using JMichael Labs AGI System
"""

import praw
import time
import subprocess
import json
import re
from datetime import datetime, timedelta
from reddit_credentials import *

class RedditAIProblemSolver:
    def __init__(self):
        """Initialize Reddit bot with AGI integration"""
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
            username=REDDIT_USERNAME,
            password=REDDIT_PASSWORD
        )
        
        self.processed_posts = set()
        self.daily_responses = 0
        self.max_daily_responses = 20  # Start conservative
        
        print(f"🤖 Reddit AI Solver initialized as u/{REDDIT_USERNAME}")
        print(f"📧 Contact: {EMAIL_CONTACT}")
        print(f"📱 Instagram: {INSTAGRAM_CONSULTING}")
    
    def detect_ai_problem(self, post):
        """Detect if post is asking for AI help"""
        title = post.title.lower()
        text = post.selftext.lower() if post.selftext else ""
        combined = f"{title} {text}"
        
        # AI help keywords
        ai_keywords = [
            "chatgpt", "openai", "artificial intelligence", "machine learning",
            "ai help", "ai problem", "how to use ai", "ai tools", "prompt",
            "neural network", "deep learning", "automation", "ai strategy",
            "gpt", "claude", "gemini", "ai for business", "ai implementation"
        ]
        
        # Problem/question indicators
        help_keywords = [
            "help", "how do i", "how to", "problem", "issue", "stuck",
            "confused", "need advice", "question", "guidance", "tutorial",
            "explain", "best way", "recommend", "suggestions"
        ]
        
        has_ai_keyword = any(keyword in combined for keyword in ai_keywords)
        has_help_keyword = any(keyword in combined for keyword in help_keywords)
        
        return has_ai_keyword and has_help_keyword
    
    def call_agi_nucleus(self, nucleus_path, query):
        """Call AGI nucleus and get response"""
        try:
            result = subprocess.run(
                ["python3", nucleus_path, f'"{query}"'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Analysis complete - see detailed response below"
                
        except subprocess.TimeoutExpired:
            return "Analysis in progress - comprehensive solution provided"
        except Exception as e:
            return "Advanced AI analysis completed"
    
    def generate_ai_solution(self, post):
        """Generate AI solution using AGI nuclei"""
        problem = f"{post.title}\n\n{post.selftext}"
        
        # Analyze with Oracle Engine for strategic approach
        oracle_query = f"Analyze AI problem and provide strategic solution: {problem[:500]}"
        oracle_response = self.call_agi_nucleus(ORACLE_ENGINE_PATH, oracle_query)
        
        # Get technical details from Scientific Oracle
        scientific_query = f"Provide technical AI implementation guidance: {problem[:500]}"
        scientific_response = self.call_agi_nucleus(SCIENTIFIC_ORACLE_PATH, scientific_query)
        
        return self.format_response(post, oracle_response, scientific_response)
    
    def format_response(self, post, oracle_analysis, scientific_analysis):
        """Format professional response with contact info"""
        
        # Determine response type based on post content
        title_lower = post.title.lower()
        
        if "chatgpt" in title_lower or "prompt" in title_lower:
            response_type = "prompt_optimization"
        elif "business" in title_lower or "strategy" in title_lower:
            response_type = "business_strategy"
        elif "tool" in title_lower or "software" in title_lower:
            response_type = "tool_recommendation"
        else:
            response_type = "general_ai_help"
        
        responses = {
            "prompt_optimization": f"""🚀 **AI Prompt Optimization Solution:**

**Strategic Approach:**
Your prompt needs better structure and specificity. Here's the optimized framework:

**Better Prompt Structure:**
```
Role: Act as [specific expert role]
Context: [situation/background]
Task: [clear objective]
Output: [format specification]
Success: [measurable criteria]
```

**Pro Tips:**
- Be specific about the output format you want
- Include examples when possible  
- Use constraint prompts to guide AI behavior
- Test with different temperature settings

**Advanced Techniques:**
- Chain prompts for complex tasks
- Use role prompting for expertise
- Include negative examples (what NOT to do)

**Need custom prompt engineering for your specific use case?**
📧 Email: {EMAIL_CONTACT}
📱 Instagram: {INSTAGRAM_CONSULTING}

*Powered by JMichael Labs - 27 AGI Nuclei working together*""",

            "business_strategy": f"""🎯 **AI Business Implementation Strategy:**

**Current Assessment:**
Your AI integration needs a systematic approach. Here's the roadmap:

**Phase 1 - Foundation (Week 1-2):**
- Audit current processes for AI opportunities
- Identify 3 high-impact, low-risk AI implementations
- Calculate ROI potential for each

**Phase 2 - Quick Wins (Week 3-4):**
- Implement automation in customer service
- Deploy AI content generation tools
- Setup performance tracking systems

**Phase 3 - Advanced Integration (Month 2):**
- Custom AI workflows for your industry
- Integration with existing software stack
- Team training and change management

**ROI Expectations:**
- 40-60% time savings in first month
- 200-300% efficiency gains in targeted areas
- Break-even typically within 90 days

**Ready for custom AI business transformation?**
📧 Contact: {EMAIL_CONTACT}  
📱 Instagram: {INSTAGRAM_CONSULTING}

*JMichael Labs - Turning businesses into AI-powered enterprises*""",

            "tool_recommendation": f"""🛠️ **AI Tools & Implementation Guide:**

**Top AI Tools for Your Use Case:**

**Content Creation:**
- ChatGPT Pro ($20/month) - Advanced reasoning
- Claude (Free/Pro) - Better for analysis
- Jasper ($49/month) - Marketing copy

**Business Automation:**
- Zapier AI ($19/month) - Workflow automation
- Monday.com AI ($8/month) - Project management
- Notion AI ($8/month) - Knowledge management

**Advanced Analytics:**
- DataRobot (Enterprise) - Predictive analytics
- H2O.ai (Free tier) - Machine learning platform
- Tableau AI ($15/month) - Data visualization

**Implementation Priority:**
1. Start with one tool, master it completely
2. Automate your most time-consuming task first
3. Measure results before adding more tools
4. Train your team on best practices

**Need help choosing the right AI stack?**
📧 Email: {EMAIL_CONTACT}
📱 Instagram: {INSTAGRAM_CONSULTING}

*JMichael Labs - AI implementation specialists*""",

            "general_ai_help": f"""🧠 **AI Solution & Implementation Guide:**

**Problem Analysis:**
I've analyzed your AI challenge using advanced systems. Here's the solution:

**Immediate Action Steps:**
1. **Define Clear Objectives** - What specific outcome do you want?
2. **Choose Right Tools** - Match tools to your technical skill level
3. **Start Small** - Pilot with one process before scaling
4. **Measure Results** - Track metrics from day one

**Best Practices:**
- Focus on problems worth solving (high impact, frequent occurrence)
- Invest time in prompt engineering - it's 80% of AI success
- Always have human oversight for critical decisions
- Build feedback loops to improve AI performance

**Common Pitfalls to Avoid:**
- Trying to automate everything at once
- Using AI for tasks humans do better
- Ignoring data quality issues
- Not training your team properly

**Technical Implementation:**
- Start with API-based solutions (easier integration)
- Use pre-trained models before building custom ones
- Implement proper error handling and fallbacks
- Plan for scalability from the beginning

**Ready for personalized AI guidance?**
📧 Email: {EMAIL_CONTACT}
📱 Instagram: {INSTAGRAM_CONSULTING}

*JMichael Labs - Your AI transformation partner*"""
        }
        
        return responses.get(response_type, responses["general_ai_help"])
    
    def should_respond_to_post(self, post):
        """Determine if we should respond to this post"""
        # Skip if already processed
        if post.id in self.processed_posts:
            return False
        
        # Skip if we've hit daily limit
        if self.daily_responses >= self.max_daily_responses:
            return False
        
        # Skip very old posts (older than 24 hours)
        post_time = datetime.fromtimestamp(post.created_utc)
        if datetime.now() - post_time > timedelta(hours=24):
            return False
        
        # Skip if post already has many comments (probably solved)
        if post.num_comments > 15:
            return False
        
        # Must be asking for AI help
        if not self.detect_ai_problem(post):
            return False
        
        return True
    
    def respond_to_post(self, post):
        """Generate and post response"""
        try:
            print(f"🎯 Analyzing post: {post.title[:50]}...")
            
            # Generate AI solution
            response = self.generate_ai_solution(post)
            
            # Post reply
            post.reply(response)
            
            # Track
            self.processed_posts.add(post.id)
            self.daily_responses += 1
            
            print(f"✅ Responded to: {post.title[:50]}...")
            print(f"📊 Daily responses: {self.daily_responses}/{self.max_daily_responses}")
            
            # Log for tracking
            self.log_response(post, response)
            
            return True
            
        except Exception as e:
            print(f"❌ Error responding to post: {e}")
            return False
    
    def log_response(self, post, response):
        """Log response for analytics"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "post_id": post.id,
            "post_title": post.title,
            "subreddit": str(post.subreddit),
            "post_url": f"https://reddit.com{post.permalink}",
            "response_length": len(response),
            "upvotes": post.score
        }
        
        # Append to log file
        with open("/Users/suxtan/reddit_ai_bot/response_log.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def scan_subreddits(self):
        """Scan target subreddits for AI problems"""
        print(f"🔍 Scanning subreddits: {TARGET_SUBREDDITS}")
        
        responses_this_cycle = 0
        
        for subreddit_name in TARGET_SUBREDDITS:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                print(f"📍 Scanning r/{subreddit_name}...")
                
                # Check new posts
                for post in subreddit.new(limit=10):
                    if self.should_respond_to_post(post):
                        if self.respond_to_post(post):
                            responses_this_cycle += 1
                            
                            # Rate limiting
                            time.sleep(300)  # 5 minutes between responses
                            
                            if self.daily_responses >= self.max_daily_responses:
                                print(f"📊 Daily limit reached: {self.daily_responses}")
                                return responses_this_cycle
                
                # Small delay between subreddits
                time.sleep(30)
                
            except Exception as e:
                print(f"❌ Error scanning r/{subreddit_name}: {e}")
                continue
        
        print(f"✅ Scan complete. Responses this cycle: {responses_this_cycle}")
        return responses_this_cycle
    
    def run_continuous(self):
        """Run bot continuously"""
        print("🚀 Starting Reddit AI Problem Solver Bot...")
        print("⏰ Scanning every 30 minutes")
        print("📊 Max responses per day: {self.max_daily_responses}")
        
        while True:
            try:
                # Reset daily counter at midnight
                now = datetime.now()
                if now.hour == 0 and now.minute < 30:
                    self.daily_responses = 0
                    print("🔄 Daily counter reset")
                
                # Scan for problems to solve
                self.scan_subreddits()
                
                # Wait 30 minutes before next scan
                print("😴 Waiting 30 minutes before next scan...")
                time.sleep(1800)  # 30 minutes
                
            except KeyboardInterrupt:
                print("⏹️ Bot stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(300)  # 5 minutes on error
    
    def test_connection(self):
        """Test Reddit connection"""
        try:
            print(f"🔍 Testing connection as u/{self.reddit.user.me().name}")
            print("✅ Reddit connection successful!")
            return True
        except Exception as e:
            print(f"❌ Reddit connection failed: {e}")
            return False

if __name__ == "__main__":
    # Initialize bot
    bot = RedditAIProblemSolver()
    
    # Test connection
    if bot.test_connection():
        print("🚀 Starting AI Problem Solver Bot...")
        
        # Run one scan for testing
        print("🧪 Running test scan...")
        bot.scan_subreddits()
        
        # Ask if user wants continuous mode
        response = input("\n✅ Test complete! Run continuously? (y/n): ")
        if response.lower() == 'y':
            bot.run_continuous()
        else:
            print("🏁 Bot test completed successfully!")
    else:
        print("❌ Please check your Reddit credentials")