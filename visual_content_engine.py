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
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from vertexai.preview.generative_models import GenerativeModel
import random

class VisualContentEngine:
    def __init__(self):
        """Initialize advanced visual content generation with Vertex AI (fallback available)"""
        
        self.vertex_ai_available = False
        self.text_model = None
        self.image_model = None
        
        try:
            # Initialize Vertex AI
            project_id = os.getenv('GOOGLE_PROJECT_ID', 'ai-education-hub-428332946540')
            location = "us-central1"
            
            vertexai.init(project=project_id, location=location)
            
            # Initialize models
            self.text_model = GenerativeModel("gemini-1.5-pro")
            self.image_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
            self.vertex_ai_available = True
            print("✅ Vertex AI models initialized successfully")
            
        except Exception as e:
            print(f"⚠️ Vertex AI not available: {e}")
            print("🔄 Using fallback content generation mode")
            self.vertex_ai_available = False
        
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
        """Generate YouTube-style narrative script using Gemini"""
        
        theme = self.narrative_themes[theme_type]
        hook = random.choice(theme["hooks"])
        
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
            response = self.text_model.generate_content(narrative_prompt)
            return response.text
        except Exception as e:
            print(f"⚠️ Narrative generation error: {e}")
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
        """Generate educational images using Imagen 3.0"""
        
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
            print(f"🎨 Generating {visual_type} image: {prompt[:50]}...")
            
            images = self.image_model.generate_images(
                prompt=enhanced_prompt,
                number_of_images=1,
                aspect_ratio="16:9",
                safety_filter_level="block_few",
                person_generation="allow_adult"
            )
            
            if images:
                # Save image locally
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"/tmp/ai_education_{visual_type}_{timestamp}.png"
                
                images[0].save(location=filename)
                print(f"✅ Image saved: {filename}")
                return filename
            else:
                print("⚠️ No images generated")
                return None
                
        except Exception as e:
            print(f"⚠️ Image generation error: {e}")
            return None

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
        
        # Generate thumbnail
        thumbnail_prompt = f"""
YouTube thumbnail for '{tool_data['name']} Tutorial for {industry} Professionals'
Show: Tool interface, successful professional, dramatic before/after results
Text overlay: '{tool_data['name']} REVEALED', 'GAME CHANGER', '${tool_data.get('income_potential', '2500')}/month'
Style: High contrast, bold colors, attention-grabbing
"""
        thumbnail_path = self.generate_educational_image(thumbnail_prompt, "thumbnail")
        if thumbnail_path:
            visual_package["images"]["thumbnail"] = thumbnail_path

        # Generate workflow diagram
        workflow_prompt = f"""
Step-by-step workflow diagram showing how {tool_data['name']} automates {industry} processes
Show: Input data → {tool_data['name']} processing → Automated output → Results
Include: Icons, arrows, clear labels, professional design
Style: Modern infographic, easy to follow, educational
"""
        workflow_path = self.generate_educational_image(workflow_prompt, "workflow_visualizations")
        if workflow_path:
            visual_package["images"]["workflow"] = workflow_path

        # Generate feature breakdown
        features_prompt = f"""
Feature breakdown infographic for {tool_data['name']}
Show: Key features, benefits, pricing, comparison with alternatives
Layout: Grid format, icons for each feature, clear hierarchy
Text: Feature names, brief descriptions, value propositions
Style: Clean, professional, educational design
"""
        features_path = self.generate_educational_image(features_prompt, "educational_diagrams")
        if features_path:
            visual_package["images"]["features"] = features_path

        # Generate success metrics
        metrics_prompt = f"""
Success metrics and ROI visualization for {tool_data['name']} in {industry}
Show: Time saved, revenue increase, efficiency gains, user satisfaction
Charts: Bar graphs, pie charts, trend lines showing improvement
Data: {tool_data.get('income_potential', '$2,500/month')}, 70% time savings, 95% user satisfaction
Style: Professional dashboard, clear data visualization
"""
        metrics_path = self.generate_educational_image(metrics_prompt, "educational_diagrams")
        if metrics_path:
            visual_package["images"]["metrics"] = metrics_path

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
        
        # Complete package
        complete_package = {
            "title": title,
            "theme": theme_type,
            "script": script,
            "visuals": visual_package["images"],
            "metadata": visual_package["metadata"],
            "publishing_ready": True,
            "estimated_duration": "6-8 minutes",
            "content_type": "educational_narrative"
        }
        
        print(f"✅ Complete educational package created: {title}")
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