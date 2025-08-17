#!/bin/bash
# Smart Reddit Bot Auto Launcher
# Inicia el sistema inteligente de auto-posting

echo "🤖 JMichael Labs - Smart Reddit Bot Launcher"
echo "============================================="

# Change to bot directory
cd "/Volumes/DiskExFAT 1/reddit_ai_bot_production"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

# Check if requests module is available
if ! python3 -c "import requests" 2>/dev/null; then
    echo "📦 Installing requests module..."
    pip3 install requests
fi

echo "🚀 Starting Smart Auto Launcher..."
echo "⏱️  Will check every 30 minutes if bot should post"
echo "🎯 Posts when optimal (18-30 hour intervals)"
echo "⚠️  Press Ctrl+C to stop"
echo ""

# Start the smart launcher
python3 smart_auto_launcher.py