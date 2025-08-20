#!/usr/bin/env python3
"""
Smart Video Generator - Detects available models and creates best possible content
"""

import os
import subprocess
import time
from datetime import datetime
from google import genai

def check_veo_availability():
    """Check if any Veo models are actually available"""
    
    try:
        gemini_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        if not gemini_key:
            return False, "No GEMINI_API_KEY"
        
        client = genai.Client()
        
        # Test different Veo model names that might exist
        possible_models = [
            "veo-3.0-generate-preview",
            "veo-3-generate-preview", 
            "veo-2",
            "veo",
            "video-generation"
        ]
        
        for model in possible_models:
            try:
                # Just try to create request - don't wait for result
                operation = client.models.generate_videos(
                    model=model,
                    prompt="test",
                    config=genai.types.GenerateVideosConfig(aspect_ratio="16:9")
                )
                return True, f"Found working model: {model}"
            except Exception as e:
                error_msg = str(e)
                if "not found" not in error_msg.lower() and "supported" not in error_msg.lower():
                    # If error is not "model not found", the model exists but has other issues
                    return True, f"Model {model} exists but: {error_msg[:50]}"
                    
        return False, "No Veo models available in Gemini API"
        
    except Exception as e:
        return False, f"API check failed: {e}"

def create_professional_mock_video(segment_prompt, segment_number, industry, tool_name):
    """Create a professional-looking mock video with realistic AI newsroom content"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mock_filename = f"/tmp/ai_news_segment_{segment_number}_{industry}_{timestamp}.mp4"
    
    # Create realistic newsroom-style content based on segment
    newsroom_segments = {
        1: {
            "title": f"🚀 AI BREAKTHROUGH", 
            "subtitle": f"{tool_name} Revolutionizes {industry.title()}",
            "ticker": "BREAKING: New AI Innovation Transforms Industry"
        },
        2: {
            "title": f"🔍 EXPERT ANALYSIS",
            "subtitle": f"Market Impact of {tool_name}",
            "ticker": "ANALYSIS: 47% Productivity Increase Reported"
        },
        3: {
            "title": f"💡 FUTURE OUTLOOK", 
            "subtitle": f"Next Generation AI in {industry.title()}",
            "ticker": "OUTLOOK: AI Adoption Accelerates Globally"
        }
    }
    
    segment_info = newsroom_segments.get(segment_number, {
        "title": f"AI UPDATE {segment_number}",
        "subtitle": f"{tool_name} Latest",
        "ticker": "AI News Update"
    })
    
    try:
        # Create professional newsroom-style mock video
        ffmpeg_cmd = [
            "ffmpeg", "-f", "lavfi",
            # Create dark blue gradient background like real newsroom
            "-i", "color=c=0x0a1428:s=1280x720:d=8:r=30",
            "-vf", 
            # Multi-layer text overlay like real news
            (f"drawtext=text='{segment_info['title']}':fontcolor=white:fontsize=52:x=(w-text_w)/2:y=150:fontfile=/System/Library/Fonts/Helvetica.ttc,"
             f"drawtext=text='{segment_info['subtitle']}':fontcolor=0xaaaaaa:fontsize=32:x=(w-text_w)/2:y=220:fontfile=/System/Library/Fonts/Helvetica.ttc,"
             f"drawtext=text='{segment_info['ticker']}':fontcolor=0x4a90ff:fontsize=24:x=50:y=650:fontfile=/System/Library/Fonts/Helvetica.ttc,"
             f"drawtext=text='LIVE':fontcolor=red:fontsize=20:x=50:y=50:fontfile=/System/Library/Fonts/Helvetica.ttc,"
             f"drawtext=text='AI NEWS NETWORK':fontcolor=white:fontsize=18:x=120:y=55:fontfile=/System/Library/Fonts/Helvetica.ttc,"
             # Add timestamp
             f"drawtext=text='{datetime.now().strftime('%H:%M UTC')}':fontcolor=0x888888:fontsize=16:x=w-150:y=50:fontfile=/System/Library/Fonts/Helvetica.ttc"),
            "-c:v", "libx264", "-t", "8", "-pix_fmt", "yuv420p", "-y",
            mock_filename
        ]
        
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(mock_filename):
            file_size = os.path.getsize(mock_filename)
            print(f"🎥 PROFESSIONAL MOCK VIDEO created!")
            print(f"📁 File: {mock_filename}")
            print(f"📊 File size: {file_size} bytes")
            print(f"🎬 Style: Professional AI newsroom")
            print(f"📺 Content: {segment_info['title']} - {segment_info['subtitle']}")
            
            return {
                "segment_number": segment_number,
                "file_path": mock_filename,
                "file_size": file_size,
                "source": "professional_mock"
            }
        else:
            print(f"❌ Professional mock creation failed: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Professional mock error: {e}")
        return None

def generate_smart_video_segment(segment_prompt, segment_number, industry, tool_name="AI Tool"):
    """Smart video generation - tries Veo 3, falls back to professional mock"""
    
    print(f"🧠 SMART VIDEO GENERATION - Segment {segment_number}")
    
    # Step 1: Check if Veo is available
    veo_available, veo_status = check_veo_availability()
    print(f"🔍 Veo availability: {veo_status}")
    
    if veo_available:
        print("🚀 Veo models detected - attempting real generation...")
        
        try:
            client = genai.Client()
            
            # Try the most likely working model
            operation = client.models.generate_videos(
                model="veo-3.0-generate-preview",  # Try this first
                prompt=segment_prompt,
                config=genai.types.GenerateVideosConfig(aspect_ratio="16:9")
            )
            
            print("⏳ Waiting for Veo generation (max 3 minutes)...")
            poll_count = 0
            max_polls = 18
            
            while not operation.done and poll_count < max_polls:
                poll_count += 1
                time.sleep(10)
                operation = client.operations.get(operation)
            
            if operation.done and operation.response and operation.response.generated_videos:
                # Save real video
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                video_filename = f"/tmp/veo_real_{segment_number}_{industry}_{timestamp}.mp4"
                
                generated_video = operation.response.generated_videos[0]
                client.files.download(file=generated_video.video)
                generated_video.video.save(video_filename)
                
                if os.path.exists(video_filename):
                    file_size = os.path.getsize(video_filename)
                    print(f"🎥 REAL VEO VIDEO successfully generated!")
                    
                    return {
                        "segment_number": segment_number,
                        "file_path": video_filename,
                        "file_size": file_size,
                        "source": "veo_real"
                    }
            
            print("⚠️ Veo generation failed or timed out")
            
        except Exception as e:
            print(f"⚠️ Veo error: {e}")
    
    # Step 2: Create professional mock as fallback
    print("🎬 Creating professional mock video...")
    return create_professional_mock_video(segment_prompt, segment_number, industry, tool_name)

if __name__ == "__main__":
    # Test the smart generator
    result = generate_smart_video_segment(
        "A futuristic AI newsroom with holographic displays", 
        1, 
        "technology", 
        "TestTool"
    )
    if result:
        print(f"✅ SUCCESS: {result}")
    else:
        print("❌ FAILED to generate any video")