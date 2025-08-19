#!/usr/bin/env python3
"""
Multi-Platform AI Education Engine
Distributes specialized AI education content across 2 platforms × 4 industries (8 channels)
"""

import os
import json
import time
import requests
import random
from datetime import datetime
from google.cloud import language_v1
from infinite_content_engine import InfiniteContentEngine
from visual_content_engine import VisualContentEngine

class MultiPlatformEngine:
    def __init__(self):
        """Initialize multi-platform content distribution engine"""
        
        # SINGLE MAIN CHANNEL - All content goes to AIEducationHub_bot for partner demonstration
        self.main_channel = {
            "channel": "@AIEducationHub_bot", 
            "token": os.getenv('TELEGRAM_GENERAL_TOKEN')
        }
        
        # Industry classification for content adaptation (all goes to main channel)
        self.industries = {
            "legal": {
                "keywords": ["law", "legal", "attorney", "lawyer", "court", "litigation", "contract", "compliance"],
                "label": "🏛️ LEGAL AI",
                "description": "Legal sector automation and AI tools"
            },
            "medical": {
                "keywords": ["medical", "healthcare", "doctor", "physician", "patient", "diagnosis", "treatment", "clinical"],
                "label": "🏥 MEDICAL AI", 
                "description": "Healthcare and medical AI innovations"
            },
            "senior": {
                "keywords": ["senior", "elderly", "aging", "caregiver", "retirement", "accessibility", "simple", "easy"],
                "label": "👴 SENIOR TECH",
                "description": "Senior-friendly AI and technology"
            },
            "general": {
                "keywords": ["ai", "artificial intelligence", "automation", "technology", "innovation", "business"],
                "label": "🧠 GENERAL AI",
                "description": "General AI education and automation"
            }
        }
        
        # Initialize Google Cloud Natural Language for content classification
        self.language_client = language_v1.LanguageServiceClient()
        
        # Initialize content engines
        self.content_engine = InfiniteContentEngine()
        self.visual_engine = VisualContentEngine()
        
        # Initialize notification system
        self.notification_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.notification_token = os.getenv('TELEGRAM_GENERAL_TOKEN')  # Use dedicated token
        
        print("🚀 AI Education Demo Channel Engine initialized")
        print(f"📊 Content types: {len(self.industries)} industry categories")
        print(f"🔧 Platform: Single Telegram Channel + Visual Content (Vertex AI)")
        print(f"📡 Main channel: {self.main_channel['channel']}")
        print(f"🎨 Visual capabilities: Images + Narrative Scripts + Partner Demo")

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
            # Simple keyword fallback when Google Cloud API fails
            content_lower = content.lower()
            for industry, data in self.industries.items():
                for keyword in data["keywords"]:
                    if keyword in content_lower:
                        print(f"🎯 Fallback classification: {industry}")
                        return industry, 1
            return "general", 1  # Default fallback with confidence

    def adapt_content_for_industry(self, base_content, industry, platform):
        """
        Adapt base content for specific industry and platform
        """
        adaptations = {
            "legal": {
                "telegram": {
                    "prefix": "⚖️ Legal AI Visual Learning",
                    "tone": "Professional, precise, compliance-focused",
                    "cta": "Join our Legal AI community for visual tutorials and case studies"
                }
            },
            "medical": {
                "telegram": {
                    "prefix": "🏥 Medical AI Visual Education",
                    "tone": "Evidence-based, clinical relevance",
                    "cta": "Join our Medical AI community for video tutorials and clinical case studies"
                }
            },
            "senior": {
                "telegram": {
                    "prefix": "👴 Senior-Friendly AI Visual Guide",
                    "tone": "Simple, patient, encouraging",
                    "cta": "Join our Senior Tech community for easy-to-follow video tutorials"
                }
            },
            "general": {
                "telegram": {
                    "prefix": "🧠 AI Education Visual Hub",
                    "tone": "Educational, comprehensive",
                    "cta": "Join our AI Education community for videos, images, and interactive tutorials"
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

    def publish_to_main_channel(self, industry, content, images=None, visual_package=None):
        """Publish content to main demo channel with industry labeling, images, and video"""
        try:
            token = self.main_channel["token"]
            channel = self.main_channel["channel"]
            
            # Add industry label to content
            industry_info = self.industries[industry]
            labeled_content = f"{industry_info['label']} | {industry_info['description']}\n\n{content}"
            
            if not token:
                print(f"⚠️ No Telegram token for main channel")
                return False
            
            # Send text first
            text_url = f"https://api.telegram.org/bot{token}/sendMessage"
            text_payload = {
                "chat_id": channel,
                "text": labeled_content,
                "parse_mode": "Markdown"
            }
            
            print(f"🔍 DEBUG: Sending {industry} text content to main channel {channel}")
            text_response = requests.post(text_url, json=text_payload)
            
            if text_response.status_code != 200:
                print(f"❌ Text message failed: {text_response.status_code} - {text_response.text[:100]}")
                return False
            
            # Send images if available
            if images and isinstance(images, dict):
                print(f"📸 Sending {len(images)} images to {channel}")
                image_success = 0
                
                for image_type, image_path in images.items():
                    if image_path and os.path.exists(image_path):
                        try:
                            # Send photo
                            photo_url = f"https://api.telegram.org/bot{token}/sendPhoto"
                            
                            with open(image_path, 'rb') as photo_file:
                                files = {'photo': photo_file}
                                photo_data = {
                                    'chat_id': channel,
                                    'caption': f"🎨 {image_type.title().replace('_', ' ')}: Visual content for {industry} industry"
                                }
                                
                                photo_response = requests.post(photo_url, data=photo_data, files=files)
                                if photo_response.status_code == 200:
                                    print(f"✅ Sent {image_type} image successfully")
                                    image_success += 1
                                else:
                                    print(f"⚠️ Failed to send {image_type}: {photo_response.status_code}")
                                    
                        except Exception as img_error:
                            print(f"⚠️ Error sending {image_type}: {img_error}")
                    else:
                        print(f"⚠️ Image not found: {image_path}")
                
                print(f"📊 Images sent: {image_success}/{len(images)}")
            
            # Send whiteboard explainer video if available  
            if visual_package and 'whiteboard_video' in visual_package:
                video_path = visual_package['whiteboard_video']
                if video_path and os.path.exists(video_path):
                    try:
                        print(f"🎬 Sending whiteboard explainer video to {channel}")
                        video_url = f"https://api.telegram.org/bot{token}/sendVideo"
                        
                        with open(video_path, 'rb') as video_file:
                            files = {'video': video_file}
                            video_data = {
                                'chat_id': channel,
                                'caption': f"🎨 Whiteboard Explainer Video: {industry} AI automation with psychological persuasion",
                                'supports_streaming': True
                            }
                            
                            video_response = requests.post(video_url, data=video_data, files=files, timeout=90)
                            if video_response.status_code == 200:
                                print(f"✅ Whiteboard explainer video sent successfully!")
                            else:
                                print(f"⚠️ Whiteboard video upload failed: {video_response.status_code}")
                    except Exception as video_error:
                        print(f"⚠️ Error sending whiteboard video: {video_error}")
                else:
                    # Send preview message if video was generated but file not ready
                    try:
                        text_url = f"https://api.telegram.org/bot{token}/sendMessage"
                        video_preview = f"🎥 **Whiteboard Explainer Video Generated!**\n\n🎨 Content: Hand-drawn whiteboard animation for {industry} professionals\n📖 Features: Psychological persuasion + Visual storytelling\n⏱️ Duration: 60-90 seconds\n💡 Style: Real whiteboard drawing with step-by-step explanation\n\n*Powered by Google Veo 3 - Most advanced video AI*"
                        
                        preview_payload = {
                            "chat_id": channel,
                            "text": video_preview,
                            "parse_mode": "Markdown"
                        }
                        requests.post(text_url, json=preview_payload)
                        print("✅ Video preview message sent")
                    except Exception as preview_error:
                        print(f"⚠️ Error sending video preview: {preview_error}")
            
            # Send additional whiteboard explanation if comprehensive whiteboard image exists
            if images and 'whiteboard_complete' in images:
                try:
                    text_url = f"https://api.telegram.org/bot{token}/sendMessage"
                    whiteboard_explanation = f"🎨 **Comprehensive Whiteboard Image**\n\n📚 This visual contains everything:\n• Problem identification & frustration\n• Step-by-step solution workflow  \n• Benefits visualization & ROI charts\n• Industry-specific implementation\n• Success metrics & statistics\n\n💡 Hand-drawn style makes complex AI concepts simple to understand!"
                    
                    explanation_payload = {
                        "chat_id": channel,
                        "text": whiteboard_explanation,
                        "parse_mode": "Markdown"
                    }
                    requests.post(text_url, json=explanation_payload)
                    print("✅ Whiteboard explanation sent")
                except Exception as explanation_error:
                    print(f"⚠️ Error sending whiteboard explanation: {explanation_error}")
            
            print(f"✅ Published {industry} content to main channel: {channel}")
            return True
                
        except Exception as e:
            print(f"❌ Main channel {industry} error: {e}")
            return False

    # Ko-fi API doesn't support posting content - only payment webhooks
    # Removed non-functional Ko-fi integration


    # DISABLED: Gumroad API doesn't support product updates
    # def publish_to_gumroad(self, industry, content):
        """Update industry-specific Gumroad product with new content"""
        print(f"🚀 GUMROAD FUNCTION CALLED for industry: {industry}")
        try:
            api_key = self.industries[industry]["platforms"]["gumroad"]["api_key"]
            product_id = self.industries[industry]["platforms"]["gumroad"]["product_id"]
            
            if not api_key or not product_id:
                print(f"⚠️ Gumroad credentials missing for {industry}")
                return False
            
            # Gumroad API v2 - Try different endpoints for update
            # Method 1: Direct product update (most common)
            update_url = f"https://api.gumroad.com/v2/products/{product_id}"
            print(f"🔍 DEBUG Gumroad: URL={update_url}, ProductID={product_id}, APIKey={api_key[:8]}...")
            
            # First test API key with user endpoint
            user_test_url = "https://api.gumroad.com/v2/user"
            user_response = requests.get(user_test_url, params={"access_token": api_key}, timeout=10)
            print(f"🔍 User API test: {user_response.status_code} - {user_response.text[:100]}")
            
            # List all products to see available IDs
            products_list_url = "https://api.gumroad.com/v2/products"
            products_response = requests.get(products_list_url, params={"access_token": api_key}, timeout=10)
            print(f"🔍 Products list: {products_response.status_code} - {products_response.text[:200]}")
            
            # Test if specific product exists with GET
            get_product_url = f"https://api.gumroad.com/v2/products/{product_id}"
            get_response = requests.get(get_product_url, params={"access_token": api_key}, timeout=10)
            print(f"🔍 Get product test: {get_response.status_code} - {get_response.text[:100]}")
            
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
            
            # Use form-data with access_token (Gumroad API v2 standard)
            payload = {
                "access_token": api_key,
                "description": formatted_description[:1000],  # Gumroad description limit
                "tags": f"ai,education,{industry},automation,prompts"
            }
            
            headers = {
                "User-Agent": "MultiPlatform-AI-Education/1.0"
            }
            
            # Gumroad API: Try PUT with form data (most common for updates)
            print(f"🔄 Trying PUT with form data...")
            response = requests.put(update_url, data=payload, headers=headers, timeout=30)
            print(f"🔍 PUT response: {response.status_code} - {response.text[:100]}")
            
            # If PUT fails, try POST with form data
            if response.status_code in [404, 405]:
                print(f"🔄 PUT failed, trying POST with form data...")
                response = requests.post(update_url, data=payload, headers=headers, timeout=30)
                print(f"🔍 POST response: {response.status_code} - {response.text[:100]}")
                
            # If both fail, try without User-Agent header (some APIs are picky)
            if response.status_code in [404, 405]:
                print(f"🔄 Trying PUT without User-Agent header...")
                simple_headers = {}
                response = requests.put(update_url, data=payload, headers=simple_headers, timeout=30)
                print(f"🔍 Simple PUT response: {response.status_code} - {response.text[:100]}")
            
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
            
            # Ensure chat_id is integer if it's a number
            chat_id = self.notification_chat_id
            try:
                chat_id = int(chat_id) if chat_id.isdigit() or (chat_id.startswith('-') and chat_id[1:].isdigit()) else chat_id
            except (AttributeError, ValueError):
                pass
                
            payload = {
                "chat_id": chat_id,
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
        Main function: Classify content and publish to main demo channel
        """
        print(f"\n🚀 Starting main channel publishing...")
        print(f"📝 Base content: {base_content[:100]}...")
        
        # Classify content to determine primary industry
        primary_industry, confidence = self.classify_content_industry(base_content)
        
        # Adapt content for the classified industry
        adapted_content = self.adapt_content_for_industry(base_content, primary_industry, "telegram")
        
        # Publish to main channel with industry labeling (text only)
        success = self.publish_to_main_channel(primary_industry, adapted_content, None, None)
        results = {f"{primary_industry}_main_channel": success}
        
        print(f"📡 Published {primary_industry} content to main demo channel")
        return results

    def run_visual_content_cycle(self):
        """
        Run advanced visual content generation cycle
        """
        print(f"\n🎬 Starting visual content generation: {datetime.now()}")
        
        # Get fresh tool from content engine
        self.content_engine.update_ai_tools_database()
        available_tools = self.content_engine.get_fresh_tools()
        
        if not available_tools:
            print("❌ No tools available for content generation")
            return 0
            
        # Select random tool and convert to visual content format
        selected_tool = random.choice(available_tools)
        tool_data = {
            "name": selected_tool.name,
            "description": selected_tool.description,
            "category": selected_tool.category,
            "use_case": selected_tool.use_case,
            "income_potential": selected_tool.income_potential,
            "related_tools": ["Zapier", "Make.com", "Airtable"]  # Mock related tools
        }
        
        print(f"🎯 Selected tool for visual content: {tool_data['name']}")
        
        # Generate visual content for one random industry to avoid quota issues
        results = {}
        selected_industry = random.choice(list(self.industries.keys()))
        print(f"🎯 Generating visual content for selected industry: {selected_industry}")
        
        for industry in [selected_industry]:  # Only process one industry
            try:
                print(f"\n🎨 Generating visual content for {industry} industry...")
                
                # Generate complete educational package
                visual_package = self.visual_engine.generate_complete_educational_content(
                    tool_data, industry
                )
                
                if visual_package:
                    # Adapt for Telegram with visual elements  
                    try:
                        telegram_content = self.create_telegram_visual_post(visual_package, industry)
                    except Exception as e:
                        print(f"⚠️ Visual post creation error: {e}")
                        # Use basic adaptation as fallback
                        telegram_content = self.adapt_content_for_industry(
                            f"Visual content: {visual_package.get('title', 'AI Education Content')}", 
                            industry, 
                            "telegram"
                        )
                    
                    # Publish to main demo channel with images and video
                    success = self.publish_to_main_channel(industry, telegram_content, visual_package.get('visuals'), visual_package)
                    results[f"{industry}_visual"] = success
                    
                    if success:
                        print(f"✅ Visual content published to main demo channel")
                    else:
                        print(f"❌ Failed to publish to main demo channel")
                        
                    # Small delay between industries
                    time.sleep(3)
                else:
                    print(f"❌ Failed to generate visual package for {industry}")
                    results[f"{industry}_visual"] = False
                    
            except Exception as e:
                print(f"❌ Error generating visual content for {industry}: {e}")
                results[f"{industry}_visual"] = False
        
        # Summary
        successful_publications = sum(1 for success in results.values() if success)
        total_attempts = len(results)
        success_rate = (successful_publications/total_attempts)*100 if total_attempts > 0 else 0
        
        print(f"\n📊 Visual Content Summary:")
        print(f"✅ Successful: {successful_publications}/{total_attempts}")
        print(f"📈 Success rate: {success_rate:.1f}%")
        print(f"🎨 Tool featured: {tool_data['name']}")
        
        # Send notification
        notification_msg = f"""🎬 **Visual Content Generation Complete**
        
🎯 Featured Tool: {tool_data['name']}
✅ Successful: {successful_publications}/{total_attempts} publications
📈 Success rate: {success_rate:.1f}%
🕐 Time: {datetime.now().strftime('%H:%M %Z')}
📡 Main Demo Channel: {self.main_channel['channel']}
🎨 Content: Advanced narrative + images
👥 Partner Demo: Content visible for evaluation

Platform: Single Telegram Channel + Vertex AI Visual Engine"""
        
        self.send_notification(notification_msg)
        
        return successful_publications
    
    def create_telegram_visual_post(self, visual_package, industry):
        """Create Telegram post with visual content references"""
        
        # Get industry info and create telegram config
        industry_info = self.industries[industry]
        
        # Create telegram config from adaptation function
        adapted_content = self.adapt_content_for_industry("", industry, "telegram")
        
        # Extract telegram config from industry adaptations
        telegram_config = {
            "prefix": industry_info["label"],
            "cta": f"Join our {industry_info['description']} community for visual tutorials and case studies"
        }
        
        # Create visual-enhanced content
        content = f"""{telegram_config['prefix']}

🎬 **{visual_package['title']}**

📖 **Narrative Theme:** {visual_package['theme'].replace('_', ' ').title()}
⏱️ **Duration:** {visual_package['estimated_duration']}

**🔥 Key Highlights:**
{self.extract_script_highlights(visual_package['script'])}

**🎯 Visual Learning Included:**
📸 Professional thumbnails and diagrams
📊 Workflow visualizations  
📈 Success metrics and ROI data
🎨 Step-by-step implementation guides

**📚 Educational Value:**
• Advanced {industry} automation strategies
• Real-world case studies and examples
• Future-ready skill development
• Community-driven learning

---

{telegram_config['cta']}

📧 Contact: {os.getenv('EMAIL_CONTACT', 'jmichaeloficial@gmail.com')}
📱 Community: {os.getenv('INSTAGRAM_CONSULTING', 'https://instagram.com/jmichaeloficial')}

#{industry.upper()}AI #VisualLearning #Education #Automation

*{visual_package['metadata']['created'][:10]} - Advanced Visual Content*"""

        return content
    
    def extract_script_highlights(self, script):
        """Extract key highlights from the generated script"""
        # Simple extraction of key points (in production, could use NLP)
        lines = script.split('\n')
        highlights = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['key', 'important', 'result', 'benefit', 'save']):
                clean_line = line.strip('•-* ').strip()
                if len(clean_line) > 20 and len(clean_line) < 100:
                    highlights.append(f"• {clean_line}")
                    if len(highlights) >= 3:
                        break
        
        if not highlights:
            highlights = [
                "• Professional-grade automation implementation",
                "• Real case studies with measurable results", 
                "• Step-by-step visual learning approach"
            ]
        
        return '\n'.join(highlights[:3])

    def run_daily_publishing_cycle(self):
        """
        Run complete daily publishing cycle with visual content
        """
        print(f"\n🌅 Starting advanced publishing cycle: {datetime.now()}")
        
        # Force visual content for better engagement (90% visual, 10% text)
        use_visual = random.random() < 0.9
        
        if use_visual:
            print("🎨 Running visual content generation...")
            return self.run_visual_content_cycle()
        else:
            print("📝 Running text content generation...")
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
                
                print(f"\n📊 Text Publishing Summary:")
                print(f"✅ Successful: {successful_publications}/{total_attempts}")
                print(f"📈 Success rate: {success_rate:.1f}%")
                
                # Send notification
                notification_msg = f"""📊 **Text Content Publishing Complete**
                
✅ Successful: {successful_publications}/{total_attempts} publications
📈 Success rate: {success_rate:.1f}%
🕐 Time: {datetime.now().strftime('%H:%M %Z')}
📡 Main Demo Channel: {self.main_channel['channel']}
👥 Partner Demo: Content visible for evaluation

Platform: Single Telegram Channel (text content)"""
                
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