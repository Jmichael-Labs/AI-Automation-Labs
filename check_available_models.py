#!/usr/bin/env python3
"""
Check what models are actually available in Gemini API
"""

import os
from google import genai

def check_available_models():
    """Check what models are available in Gemini API"""
    
    print("🔍 CHECKING AVAILABLE MODELS IN GEMINI API")
    print("=" * 50)
    
    try:
        # Check API key
        gemini_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        if not gemini_key:
            print("❌ No GEMINI_API_KEY found")
            return
        
        print(f"✅ API Key: {'*' * 10}...{gemini_key[-4:]}")
        
        # Initialize client
        client = genai.Client()
        print("✅ Client initialized")
        
        # Try to list models
        print("\n📋 ATTEMPTING TO LIST MODELS...")
        
        try:
            # Method 1: Direct model listing (if available)
            models = client.models.list()
            print(f"✅ Found {len(models)} models:")
            for model in models:
                print(f"   - {model.name}")
                if "veo" in model.name.lower():
                    print(f"     🎥 VIDEO MODEL FOUND: {model.name}")
        except Exception as e:
            print(f"⚠️ Model listing failed: {e}")
            
        # Method 2: Test specific Veo models
        print("\n🎬 TESTING SPECIFIC VEO MODELS...")
        
        veo_models_to_test = [
            "veo-3.0-generate-preview",
            "veo-3-generate-preview", 
            "veo-3.0-fast-generate-001",
            "veo-3-fast",
            "veo",
            "veo-2",
            "video-generation"
        ]
        
        for model_name in veo_models_to_test:
            try:
                print(f"🧪 Testing model: {model_name}")
                
                # Try to create a generation request (without waiting)
                operation = client.models.generate_videos(
                    model=model_name,
                    prompt="test video",
                    config=genai.types.GenerateVideosConfig(
                        aspect_ratio="16:9"
                    )
                )
                print(f"✅ {model_name}: REQUEST SUCCESSFUL")
                print(f"   Operation type: {type(operation)}")
                
                # Don't wait for completion, just check if request was accepted
                break
                
            except Exception as e:
                print(f"❌ {model_name}: {str(e)[:100]}...")
                
        print("\n🎯 TESTING ALTERNATIVE APPROACHES...")
        
        # Test if text generation works (to confirm API key is valid)
        try:
            text_response = client.models.generate_text(
                model="gemini-1.5-flash",
                prompt="Hello world"
            )
            print("✅ Text generation works - API key is valid")
        except Exception as e:
            print(f"❌ Text generation failed: {e}")
            
    except Exception as e:
        print(f"❌ General error: {e}")

if __name__ == "__main__":
    check_available_models()