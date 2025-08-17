#!/usr/bin/env python3
"""
Real-time AI News Aggregator
Scrapes AI subreddits for latest news and creates unified posts
"""

import praw
import requests
import json
from datetime import datetime, timedelta
import re

class AINewsAggregator:
    def __init__(self, reddit_instance):
        self.reddit = reddit_instance
        
        # AI/Tech subreddits for news gathering
        self.news_subreddits = [
            "artificial",
            "MachineLearning", 
            "OpenAI",
            "ChatGPT",
            "ArtificialIntelligence",
            "singularity",
            "Futurology",
            "technology",
            "MachineLearningNews"
        ]
        
        # LLM API for content rewriting (using simple API)
        self.llm_api_url = "https://api.openai.com/v1/chat/completions" # Fallback to local LLM
        
    def scrape_latest_ai_news(self, hours_back=24, max_posts=20):
        """Scrape latest AI news from multiple subreddits"""
        news_items = []
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        print(f"Scraping AI news from last {hours_back} hours...")
        
        for subreddit_name in self.news_subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                print(f"Checking r/{subreddit_name}...")
                
                for post in subreddit.hot(limit=max_posts):
                    post_time = datetime.fromtimestamp(post.created_utc)
                    
                    # Only get recent posts
                    if post_time > cutoff_time:
                        # Filter for AI/tech related content
                        if self.is_tech_news(post):
                            news_item = {
                                'title': post.title,
                                'content': post.selftext[:500] if post.selftext else "",
                                'url': post.url,
                                'score': post.score,
                                'subreddit': subreddit_name,
                                'created': post_time,
                                'num_comments': post.num_comments
                            }
                            news_items.append(news_item)
                            
            except Exception as e:
                print(f"Error scraping r/{subreddit_name}: {e}")
                continue
        
        # Sort by score and recency
        news_items.sort(key=lambda x: (x['score'], x['created']), reverse=True)
        return news_items[:10]  # Top 10 stories
    
    def is_tech_news(self, post):
        """Determine if post is relevant AI/tech news"""
        title_lower = post.title.lower()
        content_lower = post.selftext.lower() if post.selftext else ""
        combined = f"{title_lower} {content_lower}"
        
        # Key indicators of AI/tech news
        tech_keywords = [
            "ai", "artificial intelligence", "machine learning", "openai", "chatgpt",
            "claude", "gemini", "llm", "gpt", "neural network", "deep learning",
            "automation", "algorithm", "model", "technology", "breakthrough",
            "research", "development", "innovation", "release", "update",
            "announcement", "launch", "startup", "funding", "acquisition"
        ]
        
        # News indicators
        news_indicators = [
            "announced", "released", "launched", "revealed", "discovered",
            "breakthrough", "new", "latest", "today", "this week", "report",
            "study", "research", "funding", "investment", "acquired"
        ]
        
        has_tech = any(keyword in combined for keyword in tech_keywords)
        has_news = any(indicator in combined for indicator in news_indicators)
        
        # Must have good engagement (avoid spam)
        has_engagement = post.score > 10 or post.num_comments > 5
        
        return has_tech and (has_news or has_engagement)
    
    def synthesize_news_with_llm(self, news_items):
        """Use LLM to synthesize multiple news items into cohesive post"""
        
        # Prepare news summary for LLM
        news_summary = "Recent AI/Tech News Items:\n\n"
        for i, item in enumerate(news_items[:5], 1):  # Top 5 stories
            news_summary += f"{i}. {item['title']}\n"
            if item['content']:
                news_summary += f"   {item['content'][:200]}...\n"
            news_summary += f"   Source: r/{item['subreddit']} | Score: {item['score']}\n\n"
        
        # Captology-focused prompt (no emojis, humanized)
        captology_prompt = f"""You are an expert technology analyst writing for business professionals. 
        
Transform these AI/tech news items into a compelling, humanized article that:

1. NEVER uses emojis or symbols
2. Writes in a conversational, expert tone (like a trusted advisor)
3. Focuses on practical business implications
4. Connects the dots between different developments  
5. Includes subtle persuasive elements (social proof, urgency, authority)
6. Ends with a thought-provoking question for engagement

News to synthesize:
{news_summary}

Write a 400-word article that makes readers feel informed and slightly behind if they're not paying attention to AI developments. Be authoritative but approachable.

Title: Create a compelling title (no emojis)
Content: Write the full article"""

        try:
            # Try to use LLM API (simplified version)
            response = self.call_llm_api(captology_prompt)
            if response:
                return self.parse_llm_response(response)
        except Exception as e:
            print(f"LLM API failed: {e}")
        
        # Fallback: Template-based synthesis
        return self.template_based_synthesis(news_items)
    
    def call_llm_api(self, prompt):
        """Call LLM API for content generation"""
        # For now, return None to use template fallback
        # TODO: Integrate with your 27 AGI nuclei system
        return None
    
    def template_based_synthesis(self, news_items):
        """Fallback template-based news synthesis - BILINGUAL"""
        if not news_items:
            return None, None
            
        today = datetime.now().strftime("%B %d, %Y")
        today_es = datetime.now().strftime("%d de %B, %Y")
        title = f"AI Intelligence Brief - Informe de IA | {today}"
        
        # Group news by theme
        breakthrough_news = [item for item in news_items if any(word in item['title'].lower() 
                            for word in ['breakthrough', 'new', 'launch', 'release'])]
        business_news = [item for item in news_items if any(word in item['title'].lower() 
                        for word in ['funding', 'acquisition', 'startup', 'company'])]
        research_news = [item for item in news_items if any(word in item['title'].lower() 
                        for word in ['research', 'study', 'paper', 'model'])]
        
        content = f"""# AI Intelligence Brief - Informe de IA | {today}

**English:** The artificial intelligence landscape continues evolving at breakneck speed. Here's what caught my attention in the past 24 hours, and why it matters for anyone building their future around intelligent systems.

**Español:** El panorama de la inteligencia artificial sigue evolucionando a una velocidad vertiginosa. Aquí está lo que captó mi atención en las últimas 24 horas, y por qué es importante para cualquiera que esté construyendo su futuro con sistemas inteligentes.

## Technology Developments | Desarrollos Tecnológicos

"""
        
        if breakthrough_news:
            content += f"""**{breakthrough_news[0]['title']}**

**EN:** The implications here extend beyond the immediate technical achievement. {breakthrough_news[0]['content'][:100] if breakthrough_news[0]['content'] else 'This development signals a broader shift in how AI systems are being designed and deployed.'}

**ES:** Las implicaciones van más allá del logro técnico inmediato. {breakthrough_news[0]['content'][:100] if breakthrough_news[0]['content'] else 'Este desarrollo señala un cambio más amplio en cómo los sistemas de IA están siendo diseñados e implementados.'}

"""
        
        if business_news:
            content += f"""## Market Movements | Movimientos del Mercado

**{business_news[0]['title']}**

**EN:** Follow the money, and you'll see where the industry is heading. {business_news[0]['content'][:100] if business_news[0]['content'] else 'Investment patterns like this often predict which technologies will dominate the next cycle.'}

**ES:** Sigue el dinero y verás hacia dónde se dirige la industria. {business_news[0]['content'][:100] if business_news[0]['content'] else 'Patrones de inversión como este a menudo predicen qué tecnologías dominarán el próximo ciclo.'}

"""
        
        if research_news:
            content += f"""## Research Frontiers | Fronteras de Investigación

**{research_news[0]['title']}**

**EN:** Academic breakthroughs typically take 18-24 months to reach practical applications. {research_news[0]['content'][:100] if research_news[0]['content'] else 'Smart money starts positioning now for what researchers are publishing today.'}

**ES:** Los avances académicos típicamente toman 18-24 meses en llegar a aplicaciones prácticas. {research_news[0]['content'][:100] if research_news[0]['content'] else 'El dinero inteligente comienza a posicionarse ahora para lo que los investigadores están publicando hoy.'}

"""
        
        content += f"""## Why This Matters | Por Qué Esto Importa

**EN:** The convergence of these developments isn't coincidental. We're seeing the early stages of AI systems that can truly augment human decision-making at scale. The companies and professionals who recognize this pattern first will have a significant advantage.

**ES:** La convergencia de estos desarrollos no es coincidencial. Estamos viendo las primeras etapas de sistemas de IA que realmente pueden aumentar la toma de decisiones humanas a escala. Las empresas y profesionales que reconozcan este patrón primero tendrán una ventaja significativa.

**EN:** The question isn't whether AI will transform your industry - it's whether you'll be leading that transformation or responding to it.

**ES:** La pregunta no es si la IA transformará tu industria - es si estarás liderando esa transformación o respondiendo a ella.

**EN:** What patterns are you seeing in your field that suggest AI integration is accelerating?

**ES:** ¿Qué patrones estás viendo en tu campo que sugieren que la integración de IA se está acelerando?

---

**Want to discuss how these developments might impact your specific situation? | ¿Quieres discutir cómo estos desarrollos podrían impactar tu situación específica?**

Email: jmichaeloficial@gmail.com
Instagram: https://www.instagram.com/jmichaeloficial/

*Building competitive advantage through intelligent automation | Construyendo ventaja competitiva a través de automatización inteligente*"""
        
        return title, content
    
    def parse_llm_response(self, response):
        """Parse LLM response to extract title and content"""
        # TODO: Implement when LLM API is working
        return None, None
    
    def generate_real_time_post(self):
        """Main function to generate real-time AI news post"""
        print("Generating real-time AI news post...")
        
        # Scrape latest news
        news_items = self.scrape_latest_ai_news(hours_back=24, max_posts=15)
        
        if not news_items:
            print("No recent AI news found, using fallback content")
            return None, None
        
        print(f"Found {len(news_items)} relevant news items")
        
        # Synthesize with LLM/template
        title, content = self.synthesize_news_with_llm(news_items)
        
        return title, content

if __name__ == "__main__":
    # Test the aggregator
    import praw
    
    reddit = praw.Reddit(
        client_id='sVYH1t6xaF8j5MkfcTVxww',
        client_secret='7kbuoA9Ct_X_LN5DyFJwcL3gKHVu3A',
        user_agent='AIAutomationLabsBot:v1.0 (by /u/AIAutomationLabs)',
        username='AIAutomationLabs',
        password='Suxtan20@'
    )
    
    aggregator = AINewsAggregator(reddit)
    title, content = aggregator.generate_real_time_post()
    
    if title and content:
        print(f"\nGENERATED POST:")
        print(f"Title: {title}")
        print(f"Content:\n{content}")
    else:
        print("Failed to generate post")