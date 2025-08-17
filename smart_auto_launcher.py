#!/usr/bin/env python3
"""
Smart Auto Launcher - Reddit AI Bot
Sistema inteligente que detecta cuándo activar el bot automáticamente
"""

import time
import requests
import json
from datetime import datetime, timedelta
import os
import random

class SmartAutoLauncher:
    def __init__(self):
        self.render_url = "https://reddit-ai-problem-solver.onrender.com"
        self.status_file = "/tmp/reddit_bot_status.json"
        self.check_interval = 30 * 60  # Check every 30 minutes
        self.min_daily_interval = 18 * 60 * 60  # Minimum 18 hours between posts
        self.max_daily_interval = 30 * 60 * 60  # Maximum 30 hours between posts
        
        print("🤖 Smart Auto Launcher initialized")
        print(f"📡 Target: {self.render_url}")
        print(f"⏱️  Check interval: {self.check_interval//60} minutes")
        print(f"📅 Post interval: {self.min_daily_interval//3600}-{self.max_daily_interval//3600} hours")
    
    def load_status(self):
        """Load last execution status"""
        try:
            if os.path.exists(self.status_file):
                with open(self.status_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading status: {e}")
        
        return {
            'last_post_time': None,
            'last_check_time': None,
            'total_posts': 0,
            'consecutive_failures': 0
        }
    
    def save_status(self, status):
        """Save execution status"""
        try:
            with open(self.status_file, 'w') as f:
                json.dump(status, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving status: {e}")
    
    def should_post_today(self, status):
        """Intelligent logic to decide if we should post"""
        now = datetime.now()
        
        # If never posted, post immediately
        if not status['last_post_time']:
            return True, "First time posting"
        
        # Parse last post time
        try:
            last_post = datetime.fromisoformat(status['last_post_time'])
        except:
            return True, "Invalid last post time - posting now"
        
        # Calculate time since last post
        time_since_last = (now - last_post).total_seconds()
        
        # If less than minimum interval, don't post
        if time_since_last < self.min_daily_interval:
            hours_remaining = (self.min_daily_interval - time_since_last) / 3600
            return False, f"Too soon - wait {hours_remaining:.1f} more hours"
        
        # If more than maximum interval, definitely post
        if time_since_last > self.max_daily_interval:
            return True, f"Overdue - {time_since_last/3600:.1f} hours since last post"
        
        # Between min and max - use intelligent probability
        # As time passes, probability increases
        time_factor = (time_since_last - self.min_daily_interval) / (self.max_daily_interval - self.min_daily_interval)
        probability = 0.1 + (time_factor * 0.8)  # 10% to 90% probability
        
        # Add randomness based on current hour (prefer posting during active hours)
        current_hour = now.hour
        if 8 <= current_hour <= 22:  # 8 AM to 10 PM - active hours
            probability *= 1.5
        elif 23 <= current_hour or current_hour <= 6:  # Night hours
            probability *= 0.3
        
        # Cap probability at 95%
        probability = min(probability, 0.95)
        
        should_post = random.random() < probability
        return should_post, f"Probability: {probability:.1%} - {'Posting' if should_post else 'Waiting'}"
    
    def check_render_health(self):
        """Check if Render service is healthy"""
        try:
            response = requests.get(f"{self.render_url}/ping", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return True, data.get('timestamp', 'Unknown')
            else:
                return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    def trigger_bot_run(self):
        """Trigger bot execution on Render"""
        try:
            print("🚀 Triggering bot run on Render...")
            response = requests.post(f"{self.render_url}/run", timeout=300)  # 5 minute timeout
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    posts_count = data.get('posts_generated', 0)
                    execution_time = data.get('execution_time_seconds', 0)
                    return True, f"Success: {posts_count} posts in {execution_time:.1f}s"
                else:
                    return False, f"Bot returned: {data.get('status', 'unknown')}"
            else:
                return False, f"HTTP {response.status_code}: {response.text[:100]}"
                
        except Exception as e:
            return False, f"Request failed: {str(e)}"
    
    def run_smart_check(self):
        """Run one intelligent check cycle"""
        now = datetime.now()
        print(f"\n⏰ Smart check at {now.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Load status
        status = self.load_status()
        
        # Check if Render is healthy
        health_ok, health_msg = self.check_render_health()
        if not health_ok:
            print(f"❌ Render service unhealthy: {health_msg}")
            status['consecutive_failures'] += 1
            status['last_check_time'] = now.isoformat()
            self.save_status(status)
            return
        
        print(f"✅ Render service healthy: {health_msg}")
        
        # Check if we should post
        should_post, reason = self.should_post_today(status)
        print(f"🤔 Post decision: {reason}")
        
        if should_post:
            # Trigger bot run
            success, result_msg = self.trigger_bot_run()
            
            if success:
                print(f"🎉 Bot run successful: {result_msg}")
                status['last_post_time'] = now.isoformat()
                status['total_posts'] += 1
                status['consecutive_failures'] = 0
            else:
                print(f"❌ Bot run failed: {result_msg}")
                status['consecutive_failures'] += 1
        else:
            print("⏳ Not posting this time")
        
        # Update status
        status['last_check_time'] = now.isoformat()
        self.save_status(status)
        
        # Show summary
        print(f"📊 Summary: {status['total_posts']} total posts, {status['consecutive_failures']} consecutive failures")
    
    def run_continuous(self):
        """Run continuous monitoring"""
        print("🔄 Starting continuous smart monitoring...")
        print("⚠️  Press Ctrl+C to stop")
        
        try:
            while True:
                self.run_smart_check()
                
                # Wait for next check
                print(f"😴 Sleeping for {self.check_interval//60} minutes...")
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Smart launcher stopped by user")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
    
    def run_once(self):
        """Run single check (for testing)"""
        print("🧪 Running single smart check...")
        self.run_smart_check()
        print("✅ Single check completed")

if __name__ == "__main__":
    import sys
    
    launcher = SmartAutoLauncher()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        launcher.run_once()
    else:
        launcher.run_continuous()