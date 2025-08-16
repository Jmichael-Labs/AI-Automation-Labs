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
        """Detect if post is related to AI (much more permissive)"""
        title = post.title.lower()
        text = post.selftext.lower() if post.selftext else ""
        combined = f"{title} {text}"
        
        # Expanded AI keywords - más amplio
        ai_keywords = [
            "chatgpt", "openai", "artificial intelligence", "machine learning", "ai",
            "prompt", "neural network", "deep learning", "automation", "bot",
            "gpt", "claude", "gemini", "llm", "model", "algorithm", "data science",
            "python ai", "tensorflow", "pytorch", "hugging face", "langchain",
            "rag", "vector", "embedding", "fine-tuning", "training", "api",
            "nlp", "computer vision", "generative", "transformer", "copilot"
        ]
        
        # Mucho más flexible - no requiere help keywords específicos
        engagement_indicators = [
            "help", "how", "what", "why", "when", "where", "which", "best",
            "recommend", "advice", "opinion", "thoughts", "experience", "tips",
            "guide", "tutorial", "learn", "understand", "explain", "compare",
            "vs", "better", "good", "bad", "works", "doesn't work", "issue",
            "problem", "solution", "idea", "project", "building", "creating",
            "?", "anyone", "suggestions", "feedback", "review"
        ]
        
        has_ai_keyword = any(keyword in combined for keyword in ai_keywords)
        has_engagement = any(keyword in combined for keyword in engagement_indicators)
        
        # Mucho más permisivo: solo necesita AI keyword OR estar en subreddit AI
        is_ai_subreddit = post.subreddit.display_name.lower() in [
            'artificial', 'machinelearning', 'chatgpt', 'openai', 
            'artificialintelligence', 'deeplearning', 'mlquestions'
        ]
        
        return has_ai_keyword or (is_ai_subreddit and has_engagement)
    
    def generate_ai_solution(self, post):
        """Generate AI solution (simplified for Render deployment)"""
        problem = f"{post.title}\n\n{post.selftext}"
        
        # For Render deployment, we'll use pre-built responses instead of calling AGI nuclei
        # This avoids timeout issues and complex subprocess calls
        return self.format_response(post)
    
    def format_response(self, post):
        """Format conversational, helpful response with contact info"""
        
        title_lower = post.title.lower()
        
        # More nuanced response selection
        if any(word in title_lower for word in ["chatgpt", "prompt", "gpt", "claude"]):
            response_type = "prompt_optimization"
        elif any(word in title_lower for word in ["business", "strategy", "company", "startup"]):
            response_type = "business_strategy"
        elif any(word in title_lower for word in ["tool", "software", "app", "platform", "recommend"]):
            response_type = "tool_recommendation"
        elif any(word in title_lower for word in ["learn", "tutorial", "beginner", "start"]):
            response_type = "learning_guide"
        else:
            response_type = "general_ai_help"
        
        responses = {
            "prompt_optimization": f"""Hey! I've been working with ChatGPT and other AI tools extensively - here's what actually works:

**The key is being super specific.** Instead of "write me content", try:
- "Write a 300-word LinkedIn post about [topic] for [audience] with [tone]"
- Always include context, desired outcome, and format
- Add "Think step by step" at the end - it really helps

**Pro tips that changed my game:**
1. Give it a role: "You are an expert [field] consultant..."
2. Provide examples of what you want
3. Use constraints: word count, style, audience level
4. Iterate - first response is rarely perfect

**Template that works:**
```
Role: You are [expert type]
Context: [situation/background]  
Task: [specific action]
Format: [how you want output]
Audience: [who will read this]
```

The difference in quality is honestly night and day when you structure it right.

Need help with specific prompts? Feel free to reach out: {self.email_contact} or {self.instagram_consulting}

*Hope this helps!*""",

            "learning_guide": f"""Great question! I remember being in the same spot when I started with AI.

**Here's honestly the fastest path I wish someone told me:**

**Week 1-2: Get your hands dirty**
- Pick ONE tool (ChatGPT is fine to start)
- Use it for actual work problems, not tutorials
- You'll learn faster by solving real stuff

**Week 3-4: Understand the fundamentals**
- Learn prompt engineering (this is 80% of success)
- Understand tokens, context windows, temperature
- Try different AI models to see strengths/weaknesses

**Month 2: Go deeper**
- Learn APIs if you want automation
- Try specialized tools for your field
- Start building actual workflows

**Biggest mistakes I made (so you don't have to):**
- Trying to learn everything at once
- Following too many tutorials instead of practicing
- Not focusing on ONE use case first

**Actually useful resources:**
- OpenAI Playground (free, great for learning)
- Anthropic's Claude (often better than ChatGPT)
- Build simple projects with real problems you have

The key is consistent practice with real problems, not consuming more content.

What specific area are you looking to apply AI to? Happy to give more targeted advice: {self.email_contact}

*Good luck!*""",

            "business_strategy": f"""I've helped several businesses integrate AI successfully. Here's what actually works:

**Start simple, scale smart:**
- Pick ONE process that eats tons of time (customer support, content creation, data entry)
- Test AI on that specific thing for 2 weeks
- Measure actual time/cost savings before expanding

**Tools that deliver real ROI:**
- ChatGPT for content and communication (saves 3-5 hours/week)
- Zapier for workflow automation (connect your apps)
- Notion AI for documentation and knowledge management

**Common mistakes I see:**
- Trying to AI-ify everything at once (recipe for chaos)
- Choosing fancy tools without clear use cases
- Not training the team properly (they'll resist if confused)

**My recommended sequence:**
1. Week 1: Pick one repetitive task, test AI solution
2. Week 2: Measure results, get team feedback
3. Week 3: Optimize the solution based on learnings
4. Month 2: Add one more AI workflow

**The key:** Focus on problems that cost you real time/money, not just cool tech.

What specific business process are you looking to improve? Happy to give more targeted advice: {self.email_contact} or {self.instagram_consulting}""",

            "tool_recommendation": f"""Based on what you're asking about, here are the tools I actually use and recommend:

**For content/writing:**
- ChatGPT Plus ($20/month) - Best overall, great for ideation
- Claude (Anthropic) - Better for analysis and longer content  
- Grammarly AI - Editing and tone adjustment

**For business automation:**
- Zapier ($20/month) - Connect different apps automatically
- Make.com (cheaper Zapier alternative)
- Notion AI - Great for team knowledge management

**For data/analysis:**
- ChatGPT with Code Interpreter - Surprisingly good at data analysis
- Tableau with AI features - If you need real dashboards
- Excel with Copilot - If you're already in Microsoft ecosystem

**Free options to start with:**
- ChatGPT free tier
- Claude free tier  
- Google Bard
- Bing Chat

**My advice:** Start with the free versions, find what you actually use daily, THEN upgrade. Don't buy everything at once.

What's your specific use case? I can give you a more targeted recommendation: {self.email_contact}""",

            "general_ai_help": f"""I've been working with AI systems for a while - here's my take on your situation:

**The practical approach that works:**

1. **Start with your biggest pain point** - What task do you wish you could delegate?
2. **Test before you invest** - Most AI tools have free trials, use them
3. **Focus on one workflow** - Master one AI application before adding more

**What I wish someone told me when I started:**
- AI is a tool, not magic - it needs good inputs to give good outputs
- The learning curve is mostly about prompt engineering, not the tech
- 80% of AI success comes from asking the right questions

**Common patterns that work:**
- Use AI for first drafts, humans for final edits
- Automate repetitive tasks, keep humans for creative decisions  
- Think "AI-assisted" not "AI-replacement"

**Red flags to avoid:**
- Tools that promise to "replace your entire team"
- Solutions that seem too good to be true (they usually are)
- Not having a clear success metric

The best AI implementations solve real problems you already have, they don't create new workflows just because it's cool tech.

What specific challenge are you trying to solve? Feel free to reach out: {self.email_contact}

*Hope this helps!*"""
        }
        
        return responses.get(response_type, responses["general_ai_help"])
    
    def should_respond_to_post(self, post, stats=None):
        """Determine if we should respond to this post"""
        # Skip if already processed
        if post.id in self.processed_posts:
            if stats: stats['processed'] += 1
            return False
        
        # Skip if we've hit daily limit
        if self.daily_responses >= self.max_daily_responses:
            print(f"📊 Daily limit reached: {self.daily_responses}/{self.max_daily_responses}")
            return False
        
        # Skip very old posts (extended to 7 days for maximum opportunities)
        post_time = datetime.fromtimestamp(post.created_utc)
        if datetime.now() - post_time > timedelta(days=7):
            return False
        
        # Skip if post already has TOO many comments (very permissive)
        if post.num_comments > 200:
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
        total_posts_scanned = 0
        posts_by_reason = {
            'processed': 0,
            'too_old': 0, 
            'too_many_comments': 0,
            'already_commented': 0,
            'no_ai_detected': 0,
            'passed_filters': 0
        }
        
        for subreddit_name in self.TARGET_SUBREDDITS:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                print(f"📍 Scanning r/{subreddit_name}...")
                
                # Check MANY more posts for maximum opportunities  
                for post in subreddit.new(limit=50):
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