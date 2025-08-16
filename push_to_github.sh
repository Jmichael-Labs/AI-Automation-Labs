#!/bin/bash
echo "🚀 Subiendo Reddit AI Bot a GitHub..."
echo "Repositorio: github.com/Jmichael-Labs/reddit-ai-problem-solver"
echo ""

cd "/Volumes/DiskExFAT 1/reddit_ai_bot_production"

# Check if repository exists remotely
echo "📋 Verificando repositorio remoto..."
git ls-remote origin > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Repositorio existe, haciendo push..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 ¡SUCCESS! Bot subido a GitHub"
        echo "🔗 URL: https://github.com/Jmichael-Labs/reddit-ai-problem-solver"
        echo ""
        echo "📋 Próximos pasos:"
        echo "1. Ir a render.com"
        echo "2. New Web Service"
        echo "3. Connect GitHub → reddit-ai-problem-solver"
        echo "4. Configurar environment variables"
        echo "5. Deploy!"
    else
        echo "❌ Error en push. Verifica credenciales GitHub."
    fi
else
    echo "❌ Repositorio no existe. Créalo primero en GitHub:"
    echo "   1. github.com/Jmichael-Labs"
    echo "   2. New repository"
    echo "   3. Name: reddit-ai-problem-solver"
    echo "   4. Private ✅"
    echo "   5. Don't initialize with README"
    echo "   6. Create repository"
    echo ""
    echo "Luego ejecuta este script nuevamente."
fi