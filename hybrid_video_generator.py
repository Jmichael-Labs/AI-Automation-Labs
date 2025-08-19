#!/usr/bin/env python3
"""
Hybrid Video Generator - GUARANTEED video generation
Always produces a video (Veo 3 real OR mock fallback)
"""

import time
import os
import subprocess
from datetime import datetime

def create_mock_video(segment_prompt, segment_number, industry):
    """Create a mock video as fallback - GUARANTEED to work"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mock_filename = f"/tmp/mock_newsroom_segment_{segment_number}_{industry}_{timestamp}.mp4"
    
    # Create a simple mock video (black screen with text)
    try:
        # Extract key info from prompt for overlay text
        segment_title = f"Segment {segment_number}: AI News Update"
        
        mock_cmd = [
            "ffmpeg", "-f", "lavfi",
            "-i", f"color=c=black:s=1280x720:d=8:r=30",
            "-vf", f"drawtext=text='{segment_title}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2",
            "-c:v", "libx264", "-t", "8", "-pix_fmt", "yuv420p", "-y",
            mock_filename
        ]
        
        result = subprocess.run(mock_cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(mock_filename):
            file_size = os.path.getsize(mock_filename)
            print(f"✅ MOCK VIDEO created successfully!")
            print(f"📁 File: {mock_filename}")
            print(f"📊 File size: {file_size} bytes")
            print(f"⏱️ Duration: 8 seconds (Mock)")
            
            return {
                "segment_number": segment_number,
                "file_path": mock_filename,
                "file_size": file_size,
                "source": "mock_fallback"
            }
        else:
            print(f"❌ Mock video creation failed: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Mock video creation error: {e}")
        return None

def generate_guaranteed_video_segment(segment_prompt, segment_number, industry):
    """Generate video with guaranteed fallback - NEVER fails completely"""
    
    print(f"🎬 HYBRID VIDEO GENERATION - Segment {segment_number}")
    print(f"🎯 Strategy: Veo 3 first, Mock fallback if needed")
    
    # STEP 1: Try Veo 3 real generation
    try:
        from google import genai
        from google.genai import types
        
        print(f"🚀 Attempting Veo 3 generation...")
        
        # Initialize GenAI client
        client = genai.Client()
        
        # Generate video with Veo 3
        operation = client.models.generate_videos(
            model="veo-3.0-generate-preview",
            prompt=segment_prompt,
            config=types.GenerateVideosConfig(
                aspect_ratio="16:9"
            )
        )
        
        # Poll for completion (shorter timeout for faster fallback)
        print(f"⏳ Polling Veo 3 generation (max 3 minutes)...")
        poll_count = 0
        max_polls = 18  # 3 minutes (18 * 10s = 180s)
        
        while not operation.done and poll_count < max_polls:
            poll_count += 1
            print(f"   Polling {poll_count}/{max_polls}")
            time.sleep(10)
            operation = client.operations.get(operation)
        
        # Check if Veo 3 succeeded
        if operation.done and operation.response and operation.response.generated_videos:
            # Save the real video
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_filename = f"/tmp/veo3_segment_{segment_number}_{industry}_{timestamp}.mp4"
            
            generated_video = operation.response.generated_videos[0]
            client.files.download(file=generated_video.video)
            generated_video.video.save(video_filename)
            
            if os.path.exists(video_filename):
                file_size = os.path.getsize(video_filename)
                print(f"🎥 VEO 3 REAL VIDEO successfully generated!")
                print(f"📁 File: {video_filename}")
                print(f"📊 File size: {file_size} bytes")
                
                return {
                    "segment_number": segment_number,
                    "file_path": video_filename,
                    "file_size": file_size,
                    "source": "veo3_real"
                }
        
        print(f"⚠️ Veo 3 failed or timed out - falling back to mock")
        
    except Exception as e:
        print(f"⚠️ Veo 3 error: {e}")
        print(f"🔄 Falling back to mock video generation...")
    
    # STEP 2: Create mock video (GUARANTEED fallback)
    return create_mock_video(segment_prompt, segment_number, industry)

if __name__ == "__main__":
    # Test the function
    test_prompt = "A professional futuristic newsroom with AI graphics and technology displays"
    result = generate_guaranteed_video_segment(test_prompt, 1, "test")
    if result:
        print(f"✅ SUCCESS: {result}")
    else:
        print("❌ COMPLETE FAILURE - This should never happen")