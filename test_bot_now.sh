#!/bin/bash
# Test Reddit Bot - Single Run
# Prueba el bot una sola vez

echo "🧪 Testing Reddit Bot - Single Run"
echo "================================="

cd "/Volumes/DiskExFAT 1/reddit_ai_bot_production"

echo "🎯 Running single smart check..."
python3 smart_auto_launcher.py --once

echo ""
echo "✅ Test completed. Check output above for results."