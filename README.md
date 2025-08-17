# 🤖 AI Automation Labs - Autonomous Reddit Bot

![AIAutomationLabs Logo](logo.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-blue.svg)](https://github.com/features/actions)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)

## 🎯 Overview

**AI Automation Labs Reddit Bot** is a fully autonomous system that generates and posts AI automation content to Reddit communities. Built for educational purposes and community building, this bot demonstrates how to create intelligent, content-aware automation systems.

### ✨ Key Features

- **🔄 Fully Autonomous**: Runs 24/7 without manual intervention using GitHub Actions
- **📚 1,000+ Business Prompts**: Leverages extensive prompt library for varied content generation
- **📡 Real-time AI News**: Scrapes and synthesizes latest AI developments from multiple sources
- **🎯 Smart Scheduling**: Optimized posting times (9 AM, 3 PM, 8 PM EST) for maximum engagement
- **💰 Zero Cost**: Completely free to run using GitHub's infrastructure
- **🛡️ Anti-Spam Protection**: Built-in duplicate detection and rate limiting
- **🔧 Configurable**: Easy setup with environment variables

## 🚀 Quick Start

### Prerequisites

- GitHub account (free tier includes unlimited Actions minutes for public repos)
- Reddit account and application credentials
- Python 3.11+ (for local testing)

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/ai-automation-labs-bot.git
cd ai-automation-labs-bot
pip install -r requirements.txt
```

### 2. Reddit Application Setup

1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Fill in the details:
   - **Name**: Your bot name (e.g., "MyAIBot")
   - **App type**: Script
   - **Description**: Brief description of your bot
   - **About URL**: Leave blank or add your website
   - **Redirect URI**: `http://localhost:8080`
4. Save the **Client ID** and **Client Secret**

### 3. Configure GitHub Secrets

Go to your repository **Settings → Secrets and Variables → Actions** and add:

| Secret Name | Description | Example |
|------------|-------------|---------|
| `REDDIT_CLIENT_ID` | Your Reddit app client ID | `abc123def456` |
| `REDDIT_CLIENT_SECRET` | Your Reddit app secret | `xyz789uvw012` |
| `REDDIT_USERNAME` | Your Reddit account username | `YourBotAccount` |
| `REDDIT_PASSWORD` | Your Reddit account password | `YourSecurePassword` |
| `REDDIT_USER_AGENT` | Bot identifier | `YourBot:v1.0 (by /u/YourUsername)` |
| `EMAIL_CONTACT` | Contact email for posts | `your.email@example.com` |
| `INSTAGRAM_CONSULTING` | Instagram URL (optional) | `https://instagram.com/youraccount` |

### 4. Customize Your Bot

#### Target Subreddit
Edit `ai_news_poster.py` line 30:
```python
self.target_subreddit = "YourSubredditName"  # Change this to your target subreddit
```

#### Business Prompts
The bot includes 1,000+ business prompts. To add your own:
1. Add prompts to `load_business_prompts()` function
2. Or modify the prompts file path in line 355

#### Contact Information
Update your contact details in the configuration section or use environment variables.

## 🏗️ Architecture

### Core Components

```
ai-automation-labs-bot/
├── 🤖 ai_news_poster.py           # Main bot logic and content generation
├── 📡 real_time_news_aggregator.py # AI news scraping and synthesis
├── ⚙️ .github/workflows/          # GitHub Actions automation
├── 📋 requirements.txt            # Python dependencies
├── 📄 README.md                   # This documentation
└── 📜 LICENSE                     # MIT License
```

### Workflow Process

1. **GitHub Actions Trigger**: Cron jobs execute at scheduled times
2. **News Aggregation**: Scrapes latest AI developments from 9+ subreddits
3. **Content Generation**: Combines business prompts with trending AI tools
4. **Reddit Posting**: Creates engaging posts with professional formatting
5. **Anti-Spam Check**: Prevents duplicate posts and respects rate limits

## 📊 Posting Schedule

| Time (EST) | Post Type | Content Focus |
|------------|-----------|---------------|
| 9:00 AM | Morning Brief | Latest AI developments and tools |
| 3:00 PM | Afternoon Update | Business applications and case studies |
| 8:00 PM | Evening Insight | Community discussions and Q&A |

## 🛠️ Local Development

### Run Locally for Testing

```bash
# Set environment variables
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USERNAME="your_username"
export REDDIT_PASSWORD="your_password"
export REDDIT_USER_AGENT="YourBot:v1.0 (by /u/YourUsername)"

# Test the bot
python ai_news_poster.py
```

### Debug Mode

```bash
# Check Reddit connection
python check_posts.py

# Test content generation
python test_new_content.py
```

## 🔧 Configuration Options

### Content Customization

| Setting | Location | Description |
|---------|----------|-------------|
| Target Subreddit | `ai_news_poster.py:30` | Primary subreddit for posting |
| Post Frequency | `.github/workflows/autonomous_reddit_bot.yml` | Cron schedule timing |
| Business Prompts | `ai_news_poster.py:353` | Path to prompts file |
| News Sources | `real_time_news_aggregator.py:18` | AI/tech subreddits list |

### Advanced Settings

- **Rate Limiting**: Modify `max_daily_posts` in `ai_news_poster.py`
- **Content Quality**: Adjust filtering criteria in `is_tech_news()`
- **Post Templates**: Customize content generation functions

## 📈 Features in Detail

### 🧠 Intelligent Content Generation

- **Dynamic Prompts**: Cycles through 1,000+ business automation prompts
- **Trending Integration**: Incorporates current AI tools and developments
- **Context Awareness**: Adapts content based on recent industry news
- **Professional Tone**: Captology-based persuasive writing without emojis

### 🛡️ Anti-Spam Protection

- **Duplicate Detection**: Tracks posted content to prevent repetition
- **Rate Limiting**: Respects Reddit's API guidelines
- **Quality Filtering**: Only processes high-engagement, relevant content
- **Time Spacing**: Intelligent delays between multiple posts

### 📊 Monitoring and Logs

- **GitHub Actions Logs**: Track execution history and performance
- **Error Handling**: Comprehensive logging for debugging
- **Success Metrics**: Post count and engagement tracking

## 🚀 Advanced Usage

### Custom Business Prompts

Create your own prompt file:

```python
custom_prompts = [
    {
        'title': 'Your Custom Automation Idea',
        'content': 'Detailed prompt for automation strategy...',
        'category': 'automation'
    }
]
```

### Multiple Subreddits

Modify the bot to post to multiple communities:

```python
target_subreddits = ["AIAutomationLabs", "MachineLearning", "artificial"]
```

### Custom Scheduling

Adjust posting times in `.github/workflows/autonomous_reddit_bot.yml`:

```yaml
schedule:
  - cron: '0 14 * * *'  # 9 AM EST
  - cron: '0 20 * * *'  # 3 PM EST  
  - cron: '0 1 * * *'   # 8 PM EST
```

## 🔒 Security Best Practices

### Environment Variables
- ✅ Store all credentials as GitHub Secrets
- ❌ Never commit passwords or API keys to repository
- ✅ Use descriptive but non-sensitive user agents

### Reddit API Usage
- ✅ Respect rate limits (1 request per second)
- ✅ Follow Reddit's API terms of service
- ✅ Implement proper error handling

### Code Security
- ✅ Regular dependency updates
- ✅ Input validation and sanitization
- ✅ Comprehensive error logging

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 Python style guidelines
- Add docstrings to all functions
- Include tests for new features
- Update documentation as needed

## 📋 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Authentication Failed | Check Reddit credentials in GitHub Secrets |
| No Posts Generated | Verify target subreddit exists and bot has permissions |
| GitHub Actions Not Running | Check cron syntax and repository settings |
| Rate Limit Exceeded | Increase delays between requests |

### Debug Steps

1. **Check Logs**: GitHub Actions → Your workflow → View logs
2. **Test Locally**: Run bot locally with debug output
3. **Verify Credentials**: Test Reddit connection manually
4. **Review Permissions**: Ensure bot account can post to target subreddit

## 📊 Performance Metrics

### Typical Performance
- **Execution Time**: 2-3 minutes per run
- **Success Rate**: 95%+ with proper configuration
- **Content Quality**: Professional, engaging posts
- **Resource Usage**: <1% of GitHub Actions free tier

### Optimization Tips
- Use specific subreddit targets for better engagement
- Customize prompts for your industry/niche
- Monitor posting times for optimal audience reach
- Regularly update AI news sources

## 🌟 Use Cases

### Business Applications
- **Community Building**: Engage AI/automation communities
- **Thought Leadership**: Share insights on AI developments  
- **Lead Generation**: Build authority and attract prospects
- **Content Marketing**: Automated content distribution

### Educational Use
- **Learning Automation**: Practical GitHub Actions example
- **Reddit API**: Real-world API integration
- **AI Integration**: Combining multiple AI services
- **Open Source**: Community-driven development

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-automation-labs-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-automation-labs-bot/discussions)
- **Email**: See contact information in repository

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Reddit API for community platform
- GitHub Actions for free automation infrastructure  
- Open source Python libraries used in this project
- AI/automation community for inspiration and feedback

---

**Built with ❤️ by the AI Automation Labs community**

*Empowering businesses through intelligent automation*