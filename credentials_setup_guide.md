# 🔐 Multi-Platform Credentials Setup Guide

## 📋 **GitHub Secrets Required (15 total)**

### 🤖 **Telegram Bot Tokens (4 industries)**
```
TELEGRAM_LEGAL_TOKEN = "YOUR_LEGAL_BOT_TOKEN"
TELEGRAM_MEDICAL_TOKEN = "YOUR_MEDICAL_BOT_TOKEN" 
TELEGRAM_SENIOR_TOKEN = "YOUR_SENIOR_BOT_TOKEN"
TELEGRAM_GENERAL_TOKEN = "YOUR_GENERAL_BOT_TOKEN"
```

**Setup Instructions:**
1. Message @BotFather on Telegram
2. Create 4 bots with these names:
   - `@AILegalAcademyBot`
   - `@HealthAIInsights_Bot`
   - `@SeniorTechGuideBot`
   - `@AIEducationHubBot`
3. Copy each token to GitHub Secrets

### 💰 **Ko-fi API Keys (4 industries)**
```
KOFI_LEGAL_API = "YOUR_LEGAL_KOFI_KEY"
KOFI_MEDICAL_API = "YOUR_MEDICAL_KOFI_KEY"
KOFI_SENIOR_API = "YOUR_SENIOR_KOFI_KEY"
KOFI_GENERAL_API = "YOUR_GENERAL_KOFI_KEY"
```

**Setup Instructions:**
1. Create 4 Ko-fi accounts:
   - `ko-fi.com/legalaiacademy`
   - `ko-fi.com/healthaiinsights`
   - `ko-fi.com/seniortechguide`
   - `ko-fi.com/aieducationhub`
2. Enable webhooks in each account
3. Copy webhook URLs to GitHub Secrets

### 📱 **Telegram Chat ID (for notifications)**
```
TELEGRAM_CHAT_ID = "YOUR_PERSONAL_CHAT_ID"
```

**Setup Instructions:**
1. Message @userinfobot on Telegram to get your chat ID
2. Or message any of your bots and check the logs for chat_id
3. Copy the numerical ID (example: 123456789)
4. This will be used for system notifications

### 🛍️ **Gumroad Configuration (1 API key + 4 products)**
```
GUMROAD_API_KEY = "YOUR_GUMROAD_API_KEY"
GUMROAD_LEGAL_ID = "LEGAL_PRODUCT_ID"
GUMROAD_MEDICAL_ID = "MEDICAL_PRODUCT_ID"
GUMROAD_SENIOR_ID = "SENIOR_PRODUCT_ID"
GUMROAD_GENERAL_ID = "GENERAL_PRODUCT_ID"
```

**Setup Instructions:**
1. Create Gumroad account
2. Create 4 placeholder products:
   - "Legal AI Academy Collection"
   - "Health AI Insights Toolkit"
   - "Senior Tech Guide Bundle"
   - "AI Education Hub Resources"
3. Get API key from Settings > Developer API
4. Copy each product ID from product settings

### ☁️ **Google Cloud Configuration (2 items)**
```
GOOGLE_CLOUD_CREDENTIALS = "YOUR_SERVICE_ACCOUNT_JSON"
GOOGLE_PROJECT_ID = "YOUR_GCP_PROJECT_ID"
```

**Setup Instructions:**
1. Create Google Cloud Project
2. Enable Natural Language API
3. Create Service Account
4. Download JSON key file
5. Copy entire JSON content to `GOOGLE_CLOUD_CREDENTIALS`
6. Copy project ID to `GOOGLE_PROJECT_ID`

### 📞 **Contact Information (2 items)**
```
EMAIL_CONTACT = "your.email@example.com"
INSTAGRAM_CONSULTING = "https://instagram.com/youraccount"
```

## 🚀 **Quick Setup Commands**

### **Create All Telegram Bots:**
```bash
# Send these messages to @BotFather one by one:
/newbot
AI Legal Academy Bot
AILegalAcademy_Bot

/newbot  
Health AI Insights Bot
HealthAIInsights_Bot

/newbot
Senior Tech Guide Bot
SeniorTechGuide_Bot

/newbot
AI Education Hub Bot
AIEducationHub_Bot
```

### **Test Credentials:**
```bash
# Test Telegram bots:
curl "https://api.telegram.org/bot<TOKEN>/getMe"

# Test Telegram Chat ID:
curl "https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=Test"

# Test Gumroad API:
curl "https://api.gumroad.com/v2/user" -d "access_token=<API_KEY>"
```

## ⚠️ **Security Best Practices**

### **✅ DO:**
- Store all secrets in GitHub Secrets (never in code)
- Use different accounts for each industry if possible
- Enable 2FA on all accounts
- Use descriptive but non-sensitive secret names
- Test each API integration individually

### **❌ DON'T:**
- Commit API keys to repository
- Share tokens in plain text
- Use the same password for multiple accounts
- Store credentials in environment files that might be committed

## 🧪 **Testing Setup**

### **Validate All Credentials:**
```bash
# Run credential validation script:
python validate_credentials.py

# Expected output:
# ✅ Telegram Legal: Bot verified
# ✅ Telegram Medical: Bot verified  
# ✅ Telegram Senior: Bot verified
# ✅ Telegram General: Bot verified
# ✅ ConvertKit: API key valid, 4 forms found
# ✅ Gumroad: API key valid, 4 products found
# ✅ Google Cloud: Natural Language API accessible
# 🎉 All credentials configured correctly!
```

## 📊 **Cost Breakdown (90 days)**

| Service | Cost | Usage |
|---------|------|-------|
| Telegram | $0 | Unlimited (free) |
| Ko-fi | $0 | 0% fees on donations |
| ConvertKit | $0 | Free tier (10K subscribers) |
| Gumroad | 10% per sale | Revenue-based |
| Google Cloud | ~$50-80 | Natural Language API calls |
| **Total** | **~$50-80** | **For 90 days of automation** |

## 🎯 **Next Steps**

1. ✅ **Setup all accounts** (30-45 minutes)
2. ✅ **Configure GitHub Secrets** (10 minutes)
3. ✅ **Run validation test** (5 minutes)
4. ✅ **Trigger first manual workflow** (test)
5. ✅ **Monitor automated publishing** (3x daily)

**Total setup time: ~45 minutes for complete 12-channel automation system** 🚀