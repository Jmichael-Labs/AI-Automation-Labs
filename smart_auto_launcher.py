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
        self.posts_per_day = 3  # Target 3 posts daily
        self.min_post_interval = 6 * 60 * 60  # Minimum 6 hours between posts
        self.max_post_interval = 12 * 60 * 60  # Maximum 12 hours between posts
        self.optimal_hours = [9, 15, 20]  # 9AM, 3PM, 8PM EST
        
        print("🤖 Smart Auto Launcher initialized")
        print(f"📡 Target: {self.render_url}")
        print(f"⏱️  Check interval: {self.check_interval//60} minutes")
        print(f"📅 Posts per day: {self.posts_per_day}")
        print(f"⏰ Optimal hours: {self.optimal_hours}")
        print(f"📊 Post interval: {self.min_post_interval//3600}-{self.max_post_interval//3600} hours")
    
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
            'daily_posts': 0,
            'last_post_date': None,
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
        """Intelligent logic for 3 posts daily"""
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        current_hour = now.hour
        
        # Reset daily counter if new day
        if status.get('last_post_date') != current_date:
            status['daily_posts'] = 0
            status['last_post_date'] = current_date
        
        # Check if already hit daily limit
        if status['daily_posts'] >= self.posts_per_day:
            return False, f"Daily limit reached ({status['daily_posts']}/{self.posts_per_day})"
        
        # If never posted today, check optimal timing
        if status['daily_posts'] == 0:
            if current_hour >= 9:  # After 9 AM
                return True, "First post of the day"
            else:
                return False, "Too early - waiting for 9 AM"
        
        # Check minimum interval between posts
        if status['last_post_time']:
            try:
                last_post = datetime.fromisoformat(status['last_post_time'])
                time_since_last = (now - last_post).total_seconds()
                
                if time_since_last < self.min_post_interval:
                    hours_remaining = (self.min_post_interval - time_since_last) / 3600
                    return False, f"Too soon - wait {hours_remaining:.1f} more hours"
            except:
                pass
        
        # Intelligent timing based on posts completed today
        if status['daily_posts'] == 1:
            # Second post - prefer afternoon (2-4 PM)
            if 14 <= current_hour <= 16:
                return True, "Optimal time for second post (afternoon)"
            elif current_hour >= 12:
                # After noon, use probability
                probability = 0.3 + (current_hour - 12) * 0.1  # Increases after noon
                should_post = random.random() < probability
                return should_post, f"Afternoon probability: {probability:.1%}"
            else:
                return False, "Too early for second post"
        
        elif status['daily_posts'] == 2:
            # Third post - prefer evening (7-9 PM)
            if 19 <= current_hour <= 21:
                return True, "Optimal time for third post (evening)"
            elif current_hour >= 17:
                # After 5 PM, use probability
                probability = 0.2 + (current_hour - 17) * 0.15  # Increases after 5 PM
                should_post = random.random() < probability
                return should_post, f"Evening probability: {probability:.1%}"
            else:
                return False, "Too early for third post"
        
        return False, "Unknown state"
    
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
                status['daily_posts'] += 1
                status['consecutive_failures'] = 0
                print(f"📊 Daily progress: {status['daily_posts']}/{self.posts_per_day} posts")
            else:
                print(f"❌ Bot run failed: {result_msg}")
                status['consecutive_failures'] += 1
        else:
            print("⏳ Not posting this time")
        
        # Update status
        status['last_check_time'] = now.isoformat()
        self.save_status(status)
        
        # Show summary
        print(f"📊 Summary: {status['total_posts']} total posts, {status.get('daily_posts', 0)}/{self.posts_per_day} today, {status['consecutive_failures']} consecutive failures")
    
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
    
    def get_missed_posts_today(self, status):
        """Check what posts we've missed today based on optimal hours"""
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        current_hour = now.hour
        
        # Reset daily counter if new day
        if status.get('last_post_date') != current_date:
            status['daily_posts'] = 0
            status['last_post_date'] = current_date
            status['posts_completed_hours'] = []
        
        if 'posts_completed_hours' not in status:
            status['posts_completed_hours'] = []
        
        missed_opportunities = []
        tolerance_hours = 2  # Can post up to 2 hours late
        
        for target_hour in self.optimal_hours:
            # Check if we missed this posting window
            if current_hour >= (target_hour + tolerance_hours):
                # We're past the tolerance window
                if target_hour not in status['posts_completed_hours']:
                    missed_opportunities.append(target_hour)
            elif current_hour >= target_hour:
                # We're in the posting window
                if target_hour not in status['posts_completed_hours']:
                    missed_opportunities.append(target_hour)
        
        return missed_opportunities
    
    def run_startup_catchup(self):
        """Run catch-up when computer starts up"""
        print("🖥️ COMPUTER STARTUP - CATCH-UP MODE")
        print("=" * 50)
        
        status = self.load_status()
        missed_posts = self.get_missed_posts_today(status)
        
        print(f"📊 Posts completed today: {status.get('posts_completed_hours', [])}")
        print(f"🎯 Missed opportunities: {missed_posts}")
        print(f"⏰ Current time: {datetime.now().strftime('%H:%M')}")
        
        if missed_posts:
            print(f"🚀 Executing {len(missed_posts)} missed posts...")
            
            successful_posts = 0
            for i, target_hour in enumerate(missed_posts):
                print(f"\n📍 Catching up post {i+1}/{len(missed_posts)} (missed {target_hour}:00)")
                
                success, result_msg = self.trigger_bot_run()
                
                if success:
                    print(f"✅ Success: {result_msg}")
                    status['posts_completed_hours'].append(target_hour)
                    status['daily_posts'] += 1
                    status['total_posts'] += 1
                    status['last_post_time'] = datetime.now().isoformat()
                    successful_posts += 1
                    
                    # Space out multiple posts (2 minutes)
                    if i < len(missed_posts) - 1:
                        print("⏱️ Waiting 2 minutes before next post...")
                        time.sleep(120)
                else:
                    print(f"❌ Failed: {result_msg}")
                    break
            
            print(f"\n🎉 Catch-up completed: {successful_posts}/{len(missed_posts)} posts successful")
        else:
            print("✅ No missed posts - all caught up!")
        
        # Save status
        self.save_status(status)
        
        # Show final summary
        current_posts = len(status.get('posts_completed_hours', []))
        print(f"\n📊 Daily summary: {current_posts}/3 posts completed today")
        print(f"🏆 Total posts: {status.get('total_posts', 0)}")
    
    def run_once(self):
        """Run single check (for testing)"""
        print("🧪 Running single smart check...")
        self.run_smart_check()
        print("✅ Single check completed")

if __name__ == "__main__":
    import sys
    
    launcher = SmartAutoLauncher()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--once":
            launcher.run_once()
        elif sys.argv[1] == "--startup":
            launcher.run_startup_catchup()
        elif sys.argv[1] == "--catchup":
            launcher.run_startup_catchup()
        else:
            print("Usage: python3 smart_auto_launcher.py [--once|--startup|--catchup]")
            print("  --once: Single check")
            print("  --startup: Catch-up mode for computer startup")
            print("  --catchup: Manual catch-up mode")
            print("  (no args): Continuous monitoring")
    else:
        launcher.run_continuous()