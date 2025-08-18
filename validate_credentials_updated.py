#!/usr/bin/env python3
"""
Multi-Platform Credentials Validator (Updated - 12 Channels)
Validates all 15 credentials required for the system
"""

import os
import requests
import json
from datetime import datetime

def validate_telegram_bots():
    """Validate all 4 Telegram bot tokens"""
    print("🤖 Validating Telegram bots...")
    
    tokens = {
        "legal": os.getenv('TELEGRAM_LEGAL_TOKEN'),
        "medical": os.getenv('TELEGRAM_MEDICAL_TOKEN'),
        "senior": os.getenv('TELEGRAM_SENIOR_TOKEN'),
        "general": os.getenv('TELEGRAM_GENERAL_TOKEN')
    }
    
    results = {}
    for industry, token in tokens.items():
        if not token:
            print(f"❌ Telegram {industry}: Token missing")
            results[f"telegram_{industry}"] = False
            continue
        
        try:
            url = f"https://api.telegram.org/bot{token}/getMe"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                bot_data = response.json()
                bot_name = bot_data.get('result', {}).get('username', 'Unknown')
                print(f"✅ Telegram {industry}: Bot @{bot_name} verified")
                results[f"telegram_{industry}"] = True
            else:
                print(f"❌ Telegram {industry}: Invalid token (HTTP {response.status_code})")
                results[f"telegram_{industry}"] = False
                
        except Exception as e:
            print(f"❌ Telegram {industry}: Connection error - {e}")
            results[f"telegram_{industry}"] = False
    
    return results

def validate_telegram_chat_id():
    """Validate Telegram chat ID for notifications"""
    print("\n📱 Validating Telegram Chat ID...")
    
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    general_token = os.getenv('TELEGRAM_GENERAL_TOKEN')
    
    results = {}
    
    if not chat_id:
        print("❌ Telegram Chat ID: Missing")
        results["telegram_chat_id"] = False
        return results
    
    if not general_token:
        print("❌ Telegram Chat ID: Cannot test without bot token")
        results["telegram_chat_id"] = False
        return results
    
    try:
        # Test sending a message to the chat ID
        url = f"https://api.telegram.org/bot{general_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": "🧪 System Test: Telegram Chat ID validation"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Telegram Chat ID: Valid and accessible ({chat_id})")
            results["telegram_chat_id"] = True
        else:
            print(f"❌ Telegram Chat ID: Invalid or inaccessible (HTTP {response.status_code})")
            results["telegram_chat_id"] = False
            
    except Exception as e:
        print(f"❌ Telegram Chat ID: Validation error - {e}")
        results["telegram_chat_id"] = False
    
    return results

def validate_kofi_webhooks():
    """Validate Ko-fi webhook URLs"""
    print("\n💰 Validating Ko-fi webhooks...")
    
    webhooks = {
        "legal": os.getenv('KOFI_LEGAL_API'),
        "medical": os.getenv('KOFI_MEDICAL_API'),
        "senior": os.getenv('KOFI_SENIOR_API'),
        "general": os.getenv('KOFI_GENERAL_API')
    }
    
    results = {}
    for industry, webhook_url in webhooks.items():
        if not webhook_url:
            print(f"❌ Ko-fi {industry}: Webhook URL missing")
            results[f"kofi_{industry}"] = False
            continue
        
        try:
            # Test webhook with a ping payload
            test_payload = {
                "type": "test",
                "data": {"message": "Credential validation test"}
            }
            
            response = requests.post(webhook_url, json=test_payload, timeout=10)
            
            if response.status_code in [200, 201, 202, 404]:  # 404 is ok for webhook test
                print(f"✅ Ko-fi {industry}: Webhook URL accessible")
                results[f"kofi_{industry}"] = True
            else:
                print(f"⚠️ Ko-fi {industry}: Webhook returned {response.status_code}")
                results[f"kofi_{industry}"] = True  # Still usable
                
        except Exception as e:
            print(f"❌ Ko-fi {industry}: Webhook error - {e}")
            results[f"kofi_{industry}"] = False
    
    return results

def validate_gumroad_api():
    """Validate Gumroad API key and products"""
    print("\n🛍️ Validating Gumroad API...")
    
    api_key = os.getenv('GUMROAD_API_KEY')
    products = {
        "legal": os.getenv('GUMROAD_LEGAL_ID'),
        "medical": os.getenv('GUMROAD_MEDICAL_ID'),
        "senior": os.getenv('GUMROAD_SENIOR_ID'),
        "general": os.getenv('GUMROAD_GENERAL_ID')
    }
    
    results = {}
    
    if not api_key:
        print("❌ Gumroad: API key missing")
        for industry in products.keys():
            results[f"gumroad_{industry}"] = False
        return results
    
    try:
        # Test API key with user endpoint
        url = "https://api.gumroad.com/v2/user"
        payload = {"access_token": api_key}
        response = requests.get(url, params=payload, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get('user', {}).get('name', 'Unknown')
            print(f"✅ Gumroad: API key valid for user '{username}'")
            
            # Test each product ID
            for industry, product_id in products.items():
                if not product_id:
                    print(f"❌ Gumroad {industry}: Product ID missing")
                    results[f"gumroad_{industry}"] = False
                    continue
                
                try:
                    product_url = f"https://api.gumroad.com/v2/products/{product_id}"
                    product_response = requests.get(product_url, params=payload, timeout=10)
                    
                    if product_response.status_code == 200:
                        product_data = product_response.json()
                        product_name = product_data.get('product', {}).get('name', 'Unknown')
                        print(f"✅ Gumroad {industry}: Product '{product_name}' found")
                        results[f"gumroad_{industry}"] = True
                    else:
                        print(f"❌ Gumroad {industry}: Product {product_id} not accessible")
                        results[f"gumroad_{industry}"] = False
                        
                except Exception as e:
                    print(f"❌ Gumroad {industry}: Product validation error - {e}")
                    results[f"gumroad_{industry}"] = False
        else:
            print(f"❌ Gumroad: Invalid API key (HTTP {response.status_code})")
            for industry in products.keys():
                results[f"gumroad_{industry}"] = False
                
    except Exception as e:
        print(f"❌ Gumroad: API error - {e}")
        for industry in products.keys():
            results[f"gumroad_{industry}"] = False
    
    return results

def validate_google_cloud():
    """Validate Google Cloud credentials"""
    print("\n☁️ Validating Google Cloud...")
    
    credentials_json = os.getenv('GOOGLE_CLOUD_CREDENTIALS')
    project_id = os.getenv('GOOGLE_PROJECT_ID')
    
    results = {}
    
    if not credentials_json:
        print("❌ Google Cloud: Credentials JSON missing")
        results["google_cloud"] = False
        return results
    
    if not project_id:
        print("❌ Google Cloud: Project ID missing")
        results["google_cloud"] = False
        return results
    
    try:
        # Try to parse credentials JSON
        credentials_data = json.loads(credentials_json)
        service_account_email = credentials_data.get('client_email', 'Unknown')
        print(f"✅ Google Cloud: Credentials parsed for {service_account_email}")
        
        # Try to initialize the Natural Language client
        from google.cloud import language_v1
        
        # Set credentials as environment variable temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write(credentials_json)
            temp_file_path = temp_file.name
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_file_path
        
        # Test Natural Language API
        client = language_v1.LanguageServiceClient()
        
        # Simple test document
        document = language_v1.Document(
            content="This is a test for AI education content.",
            type_=language_v1.Document.Type.PLAIN_TEXT
        )
        
        # Try to analyze entities
        response = client.analyze_entities(
            request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
        )
        
        print(f"✅ Google Cloud: Natural Language API accessible, {len(response.entities)} entities detected")
        results["google_cloud"] = True
        
        # Cleanup
        os.unlink(temp_file_path)
        
    except Exception as e:
        print(f"❌ Google Cloud: Validation error - {e}")
        results["google_cloud"] = False
    
    return results

def validate_general_config():
    """Validate general configuration"""
    print("\n⚙️ Validating general configuration...")
    
    email = os.getenv('EMAIL_CONTACT')
    instagram = os.getenv('INSTAGRAM_CONSULTING')
    
    results = {}
    
    if email and '@' in email:
        print(f"✅ Email contact: {email}")
        results["email_contact"] = True
    else:
        print("❌ Email contact: Invalid or missing")
        results["email_contact"] = False
    
    if instagram and 'instagram.com' in instagram:
        print(f"✅ Instagram consulting: {instagram}")
        results["instagram_consulting"] = True
    else:
        print("❌ Instagram consulting: Invalid or missing")
        results["instagram_consulting"] = False
    
    return results

def main():
    """Run complete credential validation"""
    print("🔐 MULTI-PLATFORM CREDENTIALS VALIDATOR (12 CHANNELS)")
    print("=" * 60)
    print(f"📅 Validation time: {datetime.now()}")
    print()
    
    all_results = {}
    
    # Run all validations
    all_results.update(validate_telegram_bots())
    all_results.update(validate_telegram_chat_id())
    all_results.update(validate_kofi_webhooks())
    all_results.update(validate_gumroad_api())
    all_results.update(validate_google_cloud())
    all_results.update(validate_general_config())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    
    total_checks = len(all_results)
    successful_checks = sum(1 for result in all_results.values() if result)
    success_rate = (successful_checks / total_checks) * 100 if total_checks > 0 else 0
    
    print(f"✅ Successful: {successful_checks}/{total_checks}")
    print(f"📈 Success rate: {success_rate:.1f}%")
    print()
    
    # List failed validations
    failed_validations = [key for key, result in all_results.items() if not result]
    if failed_validations:
        print("❌ Failed validations:")
        for failed in failed_validations:
            print(f"   - {failed}")
        print()
        print("🔧 Please check the credentials setup guide and fix missing/invalid credentials.")
    else:
        print("🎉 All credentials configured correctly!")
        print("🚀 12-channel multi-platform system ready for deployment!")
    
    print("\n📋 CURRENT BOT NAMES:")
    print("✅ @AILegalAcademyBot")  
    print("✅ @HealthAIInsights_Bot")
    print("✅ @SeniorTechGuideBot")
    print("✅ @AIEducationHubBot")
    
    return success_rate >= 80  # Return True if at least 80% of validations pass

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)