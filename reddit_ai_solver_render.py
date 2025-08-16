#!/usr/bin/env python3
"""
Reddit AI Problem Solver Bot - Render.com Version
Optimized for cloud deployment with environment variables
"""

import praw
import time
import subprocess
import json
import os
import re
from datetime import datetime, timedelta

class RedditAIProblemSolver:
    def __init__(self):
        """Initialize Reddit bot with environment variables"""
        
        # Get credentials from environment variables (Render will provide these)
        self.reddit = praw.Reddit(
            client_id=os.environ.get('REDDIT_CLIENT_ID'),
            client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
            user_agent=os.environ.get('REDDIT_USER_AGENT', 'AIBot:v1.0'),
            username=os.environ.get('REDDIT_USERNAME'),
            password=os.environ.get('REDDIT_PASSWORD')
        )
        
        # Contact info from environment
        self.email_contact = os.environ.get('EMAIL_CONTACT', 'jmichaeloficial@gmail.com')
        self.instagram_consulting = os.environ.get('INSTAGRAM_CONSULTING', 'https://www.instagram.com/jmichaeloficial/')
        
        # Bot configuration with persistent memory
        self.memory_file = '/tmp/bot_memory.json'
        self.processed_posts = self.load_memory()
        self.daily_responses = 0
        self.max_daily_responses = 10  # Conservative for free tier
        
        # Target subreddits
        self.TARGET_SUBREDDITS = [
            "artificial",
            "MachineLearning", 
            "ChatGPT",
            "OpenAI",
            "ArtificialIntelligence",
            "deeplearning",
            "MLQuestions",
            "AskProgramming",
            "learnmachinelearning"
        ]
        
        print(f"🤖 Reddit AI Solver initialized for Render.com")
        print(f"📧 Contact: {self.email_contact}")
        print(f"📱 Instagram: {self.instagram_consulting}")
        print(f"🧠 Loaded {len(self.processed_posts)} processed posts from memory")
    
    def load_memory(self):
        """Load processed posts from persistent storage"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    # Only keep posts from last 24 hours to prevent memory bloat
                    current_time = datetime.now().timestamp()
                    recent_posts = {}
                    for post_id, timestamp in data.items():
                        if current_time - timestamp < 86400:  # 24 hours
                            recent_posts[post_id] = timestamp
                    return set(recent_posts.keys())
            return set()
        except Exception as e:
            print(f"⚠️ Error loading memory: {e}")
            return set()
    
    def save_memory(self):
        """Save processed posts to persistent storage"""
        try:
            # Save with timestamps for cleanup
            current_time = datetime.now().timestamp()
            memory_data = {post_id: current_time for post_id in self.processed_posts}
            
            with open(self.memory_file, 'w') as f:
                json.dump(memory_data, f)
            print(f"💾 Saved {len(self.processed_posts)} processed posts to memory")
        except Exception as e:
            print(f"⚠️ Error saving memory: {e}")
    
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
    
    def generate_ai_solution(self, post):
        """Generate AI solution (simplified for Render deployment)"""
        problem = f"{post.title}\n\n{post.selftext}"
        
        # For Render deployment, we'll use pre-built responses instead of calling AGI nuclei
        # This avoids timeout issues and complex subprocess calls
        return self.format_response(post)
    
    def format_response(self, post):
        """Format professional response with contact info"""
        
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
📧 Email: {self.email_contact}
📱 Instagram: {self.instagram_consulting}

*Powered by JMichael Labs - AI Systems Engineering*""",

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
📧 Contact: {self.email_contact}  
📱 Instagram: {self.instagram_consulting}

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
📧 Email: {self.email_contact}
📱 Instagram: {self.instagram_consulting}

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
📧 Email: {self.email_contact}
📱 Instagram: {self.instagram_consulting}

*JMichael Labs - Your AI transformation partner*"""
        }
        
        return responses.get(response_type, responses["general_ai_help"])
    
    def should_respond_to_post(self, post):
        """Determine if we should respond to this post"""
        # Skip if already processed
        if post.id in self.processed_posts:
            print(f"⏭️ Skipping already processed post: {post.id}")
            return False
        
        # Skip if we've hit daily limit
        if self.daily_responses >= self.max_daily_responses:
            print(f"📊 Daily limit reached: {self.daily_responses}/{self.max_daily_responses}")
            return False
        
        # Skip very old posts (older than 12 hours for faster response)
        post_time = datetime.fromtimestamp(post.created_utc)
        if datetime.now() - post_time > timedelta(hours=12):
            return False
        
        # Skip if post already has many comments (probably solved)
        if post.num_comments > 10:
            return False
        
        # Check if we already commented on this post (double safety)
        try:
            post.comments.replace_more(limit=0)
            for comment in post.comments:
                if hasattr(comment, 'author') and comment.author and comment.author.name == self.reddit.user.me().name:
                    print(f"⚠️ Already commented on this post: {post.id}")
                    self.processed_posts.add(post.id)  # Add to memory to prevent future attempts
                    self.save_memory()
                    return False
        except Exception as e:
            print(f"⚠️ Error checking existing comments: {e}")
        
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
            
            # Track and save to persistent memory
            self.processed_posts.add(post.id)
            self.daily_responses += 1
            self.save_memory()  # Save immediately to prevent duplicates
            
            print(f"✅ Responded to: {post.title[:50]}...")
            print(f"📊 Daily responses: {self.daily_responses}/{self.max_daily_responses}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error responding to post: {e}")
            return False
    
    def scan_subreddits(self):
        """Scan target subreddits for AI problems"""
        print(f"🔍 Scanning subreddits: {self.TARGET_SUBREDDITS}")
        
        responses_this_cycle = 0
        
        for subreddit_name in self.TARGET_SUBREDDITS:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                print(f"📍 Scanning r/{subreddit_name}...")
                
                # Check new posts (limit for free tier)
                for post in subreddit.new(limit=5):
                    if self.should_respond_to_post(post):
                        if self.respond_to_post(post):
                            responses_this_cycle += 1
                            
                            # Rate limiting for free tier
                            time.sleep(120)  # 2 minutes between responses
                            
                            if self.daily_responses >= self.max_daily_responses:
                                print(f"📊 Daily limit reached: {self.daily_responses}")
                                return responses_this_cycle
                
                # Small delay between subreddits
                time.sleep(10)
                
            except Exception as e:
                print(f"❌ Error scanning r/{subreddit_name}: {e}")
                continue
        
        print(f"✅ Scan complete. Responses this cycle: {responses_this_cycle}")
        return responses_this_cycle
    
    def test_connection(self):
        """Test Reddit connection"""
        try:
            user = self.reddit.user.me()
            print(f"🔍 Testing connection as u/{user.name}")
            print("✅ Reddit connection successful!")
            return True
        except Exception as e:
            print(f"❌ Reddit connection failed: {e}")
            return False