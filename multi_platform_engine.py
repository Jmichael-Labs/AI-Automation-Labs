#!/usr/bin/env python3
"""
Multi-Platform AI Education Engine
Distributes specialized AI education content across 3 platforms × 4 industries (12 channels)
"""

import os
import json
import time
import requests
from datetime import datetime
from google.cloud import language_v1
from infinite_content_engine import InfiniteContentEngine

class MultiPlatformEngine:
    def __init__(self):
        """Initialize multi-platform content distribution engine"""
        
        # Industry classification
        self.industries = {
            "legal": {
                "keywords": ["law", "legal", "attorney", "lawyer", "court", "litigation", "contract", "compliance"],
                "platforms": {
                    "telegram": {"channel": "@LegalAIAcademy", "token": os.getenv('TELEGRAM_LEGAL_TOKEN')},
                    "kofi": {"profile": "legalaiacademy", "api_key": os.getenv('KOFI_LEGAL_API')},
                    "gumroad": {"product_id": os.getenv('GUMROAD_LEGAL_ID'), "api_key": os.getenv('GUMROAD_API_KEY')}
                }
            },
            "medical": {
                "keywords": ["medical", "healthcare", "doctor", "physician", "patient", "diagnosis", "treatment", "clinical"],
                "platforms": {
                    "telegram": {"channel": "@HealthAIInsights", "token": os.getenv('TELEGRAM_MEDICAL_TOKEN')},
                    "kofi": {"profile": "healthaiinsights", "api_key": os.getenv('KOFI_MEDICAL_API')},
                    "gumroad": {"product_id": os.getenv('GUMROAD_MEDICAL_ID'), "api_key": os.getenv('GUMROAD_API_KEY')}
                }
            },
            "senior": {
                "keywords": ["senior", "elderly", "aging", "caregiver", "retirement", "accessibility", "simple", "easy"],
                "platforms": {
                    "telegram": {"channel": "@SeniorTechGuide", "token": os.getenv('TELEGRAM_SENIOR_TOKEN')},
                    "kofi": {"profile": "seniortechguide", "api_key": os.getenv('KOFI_SENIOR_API')},
                    "gumroad": {"product_id": os.getenv('GUMROAD_SENIOR_ID'), "api_key": os.getenv('GUMROAD_API_KEY')}
                }
            },
            "general": {
                "keywords": ["ai", "artificial intelligence", "automation", "technology", "innovation", "business"],
                "platforms": {
                    "telegram": {"channel": "@AIEducationHub", "token": os.getenv('TELEGRAM_GENERAL_TOKEN')},
                    "kofi": {"profile": "aieducationhub", "api_key": os.getenv('KOFI_GENERAL_API')},
                    "gumroad": {"product_id": os.getenv('GUMROAD_GENERAL_ID'), "api_key": os.getenv('GUMROAD_API_KEY')}
                }
            }
        }
        
        # Initialize Google Cloud Natural Language for content classification
        self.language_client = language_v1.LanguageServiceClient()
        
        # Initialize base content engine
        self.content_engine = InfiniteContentEngine()
        
        # Initialize notification system
        self.notification_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.notification_token = self.industries["general"]["platforms"]["telegram"]["token"]
        
        print("🚀 Multi-Platform AI Education Engine initialized")
        print(f"📊 Industries: {len(self.industries)}")
        print(f"🔧 Platforms per industry: 3")
        print(f"📡 Total channels: {len(self.industries) * 3}")

    def classify_content_industry(self, content):
        """
        Classify content into industry using Google Cloud Natural Language API
        """
        try:
            # Analyze content with Google NL API
            document = language_v1.Document(content=content, type_=language_v1.Document.Type.PLAIN_TEXT)
            
            # Get entities and keywords
            entities_response = self.language_client.analyze_entities(
                request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
            )
            
            # Extract keywords from entities
            detected_keywords = []
            for entity in entities_response.entities:
                detected_keywords.append(entity.name.lower())
            
            # Add content text keywords
            content_lower = content.lower()
            
            # Score each industry based on keyword matches
            industry_scores = {}
            for industry, data in self.industries.items():
                score = 0
                for keyword in data["keywords"]:
                    # Check in detected entities
                    if any(keyword in dk for dk in detected_keywords):
                        score += 2
                    # Check in content text
                    if keyword in content_lower:
                        score += 1
                
                industry_scores[industry] = score
            
            # Return industry with highest score
            best_industry = max(industry_scores, key=industry_scores.get)
            confidence = industry_scores[best_industry]
            
            print(f"🎯 Content classified as: {best_industry} (confidence: {confidence})")
            return best_industry, confidence
            
        except Exception as e:
            print(f"⚠️ Classification error: {e}")
            return "general", 0  # Default fallback

    def adapt_content_for_industry(self, base_content, industry, platform):
        """
        Adapt base content for specific industry and platform
        """
        adaptations = {
            "legal": {
                "telegram": {
                    "prefix": "⚖️ Legal AI Insight",
                    "tone": "Professional, precise, compliance-focused",
                    "cta": "Learn more: ko-fi.com/legalaiacademy"
                },
                "kofi": {
                    "prefix": "🏛️ Legal Practice Enhancement",
                    "tone": "ROI-focused, practice management",
                    "cta": "Join Legal AI Academy membership for advanced prompts"
                },
                "gumroad": {
                    "prefix": "💼 Legal AI Toolkit",
                    "tone": "Product-focused, immediate value",
                    "cta": "Get Legal AI Prompts Library ($97)"
                }
            },
            "medical": {
                "telegram": {
                    "prefix": "🏥 Medical AI Breakthrough",
                    "tone": "Evidence-based, clinical relevance",
                    "cta": "Learn more: ko-fi.com/healthaiinsights"
                },
                "kofi": {
                    "prefix": "⚕️ Healthcare Innovation",
                    "tone": "Patient outcomes, efficiency gains",
                    "cta": "Support Medical AI research with membership"
                },
                "gumroad": {
                    "prefix": "📋 Medical AI Assistant",
                    "tone": "Practical tools, time-saving",
                    "cta": "Get Medical AI Documentation Kit ($197)"
                }
            },
            "senior": {
                "telegram": {
                    "prefix": "👴 Senior-Friendly AI",
                    "tone": "Simple, patient, encouraging",
                    "cta": "Learn more: ko-fi.com/seniortechguide"
                },
                "kofi": {
                    "prefix": "❤️ Tech Support for Seniors",
                    "tone": "Supportive, step-by-step guidance",
                    "cta": "Get personalized senior tech support"
                },
                "gumroad": {
                    "prefix": "🎯 Easy AI for Seniors",
                    "tone": "Simplified, illustrated guides",
                    "cta": "Get Senior AI Starter Kit ($47)"
                }
            },
            "general": {
                "telegram": {
                    "prefix": "🧠 AI Education Daily",
                    "tone": "Educational, comprehensive",
                    "cta": "Learn more: ko-fi.com/aieducationhub"
                },
                "kofi": {
                    "prefix": "🚀 AI Learning Hub",
                    "tone": "Progressive learning, skill building",
                    "cta": "Join AI Education community"
                },
                "gumroad": {
                    "prefix": "🎓 AI Mastery Collection",
                    "tone": "Comprehensive learning resources",
                    "cta": "Get AI Education Starter Pack ($29)"
                }
            }
        }
        
        adaptation = adaptations.get(industry, adaptations["general"])
        platform_config = adaptation.get(platform, adaptation["telegram"])
        
        # Format adapted content
        adapted_content = f"""
{platform_config['prefix']}

{base_content}

💡 Tone: {platform_config['tone']}

{platform_config['cta']}

#{industry.upper()}AI #Education #Automation
"""
        
        return adapted_content.strip()

    def publish_to_telegram(self, industry, content):
        """Publish content to industry-specific Telegram channel"""
        try:
            token = self.industries[industry]["platforms"]["telegram"]["token"]
            channel = self.industries[industry]["platforms"]["telegram"]["channel"]
            
            if not token:
                print(f"⚠️ No Telegram token for {industry}")
                return False
            
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {
                "chat_id": channel,
                "text": content,
                "parse_mode": "Markdown"
            }
            
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f"✅ Published to Telegram {industry}: {channel}")
                return True
            else:
                print(f"❌ Telegram {industry} failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Telegram {industry} error: {e}")
            return False

    def publish_to_kofi(self, industry, content):
        """Publish content to industry-specific Ko-fi profile via webhook"""
        try:
            webhook_url = self.industries[industry]["platforms"]["kofi"]["api_key"]
            profile = self.industries[industry]["platforms"]["kofi"]["profile"]
            
            if not webhook_url:
                print(f"⚠️ Ko-fi webhook URL missing for {industry}")
                return False
            
            # Ko-fi uses webhook integration for posting updates
            payload = {
                "type": "shop_update",
                "data": {
                    "message": content[:500],  # Ko-fi limit ~500 chars
                    "timestamp": datetime.now().isoformat(),
                    "shop_items": f"Visit ko-fi.com/{profile} for AI education resources"
                }
            }
            
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "MultiPlatform-AI-Education/1.0"
            }
            
            response = requests.post(webhook_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code in [200, 201, 202]:
                print(f"✅ Ko-fi {industry} update posted: ko-fi.com/{profile}")
                return True
            else:
                print(f"❌ Ko-fi {industry} failed: {response.status_code} - {response.text[:100]}")
                return False
            
        except Exception as e:
            print(f"❌ Ko-fi {industry} error: {e}")
            return False


    def publish_to_gumroad(self, industry, content):
        """Update industry-specific Gumroad product with new content"""
        try:
            api_key = self.industries[industry]["platforms"]["gumroad"]["api_key"]
            product_id = self.industries[industry]["platforms"]["gumroad"]["product_id"]
            
            if not api_key or not product_id:
                print(f"⚠️ Gumroad credentials missing for {industry}")
                return False
            
            # Gumroad API v2 - Update product
            update_url = f"https://api.gumroad.com/v2/products/{product_id}"
            
            # Format content for product description update
            formatted_description = f"""
🚀 LATEST UPDATE - {datetime.now().strftime('%B %d, %Y')}

{content}

📚 This AI education resource includes:
✅ Industry-specific prompts and guides
✅ Real-world implementation examples
✅ Step-by-step tutorials
✅ Regular content updates

💡 Perfect for {industry} professionals looking to leverage AI effectively.
            """.strip()
            
            payload = {
                "access_token": api_key,
                "description": formatted_description[:1000],  # Gumroad description limit
                "tags": f"ai,education,{industry},automation,prompts"
            }
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "MultiPlatform-AI-Education/1.0"
            }
            
            response = requests.put(update_url, data=payload, headers=headers, timeout=30)
            
            if response.status_code in [200, 201]:
                product_data = response.json()
                product_url = product_data.get('product', {}).get('short_url', f'gumroad.com/l/{product_id}')
                print(f"✅ Gumroad {industry} product updated: {product_url}")
                return True
            else:
                print(f"❌ Gumroad {industry} failed: {response.status_code} - {response.text[:100]}")
                return False
            
        except Exception as e:
            print(f"❌ Gumroad {industry} error: {e}")
            return False

    def send_notification(self, message):
        """Send notification to personal Telegram chat"""
        try:
            if not self.notification_chat_id or not self.notification_token:
                print("⚠️ Notification system not configured")
                return False
            
            url = f"https://api.telegram.org/bot{self.notification_token}/sendMessage"
            payload = {
                "chat_id": self.notification_chat_id,
                "text": f"🤖 Multi-Platform System\n\n{message}",
                "parse_mode": "Markdown"
            }
            
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                print("✅ Notification sent successfully")
                return True
            else:
                print(f"❌ Notification failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Notification error: {e}")
            return False

    def publish_multi_platform(self, base_content):
        """
        Main function: Classify content and publish to all relevant platforms
        """
        print(f"\n🚀 Starting multi-platform publishing...")
        print(f"📝 Base content: {base_content[:100]}...")
        
        # Classify content to determine primary industry
        primary_industry, confidence = self.classify_content_industry(base_content)
        
        # Publish to all platforms for the primary industry
        results = {}
        for platform in ["telegram", "kofi", "gumroad"]:
            adapted_content = self.adapt_content_for_industry(base_content, primary_industry, platform)
            
            if platform == "telegram":
                success = self.publish_to_telegram(primary_industry, adapted_content)
            elif platform == "kofi":
                success = self.publish_to_kofi(primary_industry, adapted_content)
            elif platform == "gumroad":
                success = self.publish_to_gumroad(primary_industry, adapted_content)
            
            results[f"{primary_industry}_{platform}"] = success
            
            # Small delay between platforms
            time.sleep(2)
        
        # Also publish to general industry if confidence is low
        if confidence < 3:
            print(f"🔄 Low confidence ({confidence}), also publishing to general...")
            for platform in ["telegram"]:  # Just Telegram for general fallback
                adapted_content = self.adapt_content_for_industry(base_content, "general", platform)
                success = self.publish_to_telegram("general", adapted_content)
                results[f"general_{platform}"] = success
        
        return results

    def run_daily_publishing_cycle(self):
        """
        Run complete daily publishing cycle across all industries
        """
        print(f"\n🌅 Starting daily publishing cycle: {datetime.now()}")
        
        # Generate base content using existing Infinite Content Engine
        base_content = self.content_engine.generate_infinite_content()
        
        if base_content:
            title, content = base_content
            
            # Use the content for multi-platform distribution
            results = self.publish_multi_platform(content)
            
            # Summary
            successful_publications = sum(1 for success in results.values() if success)
            total_attempts = len(results)
            success_rate = (successful_publications/total_attempts)*100 if total_attempts > 0 else 0
            
            print(f"\n📊 Publishing Summary:")
            print(f"✅ Successful: {successful_publications}/{total_attempts}")
            print(f"📈 Success rate: {success_rate:.1f}%")
            
            # Send notification
            notification_msg = f"""📊 **Publishing Cycle Complete**
            
✅ Successful: {successful_publications}/{total_attempts} publications
📈 Success rate: {success_rate:.1f}%
🕐 Time: {datetime.now().strftime('%H:%M %Z')}
📡 Channels: {len(self.industries) * 3} total

Platforms: Telegram + Ko-fi + Gumroad"""
            
            self.send_notification(notification_msg)
            
            return successful_publications
        else:
            print("❌ Failed to generate base content")
            return 0

if __name__ == "__main__":
    try:
        print("🎯 MULTI-PLATFORM AI EDUCATION ENGINE STARTING...")
        print(f"📅 Execution time: {datetime.now()}")
        
        engine = MultiPlatformEngine()
        
        print("🧪 Testing multi-platform publishing...")
        publications = engine.run_daily_publishing_cycle()
        
        print(f"🎉 RESULT: {publications} successful publications across platforms")
        
        if publications > 0:
            print("✅ SUCCESS: Multi-platform system operational!")
        else:
            print("⚠️ WARNING: No publications completed")
            
    except Exception as e:
        print(f"💥 FATAL ERROR: {str(e)}")
        import traceback
        print("📍 Full traceback:")
        traceback.print_exc()
        exit(1)