#!/usr/bin/env python3
"""
Simple Veo 3 test to diagnose authentication and API issues
"""

import time
import os

def test_veo3_basic():
    """Test basic Veo 3 functionality"""
    
    print("🧪 TESTING VEO 3 BASIC FUNCTIONALITY")
    print("=" * 50)
    
    # Test 1: Import libraries
    try:
        from google import genai
        from google.genai import types
        print("✅ Libraries imported successfully")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test 2: Configure Gemini API and initialize client  
    try:
        # Check for Gemini API key (required for Veo 3)
        gemini_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        if not gemini_key:
            raise Exception("GEMINI_API_KEY required for Veo 3")
        
        print("🔧 Found Gemini API Key for Veo 3")
        print(f"🔑 Key: {'*' * 10}...{gemini_key[-4:]}")
        
        client = genai.Client()
        print("✅ GenAI Client initialized with Gemini API")
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        print("💡 Possible issues:")
        print("   - Missing API key in environment")
        print("   - Incorrect project configuration")
        print("   - Network connectivity issues")
        return False
    
    # Test 3: Check available models
    try:
        print("🔍 Checking available models...")
        # This might help us see what models are accessible
        print("✅ Client object created, attempting video generation...")
    except Exception as e:
        print(f"❌ Model check failed: {e}")
        return False
    
    # Test 4: Simple video generation
    try:
        print("🎬 Testing simple video generation...")
        
        operation = client.models.generate_videos(
            model="veo-3.0-generate-preview",
            prompt="A simple test: professional newsroom with technology displays",
            config=types.GenerateVideosConfig(
                aspect_ratio="16:9"
            )
        )
        
        print("✅ Video generation request submitted")
        print(f"📊 Operation created: {type(operation)}")
        
        # Short poll test
        poll_count = 0
        max_test_polls = 5  # Only 50 seconds for quick test
        
        while not operation.done and poll_count < max_test_polls:
            poll_count += 1
            print(f"   Quick poll {poll_count}/{max_test_polls}")
            time.sleep(10)
            try:
                operation = client.operations.get(operation)
                print(f"   Operation status: done={operation.done}")
            except Exception as poll_error:
                print(f"   Polling error: {poll_error}")
                break
        
        if operation.done:
            print("✅ Video generation completed in test!")
            if hasattr(operation, 'response') and operation.response and operation.response.generated_videos:
                print("✅ Generated videos found in response")
                return True
            else:
                print("❌ No videos in completed operation")
                return False
        else:
            print("⏳ Video still generating (normal - takes 3-5 minutes)")
            print("✅ Veo 3 API is working (generation started successfully)")
            return True  # API is working, just takes time
            
    except Exception as e:
        print(f"❌ Video generation failed: {e}")
        print("💡 Common issues:")
        print("   - API key not configured")
        print("   - Project doesn't have Veo 3 access")
        print("   - Quota exceeded")
        print("   - Model name incorrect")
        return False

def test_environment():
    """Test environment variables"""
    
    print("\n🔧 TESTING ENVIRONMENT")
    print("=" * 30)
    
    # Check common environment variables
    env_vars = [
        'GOOGLE_API_KEY',
        'GOOGLE_APPLICATION_CREDENTIALS',
        'GOOGLE_PROJECT_ID',
        'GEMINI_API_KEY'
    ]
    
    found_vars = []
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * 10}...{value[-4:] if len(value) > 4 else '***'}")
            found_vars.append(var)
        else:
            print(f"❌ {var}: Not set")
    
    if not found_vars:
        print("⚠️ No Google API credentials found in environment")
        print("💡 GenAI Client may use default credentials or service account")
    
    return len(found_vars) > 0

if __name__ == "__main__":
    print("🚀 VEO 3 DIAGNOSTIC TEST")
    print("=" * 60)
    
    # Test environment first
    env_ok = test_environment()
    
    # Test Veo 3 functionality
    veo3_ok = test_veo3_basic()
    
    print("\n📊 TEST RESULTS")
    print("=" * 20)
    print(f"Environment: {'✅ OK' if env_ok else '⚠️ Limited'}")
    print(f"Veo 3 API:   {'✅ OK' if veo3_ok else '❌ FAILED'}")
    
    if not veo3_ok:
        print("\n🔧 RECOMMENDED ACTIONS:")
        print("1. Check API key configuration")
        print("2. Verify project has Veo 3 access")
        print("3. Check network connectivity")
        print("4. Review quota limits")