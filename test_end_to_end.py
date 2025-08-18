#!/usr/bin/env python3
"""
End-to-End Testing Suite for Multi-Platform AI Education System
Tests the complete 16-channel automation pipeline
"""

import os
import sys
import time
import json
from datetime import datetime
import subprocess

def test_dependencies():
    """Test all required Python dependencies"""
    print("📦 Testing Python dependencies...")
    
    required_packages = [
        'requests',
        'google-cloud-language',
        'praw'  # For Reddit integration
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}: Available")
        except ImportError:
            print(f"❌ {package}: Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n🔧 Install missing packages: pip install {' '.join(missing_packages)}")
        return False
    
    return True

def test_environment_variables():
    """Test if all required environment variables are set"""
    print("\n🔧 Testing environment variables...")
    
    required_vars = [
        # Telegram tokens
        'TELEGRAM_LEGAL_TOKEN', 'TELEGRAM_MEDICAL_TOKEN', 
        'TELEGRAM_SENIOR_TOKEN', 'TELEGRAM_GENERAL_TOKEN',
        # Ko-fi webhooks
        'KOFI_LEGAL_API', 'KOFI_MEDICAL_API', 
        'KOFI_SENIOR_API', 'KOFI_GENERAL_API',
        # ConvertKit
        'CONVERTKIT_API_KEY', 'CONVERTKIT_LEGAL_FORM', 
        'CONVERTKIT_MEDICAL_FORM', 'CONVERTKIT_SENIOR_FORM', 'CONVERTKIT_GENERAL_FORM',
        # Gumroad
        'GUMROAD_API_KEY', 'GUMROAD_LEGAL_ID', 
        'GUMROAD_MEDICAL_ID', 'GUMROAD_SENIOR_ID', 'GUMROAD_GENERAL_ID',
        # Google Cloud
        'GOOGLE_CLOUD_CREDENTIALS', 'GOOGLE_PROJECT_ID',
        # General
        'EMAIL_CONTACT', 'INSTAGRAM_CONSULTING'
    ]
    
    missing_vars = []
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Missing")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n🚨 {len(missing_vars)} environment variables missing!")
        print("📋 Run: export VARIABLE_NAME='your_value' for each missing variable")
        return False
    
    return True

def test_infinite_content_engine():
    """Test the infinite content engine"""
    print("\n🎭 Testing Infinite Content Engine...")
    
    try:
        from infinite_content_engine import InfiniteContentEngine
        
        engine = InfiniteContentEngine()
        content = engine.generate_infinite_content()
        
        if content:
            title, body = content
            print(f"✅ Content generated: '{title[:50]}...'")
            print(f"📝 Content length: {len(body)} characters")
            return True
        else:
            print("❌ Content generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Content engine error: {e}")
        return False

def test_multi_platform_engine():
    """Test the multi-platform publishing engine"""
    print("\n🚀 Testing Multi-Platform Engine...")
    
    try:
        from multi_platform_engine import MultiPlatformEngine
        
        engine = MultiPlatformEngine()
        print("✅ Multi-Platform Engine initialized")
        
        # Test content classification
        test_content = "This AI tool helps lawyers automate legal document review and contract analysis."
        industry, confidence = engine.classify_content_industry(test_content)
        print(f"✅ Content classified as: {industry} (confidence: {confidence})")
        
        # Test content adaptation
        adapted = engine.adapt_content_for_industry(test_content, industry, "telegram")
        print(f"✅ Content adapted for {industry}/telegram: {len(adapted)} chars")
        
        return True
        
    except Exception as e:
        print(f"❌ Multi-Platform Engine error: {e}")
        return False

def test_api_integrations():
    """Test API integrations with mock data"""
    print("\n🔌 Testing API integrations...")
    
    try:
        from multi_platform_engine import MultiPlatformEngine
        
        engine = MultiPlatformEngine()
        test_content = "🧠 AI Education Test: This is a test message for API validation."
        
        # Test each platform with legal industry
        test_industry = "legal"
        
        print(f"📡 Testing {test_industry} industry APIs...")
        
        # Test Telegram (should work if token is valid)
        try:
            result = engine.publish_to_telegram(test_industry, test_content)
            print(f"✅ Telegram {test_industry}: {'Success' if result else 'Failed'}")
        except Exception as e:
            print(f"⚠️ Telegram {test_industry}: {e}")
        
        # Test other platforms (will validate credentials and endpoints)
        platforms = ["kofi", "convertkit", "gumroad"]
        for platform in platforms:
            try:
                if platform == "kofi":
                    result = engine.publish_to_kofi(test_industry, test_content)
                elif platform == "convertkit":
                    result = engine.publish_to_convertkit(test_industry, test_content)
                elif platform == "gumroad":
                    result = engine.publish_to_gumroad(test_industry, test_content)
                
                print(f"✅ {platform.title()} {test_industry}: {'Success' if result else 'Failed'}")
            except Exception as e:
                print(f"⚠️ {platform.title()} {test_industry}: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ API integration test error: {e}")
        return False

def test_github_actions_workflow():
    """Test GitHub Actions workflow structure"""
    print("\n⚙️ Testing GitHub Actions workflow...")
    
    workflow_path = "/Volumes/DiskExFAT 1/reddit_ai_bot_production/.github/workflows/multi_platform_publishing.yml"
    
    if os.path.exists(workflow_path):
        print("✅ GitHub Actions workflow file exists")
        
        try:
            with open(workflow_path, 'r') as f:
                workflow_content = f.read()
            
            # Check for required sections
            required_sections = [
                'Multi-Platform AI Education Publishing System',
                'TELEGRAM_LEGAL_TOKEN',
                'CONVERTKIT_API_KEY',
                'GUMROAD_API_KEY',
                'multi_platform_engine.py'
            ]
            
            all_sections_found = True
            for section in required_sections:
                if section in workflow_content:
                    print(f"✅ Workflow contains: {section}")
                else:
                    print(f"❌ Workflow missing: {section}")
                    all_sections_found = False
            
            return all_sections_found
            
        except Exception as e:
            print(f"❌ Error reading workflow: {e}")
            return False
    else:
        print("❌ GitHub Actions workflow file not found")
        return False

def test_credentials_validator():
    """Test the credentials validator"""
    print("\n🔐 Testing credentials validator...")
    
    try:
        # Run the credential validator
        result = subprocess.run(
            [sys.executable, "validate_credentials.py"],
            cwd="/Volumes/DiskExFAT 1/reddit_ai_bot_production",
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ Credential validation passed")
            return True
        else:
            print("⚠️ Some credential validations failed")
            print("📋 Run 'python validate_credentials.py' for details")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️ Credential validation timed out (may indicate API issues)")
        return False
    except Exception as e:
        print(f"❌ Credential validation error: {e}")
        return False

def simulate_full_publishing_cycle():
    """Simulate a complete publishing cycle"""
    print("\n🎯 Simulating full publishing cycle...")
    
    try:
        from multi_platform_engine import MultiPlatformEngine
        
        engine = MultiPlatformEngine()
        
        # Generate content
        print("📝 Generating content...")
        publications = engine.run_daily_publishing_cycle()
        
        if publications > 0:
            print(f"✅ Publishing cycle completed: {publications} publications")
            return True
        else:
            print("⚠️ Publishing cycle completed but no publications succeeded")
            return False
            
    except Exception as e:
        print(f"❌ Publishing cycle simulation error: {e}")
        return False

def calculate_system_readiness():
    """Calculate overall system readiness percentage"""
    print("\n" + "="*60)
    print("🏁 SYSTEM READINESS ASSESSMENT")
    print("="*60)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Environment Variables", test_environment_variables),
        ("Content Engine", test_infinite_content_engine),
        ("Multi-Platform Engine", test_multi_platform_engine),
        ("API Integrations", test_api_integrations),
        ("GitHub Actions", test_github_actions_workflow),
        ("Credential Validation", test_credentials_validator),
        ("Full Cycle Simulation", simulate_full_publishing_cycle)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Calculate readiness
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    readiness_percentage = (passed_tests / total_tests) * 100
    
    print("\n" + "="*60)
    print("📊 FINAL RESULTS")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
    
    print(f"\n🎯 System Readiness: {readiness_percentage:.1f}% ({passed_tests}/{total_tests} tests passed)")
    
    if readiness_percentage >= 90:
        print("🚀 EXCELLENT: System ready for production deployment!")
    elif readiness_percentage >= 70:
        print("✅ GOOD: System mostly ready, minor fixes needed")
    elif readiness_percentage >= 50:
        print("⚠️ MODERATE: System needs significant configuration")
    else:
        print("❌ CRITICAL: System requires major fixes before deployment")
    
    # Deployment recommendation
    print("\n🔧 NEXT STEPS:")
    if readiness_percentage >= 80:
        print("1. ✅ Configure remaining credentials if any")
        print("2. ✅ Test with GitHub Actions manual trigger")
        print("3. ✅ Monitor automated publishing (3x daily)")
        print("4. ✅ Scale to additional industries/platforms")
    else:
        failed_tests = [name for name, result in results.items() if not result]
        print("1. 🔧 Fix failed components:")
        for failed_test in failed_tests:
            print(f"   - {failed_test}")
        print("2. 🔧 Re-run end-to-end testing")
        print("3. 🔧 Verify credentials setup guide")
    
    return readiness_percentage

def main():
    """Run complete end-to-end testing suite"""
    print("🧪 MULTI-PLATFORM AI EDUCATION SYSTEM")
    print("🧪 END-TO-END TESTING SUITE")
    print("="*60)
    print(f"📅 Test execution: {datetime.now()}")
    print(f"📂 Working directory: {os.getcwd()}")
    print()
    
    readiness = calculate_system_readiness()
    
    print(f"\n⏱️ Testing completed at: {datetime.now()}")
    
    # Exit with appropriate code
    if readiness >= 80:
        exit(0)  # Success
    else:
        exit(1)  # Failure

if __name__ == "__main__":
    main()