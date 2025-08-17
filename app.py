#!/usr/bin/env python3
"""
Reddit AI Bot - Render.com Web Service
Exposes /run endpoint for external cron triggers
"""

from flask import Flask, jsonify, request
import os
import threading
import time
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Import our NEW AI News Poster bot
try:
    from ai_news_poster import AINewsPoster
except ImportError:
    logger.error("Could not import AI News Poster - check dependencies")
    AINewsPoster = None

# Global bot instance
bot_instance = None
last_run_time = None
run_count = 0

def initialize_bot():
    """Initialize AI News Poster bot"""
    global bot_instance
    
    if AINewsPoster and not bot_instance:
        try:
            bot_instance = AINewsPoster()
            logger.info("✅ AI News Poster initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize AI News Poster: {e}")
            bot_instance = None
    
    return bot_instance is not None

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "JMichael Labs AI News Poster",
        "version": "2.0",
        "last_run": last_run_time.isoformat() if last_run_time else None,
        "total_runs": run_count,
        "target_subreddit": "r/AIAutomationLabs",
        "bot_initialized": bot_instance is not None
    })

@app.route('/run', methods=['GET', 'POST'])
def run_bot():
    """Main endpoint to trigger bot execution"""
    global last_run_time, run_count
    
    start_time = datetime.now()
    
    try:
        # Initialize bot if needed
        if not initialize_bot():
            return jsonify({
                "error": "Bot initialization failed",
                "timestamp": start_time.isoformat()
            }), 500
        
        logger.info("🚀 Starting AI News Posting...")
        
        # Run daily posting
        posts_count = bot_instance.run_daily_posting()
        
        # Update tracking
        last_run_time = datetime.now()
        run_count += 1
        
        execution_time = (last_run_time - start_time).total_seconds()
        
        result = {
            "status": "success",
            "timestamp": last_run_time.isoformat(),
            "execution_time_seconds": execution_time,
            "posts_generated": posts_count,
            "total_runs": run_count,
            "daily_posts": bot_instance.posts_today if bot_instance else 0,
            "max_daily": bot_instance.max_daily_posts if bot_instance else 0,
            "target_subreddit": "r/AIAutomationLabs"
        }
        
        logger.info(f"✅ AI News Posting completed: {posts_count} posts in {execution_time:.1f}s")
        return jsonify(result)
        
    except Exception as e:
        error_result = {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "total_runs": run_count
        }
        
        logger.error(f"❌ Bot run failed: {e}")
        return jsonify(error_result), 500

@app.route('/stats')
def get_stats():
    """Get bot statistics"""
    return jsonify({
        "bot_status": "initialized" if bot_instance else "not_initialized",
        "last_run": last_run_time.isoformat() if last_run_time else None,
        "total_runs": run_count,
        "daily_responses": bot_instance.daily_responses if bot_instance else 0,
        "max_daily_responses": bot_instance.max_daily_responses if bot_instance else 0,
        "target_subreddits": bot_instance.TARGET_SUBREDDITS if bot_instance else [],
        "uptime": datetime.now().isoformat()
    })

@app.route('/test')
def test_connection():
    """Test Reddit connection without running full scan"""
    try:
        if not initialize_bot():
            return jsonify({"error": "Bot initialization failed"}), 500
        
        # Test connection
        connection_ok = bot_instance.test_connection()
        
        return jsonify({
            "reddit_connection": "success" if connection_ok else "failed",
            "timestamp": datetime.now().isoformat(),
            "user": "SwordfishMany6633",
            "contact": "jmichaeloficial@gmail.com"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

# Keep-alive endpoint for external monitoring
@app.route('/ping')
def ping():
    """Simple ping endpoint"""
    return jsonify({
        "pong": True,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/debug')
def debug_scan():
    """Debug endpoint to investigate why bot finds 0 opportunities"""
    try:
        if not initialize_bot():
            return jsonify({"error": "Bot initialization failed"}), 500
        
        # Test just one subreddit in detail
        subreddit_name = "ChatGPT"
        debug_info = {
            "subreddit": subreddit_name,
            "posts_found": 0,
            "posts_details": [],
            "memory_size": len(bot_instance.processed_posts),
            "daily_responses": bot_instance.daily_responses,
            "scan_limit": 10  # Just scan 10 for debugging
        }
        
        try:
            subreddit = bot_instance.reddit.subreddit(subreddit_name)
            
            for i, post in enumerate(subreddit.new(limit=10)):
                debug_info["posts_found"] += 1
                
                # Test AI detection
                ai_detected = bot_instance.detect_ai_problem(post)
                would_respond = bot_instance.should_respond_to_post(post)
                
                post_detail = {
                    "index": i + 1,
                    "id": post.id,
                    "title": post.title[:80] + "..." if len(post.title) > 80 else post.title,
                    "created_hours_ago": round((datetime.now() - datetime.fromtimestamp(post.created_utc)).total_seconds() / 3600, 1),
                    "num_comments": post.num_comments,
                    "ai_detected": ai_detected,
                    "would_respond": would_respond,
                    "already_processed": post.id in bot_instance.processed_posts
                }
                
                debug_info["posts_details"].append(post_detail)
                
        except Exception as e:
            debug_info["subreddit_error"] = str(e)
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Get port from environment (Render provides this)
    port = int(os.environ.get('PORT', 5000))
    
    # Run Flask app
    logger.info(f"🚀 Starting Reddit AI Bot Web Service on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)