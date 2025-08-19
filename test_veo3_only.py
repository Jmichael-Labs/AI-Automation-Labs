#!/usr/bin/env python3
"""
Test script to specifically test Veo 3 video generation
"""
import os
from visual_content_engine import VisualContentEngine

def test_veo3_video_generation():
    print("🧪 TESTING VEO 3 VIDEO GENERATION SPECIFICALLY")
    print("=" * 60)
    
    # Initialize engine
    engine = VisualContentEngine()
    
    # Check Veo 3 status
    print(f"✅ Veo3 Client Available: {engine.veo3_client is not None}")
    print(f"✅ Video Model: {engine.video_model}")
    print(f"✅ GEMINI_API_KEY Set: {'GEMINI_API_KEY' in os.environ}")
    
    if engine.veo3_client and engine.video_model:
        print("\n🎬 ATTEMPTING VIDEO GENERATION...")
        
        # Create test tool data
        test_tool = {
            "name": "TestAI",
            "description": "Test AI tool for video generation",
            "category": "automation",
            "use_case": "Test video creation",
            "income_potential": "$1,000/month"
        }
        
        # Try to generate a video segment
        try:
            video_path = engine.generate_futuristic_newsroom_segments(test_tool, "general", "test script")
            if video_path:
                print(f"🎥 SUCCESS! Video generated: {video_path}")
                
                # Check if file exists and has content
                if os.path.exists(video_path):
                    file_size = os.path.getsize(video_path)
                    print(f"📁 File size: {file_size} bytes")
                    print(f"📝 File type: {video_path.split('.')[-1]}")
                else:
                    print("⚠️ Video file not found on disk")
            else:
                print("❌ Video generation returned None")
        except Exception as e:
            print(f"❌ Video generation failed: {e}")
    else:
        print("⚠️ Veo 3 not available - check GEMINI_API_KEY configuration")

if __name__ == "__main__":
    test_veo3_video_generation()