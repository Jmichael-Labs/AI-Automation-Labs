#!/usr/bin/env python3
"""
Visual Content Engine - Advanced Educational Content with Google Vertex AI
Creates YouTube-style narrative content with images and videos
"""

import os
import json
import time
import requests
from datetime import datetime
# Optional Vertex AI imports - graceful fallback if not available
try:
    from google.cloud import aiplatform
    from google.cloud.aiplatform.gapic.schema import predict
    import vertexai
    from vertexai.preview.vision_models import ImageGenerationModel
    from vertexai.preview.generative_models import GenerativeModel
    VERTEX_AI_AVAILABLE = True
except ImportError:
    print("⚠️ Vertex AI dependencies not available - using Veo 3 only mode")
    VERTEX_AI_AVAILABLE = False
import google.generativeai as genai
from google import genai as google_genai
from google.genai import types
import time
import random

class VisualContentEngine:
    def __init__(self):
        """Initialize advanced visual content generation with Vertex AI (fallback available)"""
        
        self.vertex_ai_available = False
        self.text_model = None
        self.image_model = None
        self.veo3_client = None
        self.gemini_client = None
        self.video_model = None
        
        if VERTEX_AI_AVAILABLE:
            try:
                # Initialize Vertex AI
                project_id = os.getenv('GOOGLE_PROJECT_ID', 'ai-education-hub-428332946540')
                location = "us-central1"
                
                vertexai.init(project=project_id, location=location)
                
                # Initialize models with correct 2025 versions
                try:
                    self.text_model = GenerativeModel("gemini-2.5-pro")  # Latest advanced reasoning
                except:
                    try:
                        self.text_model = GenerativeModel("gemini-2.5-flash")  # Best price-performance
                    except:
                        try:
                            self.text_model = GenerativeModel("gemini-2.0-flash")  # Next-gen features
                        except:
                            self.text_model = None
                
                try:
                    self.image_model = ImageGenerationModel.from_pretrained("imagegeneration@006")
                except:
                    self.image_model = None
            
                try:
                    # Configure Gemini API for Veo 3 video generation  
                    gemini_api_key = os.getenv('GEMINI_API_KEY')
                    if gemini_api_key:
                        # Configure both APIs for different purposes
                        genai.configure(api_key=gemini_api_key)
                        self.gemini_client = genai
                        
                        # Initialize Veo 3 client for actual video generation
                        try:
                            self.veo3_client = google_genai.Client(api_key=gemini_api_key)
                            self.video_model = "veo-3.0-generate-preview"
                            print("✅ Veo 3 API configured for REAL video generation")
                        except Exception as veo_error:
                            print(f"⚠️ Veo 3 client error: {veo_error}")
                            self.veo3_client = None
                            self.video_model = "gemini-2.0-flash-exp"  # Fallback for descriptions
                            print("✅ Gemini API configured for video descriptions (Veo 3 fallback)")
                    else:
                        print("⚠️ GEMINI_API_KEY not found in environment")
                        self.gemini_client = None
                        self.veo3_client = None
                        self.video_model = None
                except Exception as video_error:
                    print(f"⚠️ Gemini API configuration error: {video_error}")
                    self.gemini_client = None 
                    self.veo3_client = None
                    self.video_model = None
                self.vertex_ai_available = True
                print("✅ Vertex AI models initialized successfully")
                
            except Exception as e:
                print(f"⚠️ Vertex AI not available: {e}")
                print("🔄 Using fallback content generation mode")
                self.vertex_ai_available = False
        else:
            print("🔄 Vertex AI dependencies not installed - Veo 3 only mode")
            self.vertex_ai_available = False
            
            # Still try to initialize Gemini API for Veo 3 even without Vertex AI
            try:
                gemini_api_key = os.getenv('GEMINI_API_KEY')
                if gemini_api_key:
                    genai.configure(api_key=gemini_api_key)
                    self.gemini_client = genai
                    
                    try:
                        self.veo3_client = google_genai.Client(api_key=gemini_api_key)
                        self.video_model = "veo-3.0-generate-preview"
                        print("✅ Veo 3 API configured for REAL video generation (no Vertex AI)")
                    except Exception as veo_error:
                        print(f"⚠️ Veo 3 client error: {veo_error}")
                        self.veo3_client = None
                        self.video_model = "gemini-2.0-flash-exp"
                        print("✅ Gemini API configured for video descriptions (Veo 3 fallback)")
                else:
                    print("⚠️ GEMINI_API_KEY not found in environment")
            except Exception as e:
                print(f"⚠️ Gemini API configuration error: {e}")
                self.gemini_client = None 
                self.veo3_client = None
                self.video_model = None
        
        # Content themes for journalistic/news style content
        self.narrative_themes = {
            "market_analysis": {
                "title_pattern": "AI Market Update: {tool_name} Impact on {industry} Sector",
                "narrative_style": "Journalistic market analysis with data",
                "visual_style": "Market charts, adoption graphs, business metrics",
                "hooks": [
                    "New data reveals {tool_name} adoption in {industry} increased 340% this quarter.",
                    "Breaking: {industry} companies using {tool_name} report average 25% cost reduction.",
                    "Market analysis: Why {tool_name} is becoming essential for {industry} competitiveness."
                ]
            },
            "industry_intelligence": {
                "title_pattern": "Industry Intelligence: {tool_name} Reshaping {industry} Landscape",
                "narrative_style": "Professional industry analysis",
                "visual_style": "Industry trends, competitive analysis, market positioning",
                "hooks": [
                    "Latest industry data shows {industry} professionals with {tool_name} skills earn 40% more.",
                    "Survey reveals: 78% of {industry} companies plan {tool_name} implementation in 2025.",
                    "Industry report: {tool_name} disrupting traditional {industry} workflows."
                ]
            },
            "tech_news_report": {
                "title_pattern": "Tech News: {tool_name} Latest Updates & {industry} Impact",
                "narrative_style": "News reporting with factual analysis",
                "visual_style": "News graphics, update timelines, impact assessments",
                "hooks": [
                    "Breaking: {tool_name} announces major update affecting {industry} workflows.",
                    "Tech news: {tool_name} partnership with major {industry} companies confirmed.",
                    "Latest update: {tool_name} adds features specifically for {industry} professionals."
                ]
            },
            "data_investigation": {
                "title_pattern": "Data Investigation: Real {tool_name} Performance in {industry}",
                "narrative_style": "Investigative journalism with verified data",
                "visual_style": "Data visualizations, performance charts, verified sources",
                "hooks": [
                    "We analyzed 500+ {industry} companies using {tool_name}. Here's what we found.",
                    "Exclusive data: Real performance metrics of {tool_name} in {industry} sector.",
                    "Investigation reveals: Actual ROI data from {tool_name} implementations in {industry}."
                ]
            },
            "product_showcase": {
                "title_pattern": "Product Showcase: Real Digital Tools for {industry} Professionals",
                "narrative_style": "Product journalism - honest reviews and demonstrations",
                "visual_style": "Product screenshots, feature demos, user testimonials",
                "hooks": [
                    "New digital tools available: AGI-created resources for {industry} automation.",
                    "Product spotlight: Real automation tools built by AI specialists.",
                    "Tool review: Genuine {industry} productivity software created by advanced AI."
                ]
            }
        }
        
        # Visual content specifications
        self.visual_specs = {
            "thumbnail": {
                "dimensions": "1280x720",
                "style": "Bold, high-contrast, YouTube-optimized",
                "elements": ["Large text overlay", "Tool logos", "Attention-grabbing visuals"]
            },
            "educational_diagrams": {
                "dimensions": "1920x1080",
                "style": "Clean, professional, infographic-style",
                "elements": ["Step-by-step flows", "Before/after comparisons", "Feature highlights"]
            },
            "workflow_visualizations": {
                "dimensions": "1920x1080", 
                "style": "Modern, tech-focused, animated-ready",
                "elements": ["Process flows", "Data connections", "Automation paths"]
            }
        }
        
        print("🎨 Visual Content Engine initialized with Vertex AI")
        print(f"📊 Narrative themes: {len(self.narrative_themes)}")
        print(f"🎯 Visual specifications: {len(self.visual_specs)}")

    def generate_narrative_script(self, tool_data, industry, theme_type):
        """Generate YouTube-style narrative script using Gemini with robust fallback"""
        
        theme = self.narrative_themes[theme_type]
        hook = random.choice(theme["hooks"])
        
        # Always use fallback if Vertex AI is not available
        if not self.vertex_ai_available or not self.text_model:
            print("🔄 Using fallback script generation (Vertex AI not available)")
            return self.generate_fallback_script(tool_data, industry, theme_type)
        
        # Create comprehensive prompt for narrative generation
        narrative_prompt = f"""
Create an engaging, YouTube-style educational script about {tool_data['name']} for {industry} professionals.

THEME: {theme['narrative_style']}
HOOK: {hook.format(tool_name=tool_data['name'], industry=industry, income=tool_data.get('income_potential', '$2,500'))}

SCRIPT STRUCTURE:
1. HOOK (15 seconds) - Grab attention immediately
2. PROBLEM SETUP (30 seconds) - What pain point does this solve?
3. SOLUTION REVEAL (45 seconds) - Introduce {tool_data['name']} as the hero
4. DEEP DIVE (2-3 minutes) - How it actually works
5. REAL EXAMPLES (1-2 minutes) - Case studies and results
6. IMPLEMENTATION (1-2 minutes) - Step-by-step guide
7. FUTURE OUTLOOK (30 seconds) - What's coming next
8. CALL TO ACTION (15 seconds) - Join our community

TONE: Informative yet entertaining, like Veritasium or Johnny Harris
STYLE: Use storytelling, data points, and visual cues
FOCUS: Make complex AI tools accessible and exciting

Tool Details:
- Name: {tool_data['name']}
- Description: {tool_data['description']}
- Category: {tool_data['category']}
- Use Case: {tool_data['use_case']}
- Income Potential: {tool_data.get('income_potential', '$2,500/month')}

Generate a compelling 6-8 minute script with clear visual cue markers [VISUAL: description] throughout.
"""

        try:
            print("🧠 Attempting Gemini 1.5 Pro script generation...")
            response = self.text_model.generate_content(narrative_prompt)
            print("✅ Gemini script generation successful")
            return response.text
        except Exception as e:
            print(f"⚠️ Vertex AI narrative generation failed: {e}")
            print("🔄 Falling back to local script generation")
            return self.generate_fallback_script(tool_data, industry, theme_type)

    def generate_fallback_script(self, tool_data, industry, theme_type):
        """Generate fallback script when Vertex AI is unavailable"""
        theme = self.narrative_themes[theme_type]
        hook = random.choice(theme["hooks"])
        
        return f"""
{hook.format(tool_name=tool_data['name'], industry=industry, income=tool_data.get('income_potential', '$2,500'))}

[VISUAL: Split screen - frustrated professional vs successful automation]

The {industry} industry has a problem. Professionals are spending 60% of their time on repetitive tasks that could be automated. But most people don't know about {tool_data['name']}.

[VISUAL: {tool_data['name']} interface showcase]

{tool_data['name']} is a {tool_data['description']} that's specifically designed for {industry} workflows. Here's what makes it different:

[VISUAL: Feature breakdown infographic]

1. INTELLIGENT AUTOMATION: Unlike basic tools, {tool_data['name']} learns your specific {industry} patterns
2. INDUSTRY INTEGRATION: Built-in connections to every major {industry} platform
3. SCALABLE RESULTS: Users report {tool_data.get('income_potential', '$2,500/month')} in time savings

[VISUAL: Case study timeline]

Take Sarah, a {industry} professional who implemented {tool_data['name']} in January. By March, she had automated 70% of her routine tasks. By June, she was generating an additional {tool_data.get('income_potential', '$2,500/month')} in revenue.

[VISUAL: Step-by-step implementation guide]

Here's exactly how to implement {tool_data['name']}:

WEEK 1: Setup and Integration
- Connect your existing {industry} tools
- Configure basic automation rules
- Test with small workflows

WEEK 2-3: Optimization
- Analyze performance data
- Refine automation triggers
- Scale successful workflows

WEEK 4+: Advanced Features
- Implement AI-powered decisions
- Create complex multi-step automations
- Monitor ROI and optimize

[VISUAL: Future prediction infographic]

The future of {industry} is automated. By 2026, professionals using tools like {tool_data['name']} will have a massive competitive advantage. Those who don't adapt will be left behind.

[VISUAL: Community showcase]

Ready to transform your {industry} career? Join our AI Education community where we provide step-by-step tutorials, case studies, and direct support for implementing these tools.

The automation revolution is happening now. Don't get left behind.
"""

    def generate_educational_image(self, prompt, visual_type="educational_diagrams"):
        """Generate educational images using Imagen 3.0 with robust fallback"""
        
        # Skip image generation if Vertex AI is not available
        if not self.vertex_ai_available or not self.image_model:
            print(f"🔄 Skipping image generation (Vertex AI not available) for: {visual_type}")
            return None
        
        spec = self.visual_specs[visual_type]
        
        # Enhanced prompt for educational content
        enhanced_prompt = f"""
{prompt}

Style: {spec['style']}
Elements: {', '.join(spec['elements'])}
Quality: Professional, educational, high-resolution
Colors: Modern tech palette (blues, whites, accent colors)
Layout: Clean, organized, easy to understand
Text: Clear, readable fonts with proper hierarchy
Purpose: Educational content for AI tool tutorials
"""

        try:
            print(f"🎨 Attempting Imagen 3.0 generation for {visual_type}: {prompt[:50]}...")
            
            images = self.image_model.generate_images(
                prompt=enhanced_prompt,
                number_of_images=1,
                aspect_ratio="16:9",
                safety_filter_level="block_few",
                person_generation="allow_adult"
            )
            
            if images:
                # Save image without PIL dependency
                try:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"/tmp/ai_education_{visual_type}_{timestamp}.png"
                    images[0].save(location=filename)
                    print(f"✅ Image saved: {filename}")
                    return filename
                except Exception as save_error:
                    print(f"⚠️ Image save error: {save_error}")
                    return None
            else:
                print("⚠️ No images generated by Imagen 3.0")
                return None
                
        except Exception as e:
            print(f"⚠️ Imagen 3.0 generation error: {e}")
            if "quota" in str(e).lower() or "429" in str(e):
                print("📊 Vertex AI quota exceeded - content will proceed without images")
            elif "404" in str(e):
                print("🔍 Imagen 3.0 model not accessible - check project permissions")
            return None

    def generate_futuristic_newsroom_segments(self, tool_data, industry, script_highlights, latest_ai_news=None):
        """Generate 12 sequential 8-second futuristic newsroom segments for complete AI news story"""
        
        if not self.veo3_client or not self.video_model:
            print(f"🔄 Skipping futuristic newsroom video generation (Veo 3 API not available)")
            return None
        
        # Futuristic newsroom visual specifications
        newsroom_style = {
            "base_aesthetic": "futuristic newsroom, holographic panels glowing in blue and purple light",
            "scene_elements": "floating 3D screens show abstract AI icons (brain, robot, lock, chip)",
            "camera_work": "slow pan across holographic desk, cinematic lighting",
            "voice_style": "calm professional newscaster voice in English",
            "mood": "informative, urgent but optimistic",
            "color_palette": "blue, purple, silver, white holographic glow"
        }
        
        # Captology-enhanced industry targeting for biografía traffic
        industry_captology = {
            "legal": {
                "hook": "Breaking: New AI regulation affecting 80% of law firms",
                "authority": "Leading legal tech experts confirm",
                "urgency": "Changes take effect this quarter",
                "social_proof": "Top-tier law firms already implementing"
            },
            "medical": {
                "hook": "Medical AI breakthrough: 40% faster diagnosis accuracy",
                "authority": "Clinical research validates effectiveness", 
                "urgency": "Early adoption provides competitive advantage",
                "social_proof": "Leading hospitals report significant improvements"
            },
            "senior": {
                "hook": "Senior-friendly AI tools gaining massive adoption",
                "authority": "Gerontology experts recommend these solutions",
                "urgency": "Simple tools becoming mainstream quickly",
                "social_proof": "Thousands of seniors successfully using daily"
            },
            "general": {
                "hook": "AI market explosion: New tools changing everything",
                "authority": "Industry analysts predict massive disruption",
                "urgency": "Early adopters securing significant advantages",
                "social_proof": "Fortune 500 companies investing heavily"
            }
        }
        
        captology = industry_captology[industry]
        
        # Define 12 sequential 8-second segments (12 total = 96 seconds complete story)
        video_segments = [
            {
                "title": "Opening - Breaking News Hook",
                "duration": 8,
                "content": f"Futuristic newsroom establishing shot with glowing holographic panels. News ticker: '{captology['hook']}'",
                "visual": f"{newsroom_style['base_aesthetic']}, {newsroom_style['camera_work']}, news ticker with breaking news text",
                "narration": f"This is AI News Update - Breaking: {captology['hook']}"
            },
            {
                "title": "Authority Validation",
                "duration": 8,
                "content": f"Holographic expert panel discussing AI trends. {captology['authority']} with floating credentials",
                "visual": f"{newsroom_style['scene_elements']}, expert hologram, floating certification badges",
                "narration": f"{captology['authority']} that {tool_data['name']} represents the future of {industry}"
            },
            {
                "title": "Market Analysis",
                "duration": 8,
                "content": f"3D holographic charts showing AI adoption rates. Market growth statistics floating in space",
                "visual": f"{newsroom_style['scene_elements']}, 3D growth charts, market statistics, data visualization",
                "narration": f"Market analysis shows {captology['urgency']} - early adopters seeing immediate ROI"
            },
            {
                "title": "Tool Spotlight",
                "duration": 8,
                "content": f"Holographic {tool_data['name']} interface materializes with glowing features highlighted",
                "visual": f"{newsroom_style['base_aesthetic']}, {tool_data['name']} logo hologram, feature callouts",
                "narration": f"Introducing {tool_data['name']} - the {industry} tool that's changing everything"
            },
            {
                "title": "Technology Deep Dive",
                "duration": 8,
                "content": f"AI brain visualization with neural networks processing {industry} data in real-time",
                "visual": f"{newsroom_style['scene_elements']}, AI brain hologram, neural network animation, data flow",
                "narration": f"Advanced AI processes {industry} workflows 300% faster than traditional methods"
            },
            {
                "title": "Success Metrics",
                "duration": 8,
                "content": f"Floating success metrics and ROI calculations with real-time updates",
                "visual": f"{newsroom_style['scene_elements']}, ROI dashboard, success percentage, profit graphs",
                "narration": f"Users report {tool_data.get('income_potential', '$2,500/month')} average income increase within 90 days"
            },
            {
                "title": "Social Proof Evidence",
                "duration": 8,
                "content": f"Holographic testimonials from {industry} professionals floating around newsroom",
                "visual": f"{newsroom_style['base_aesthetic']}, floating testimonial holograms, user avatars",
                "narration": f"{captology['social_proof']} - join thousands already transforming their {industry} practice"
            },
            {
                "title": "Implementation Guide",
                "duration": 8,
                "content": f"Step-by-step holographic tutorial showing setup process with glowing checkmarks",
                "visual": f"{newsroom_style['scene_elements']}, step-by-step tutorial, progress indicators",
                "narration": f"Getting started takes just 3 simple steps - even beginners see results immediately"
            },
            {
                "title": "Community Showcase",
                "duration": 8,
                "content": f"Holographic global map showing community members worldwide with success stories",
                "visual": f"{newsroom_style['base_aesthetic']}, world map hologram, community member icons",
                "narration": f"Join our exclusive {industry} AI community - over 50,000 professionals strong"
            },
            {
                "title": "Urgency & Scarcity",
                "duration": 8,
                "content": f"Countdown timer with limited access notification and exclusive offer details",
                "visual": f"{newsroom_style['scene_elements']}, countdown timer, exclusive access badge",
                "narration": f"Limited time: Get exclusive access to our {industry} AI toolkit and community"
            },
            {
                "title": "Contact & Bio Link",
                "duration": 8,
                "content": f"Professional contact information with direct bio link and instant access button",
                "visual": f"{newsroom_style['base_aesthetic']}, contact hologram, bio link highlight, call button",
                "narration": f"Click the link in our bio for instant access to tools, courses, and community"
            },
            {
                "title": "Closing - Future Vision",
                "duration": 8,
                "content": f"Futuristic vision of {industry} transformation with AI integration success story",
                "visual": f"{newsroom_style['base_aesthetic']}, future vision hologram, success transformation",
                "narration": f"This is the future of {industry} - and it starts with your next decision. Join us."
            }
        ]
        
        print(f"🎬 Generating {len(video_segments)} futuristic newsroom segments for {tool_data['name']}")
        print(f"📺 Total duration: {len(video_segments) * 8} seconds ({len(video_segments) * 8 / 60:.1f} minutes)")
        
        # Generate all 12 segments sequentially for complete video
        generated_segments = []
        
        for i, segment in enumerate(video_segments, 1):
            print(f"🎨 Generating segment {i}/12: {segment['title']}")
            
            segment_prompt = f"""
Create an 8-second futuristic AI newsroom segment: "{segment['title']}"

VISUAL STYLE: {segment['visual']}
NEWSROOM AESTHETIC: {newsroom_style['base_aesthetic']}
CAMERA WORK: {newsroom_style['camera_work']}
COLOR PALETTE: {newsroom_style['color_palette']}

NARRATION (English): {segment.get('narration', segment['content'])}
VOICE STYLE: {newsroom_style['voice_style']}
MOOD: {newsroom_style['mood']}

TECHNICAL REQUIREMENTS:
- Duration: Exactly 8 seconds
- Style: Futuristic holographic newsroom
- Resolution: 1080p, 16:9 aspect ratio
- Professional English narration
- Ambient electronic news theme background
- Smooth cinematic camera movements

VISUAL ELEMENTS:
- Holographic panels with blue/purple glow
- Floating 3D AI icons and data
- Professional news anchor presence
- Smooth transitions between elements
- Industry-specific content for {industry}

SEQUENCE FLOW:
This is segment {i} of 12 in a complete story arc.
Ensure visual continuity with previous segments.
End with smooth transition setup for next segment.
"""

            try:
                print(f"🎬 Using Veo 3 API for REAL newsroom video generation...")
                
                # Generate ACTUAL VIDEO with Veo 3 API
                if not self.veo3_client:
                    raise Exception("Veo 3 client not available")
                
                # Generate actual video using Veo 3
                operation = self.veo3_client.models.generate_videos(
                    model=self.video_model,
                    prompt=segment_prompt,
                    config=types.GenerateVideosConfig(
                        negative_prompt="cartoon, amateur, low quality, blurry, unprofessional, hand-drawn",
                        aspect_ratio="16:9"
                    )
                )
            
            print(f"🔄 Polling video generation operation...")
            max_wait_time = 300  # 5 minutes max wait
            poll_interval = 10   # Check every 10 seconds
            waited_time = 0
            
            # Poll for completion
            while not operation.done and waited_time < max_wait_time:
                print(f"⏱️ Waiting for video generation... ({waited_time}s/{max_wait_time}s)")
                time.sleep(poll_interval)
                waited_time += poll_interval
                operation = self.veo3_client.operations.get(operation)
            
            if operation.done and hasattr(operation, 'result'):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Get the generated video
                generated_video = operation.result.generated_videos[0]
                
                # Download and save the REAL video file
                video_filename = f"/tmp/whiteboard_segment_1_{industry}_{timestamp}.mp4"
                
                # Download the video file
                video_data = self.veo3_client.files.download(file=generated_video.video)
                
                # Save the actual video file
                with open(video_filename, 'wb') as video_file:
                    video_file.write(video_data)
                
                # Verify file was saved correctly
                if os.path.exists(video_filename):
                    file_size = os.path.getsize(video_filename)
                    print(f"🎥 REAL NEWSROOM VIDEO successfully generated!")
                    print(f"📁 File: {video_filename}")
                    print(f"📊 File size: {file_size} bytes") 
                    print(f"⏱️ Duration: 8 seconds (Veo 3)")
                    print(f"📺 Resolution: 720p, 16:9 aspect ratio")
                    print(f"🎙️ Audio: Professional English narration")
                    print(f"✅ File verification: EXISTS and has {file_size} bytes")
                    
                    generated_segments.append({
                        "segment_number": i,
                        "title": segment['title'],
                        "file_path": video_filename,
                        "file_size": file_size,
                        "narration": segment.get('narration', segment['content'])
                    })
                    
                    # For now, only generate first segment to test (quota management)
                    if i == 1:
                        print(f"🎯 Generated segment {i}/12 - Testing single segment first")
                        break
                        
                else:
                    print(f"❌ ERROR: Video file was not saved to {video_filename}")
                    
            except Exception as e:
                print(f"⚠️ Segment {i} generation error: {e}")
                continue
        
        print(f"📊 Generation Summary:")
        print(f"✅ Segments generated: {len(generated_segments)}/12")
        print(f"🎬 Style: Futuristic AI newsroom")
        print(f"🗣️ Language: Professional English")
        print(f"🎯 Purpose: Bio link conversion via captology")
        
        # Return first segment for testing (future: return concatenated video)
        if generated_segments:
            return generated_segments[0]['file_path']
        else:
            return None

    # Keep old function for backwards compatibility
    def generate_whiteboard_explainer_video(self, tool_data, industry, script_highlights):
        """Wrapper function - calls new futuristic newsroom generation"""
        return self.generate_futuristic_newsroom_segments(tool_data, industry, script_highlights)

    def create_visual_content_package(self, script, tool_data, industry):
        """Create complete visual package for educational content"""
        
        print(f"🎬 Creating visual package for {tool_data['name']} in {industry}")
        
        visual_package = {
            "script": script,
            "images": {},
            "metadata": {
                "tool": tool_data['name'],
                "industry": industry,
                "created": datetime.now().isoformat(),
                "type": "educational_narrative"
            }
        }
        
        # Generate SINGLE whiteboard-style image that represents everything
        whiteboard_image_prompt = f"""
Create a single comprehensive whiteboard-style educational diagram about {tool_data['name']} for {industry} professionals.

WHITEBOARD STYLE:
- Clean white background like a real whiteboard
- Hand-drawn black sketches and diagrams
- Simple stick figures and basic shapes
- Handwritten-style text labels
- Connecting arrows drawn by hand
- Mathematical equations and formulas if relevant
- Informal, sketch-like appearance

CONTENT TO INCLUDE IN ONE IMAGE:
1. PROBLEM SECTION (top-left): Stick figure looking frustrated at desk with papers scattered
2. SOLUTION SECTION (center): {tool_data['name']} drawn as simple interface box with arrows
3. WORKFLOW SECTION (middle): Step-by-step process: Input → {tool_data['name']} → Output → Results
4. BENEFITS SECTION (right): Hand-drawn charts showing:
   - Time saved: Clock with arrow
   - Money saved: Dollar signs
   - Efficiency: Upward trending graph
5. STATISTICS (bottom): Simple bar chart showing "{tool_data.get('income_potential', '$2,500/month')}" ROI
6. CALL-TO-ACTION (bottom-right): "Join {industry} professionals using this!" in handwritten style

VISUAL ELEMENTS:
- Hand-drawn arrows connecting all sections
- Simple icons (lightbulb for ideas, gear for process, etc.)
- Sketch-style borders around sections
- Handwritten labels and titles
- Mathematical formulas or process equations where relevant
- Simple flowchart elements

INDUSTRY CONTEXT: Adapt terminology and icons specifically for {industry} sector
TONE: Educational, approachable, like a teacher explaining on a real whiteboard
SIZE: Comprehensive enough to be the ONLY visual needed - contains all information
"""
        
        whiteboard_path = self.generate_educational_image(whiteboard_image_prompt, "educational_diagrams")
        if whiteboard_path:
            visual_package["images"]["whiteboard_complete"] = whiteboard_path
            print("✅ Single comprehensive whiteboard image generated!")
        
        # RESTORE VIDEO GENERATION - Both whiteboard image AND video
        # Generate whiteboard explainer video with Veo 3 (100% chance for testing REAL videos)
        if random.random() < 1.0:  # 100% probability to test Veo 3 real video generation
            print("🎬 Generating whiteboard explainer video...")
            whiteboard_video_path = self.generate_whiteboard_explainer_video(tool_data, industry, script)
            if whiteboard_video_path:
                visual_package["whiteboard_video"] = whiteboard_video_path
                print("🎥 Whiteboard explainer video successful!")
            else:
                print("⚠️ Video generation failed - quota or API issue")
        else:
            print("🎲 Video generation skipped this time (quota management)")
        
        # Log generation results  
        total_images = len(visual_package["images"])
        has_whiteboard_image = "whiteboard_complete" in visual_package["images"]
        has_whiteboard_video = "whiteboard_video" in visual_package
        
        print(f"🎨 Visual package complete: {total_images} images + {'🎥✅' if has_whiteboard_video else '❌'} whiteboard video")
        
        if total_images == 0 and not has_whiteboard_video:
            print("📝 Content will proceed as text-only due to generation issues")
        elif has_whiteboard_image and has_whiteboard_video:
            print("🎉 PERFECT! Both whiteboard image AND video generated!")
        elif has_whiteboard_image:
            print("✅ Whiteboard image ready - video will try next time")
        elif has_whiteboard_video:
            print("🎥 Whiteboard video ready - image generation had issues")

        return visual_package

    def generate_complete_educational_content(self, tool_data, industry):
        """Generate complete educational content package"""
        
        print(f"🚀 Generating complete educational content for {tool_data['name']}")
        
        # Select random narrative theme
        theme_type = random.choice(list(self.narrative_themes.keys()))
        print(f"📖 Using narrative theme: {theme_type}")
        
        # Generate script
        script = self.generate_narrative_script(tool_data, industry, theme_type)
        
        # Create visual package
        visual_package = self.create_visual_content_package(script, tool_data, industry)
        
        # Generate title using theme pattern
        theme = self.narrative_themes[theme_type]
        if theme_type == "comparative_analysis" and len(tool_data.get('related_tools', [])) > 0:
            title = theme["title_pattern"].format(
                tool1=tool_data['name'],
                tool2=random.choice(tool_data.get('related_tools', ['Zapier'])),
                industry=industry
            )
        else:
            title = theme["title_pattern"].format(
                tool_name=tool_data['name'],
                industry=industry,
                income=tool_data.get('income_potential', '$2,500')
            )
        
        # Complete package - INCLUDE VIDEO!
        complete_package = {
            "title": title,
            "theme": theme_type,
            "script": script,
            "visuals": visual_package["images"],
            "whiteboard_video": visual_package.get("whiteboard_video"),  # ← ADD VIDEO HERE!
            "metadata": visual_package["metadata"],
            "publishing_ready": True,
            "estimated_duration": "6-8 minutes",
            "content_type": "educational_narrative"
        }
        
        print(f"✅ Complete educational package created: {title}")
        print(f"🔍 DEBUG: Package includes video: {'whiteboard_video' in complete_package and complete_package['whiteboard_video'] is not None}")
        if complete_package.get('whiteboard_video'):
            print(f"🔍 DEBUG: Video path in package: {complete_package['whiteboard_video']}")
        return complete_package

# Test function
if __name__ == "__main__":
    # Test with sample tool data
    test_tool = {
        "name": "Zapier",
        "description": "Automation platform connecting 6000+ apps",
        "category": "automation",
        "use_case": "Automate business workflows",
        "income_potential": "$3,500/month",
        "related_tools": ["Make.com", "IFTTT", "Microsoft Power Automate"]
    }
    
    print("🧪 Testing Visual Content Engine...")
    engine = VisualContentEngine()
    
    # Generate complete package
    package = engine.generate_complete_educational_content(test_tool, "legal")
    
    print(f"\n🎉 Generated: {package['title']}")
    print(f"📝 Script length: {len(package['script'])} characters")
    print(f"🎨 Images generated: {len(package['visuals'])}")
    print(f"⏱️ Estimated duration: {package['estimated_duration']}")