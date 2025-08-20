# 🔐 GITHUB SECRETS REQUERIDOS PARA VEO 3

## ⚠️ CONFIGURACIÓN CRÍTICA CORREGIDA

**DESCUBRIMIENTO:** Veo 3 requiere **Gemini Developer API**, NO Vertex AI

### 📋 SECRETS REQUERIDOS:

1. **GEMINI_API_KEY** ⚡ CRÍTICO ⚡
   - API Key de Gemini Developer (no Vertex AI)
   - Obtener en: https://aistudio.google.com/app/apikey
   - Veo 3 solo funciona con Gemini Developer API

2. **TELEGRAM_GENERAL_TOKEN** (ya configurado)
   - Token del bot de Telegram

3. **REDDIT_CLIENT_ID** (ya configurado)
4. **REDDIT_CLIENT_SECRET** (ya configurado) 
5. **REDDIT_USERNAME** (ya configurado)
6. **REDDIT_PASSWORD** (ya configurado)
7. **EMAIL_CONTACT** (ya configurado)

## 🚨 PROBLEMA IDENTIFICADO:

**Error:** `This method is only supported in the Gemini Developer client.`

**Causa:** Configuramos Vertex AI, pero Veo 3 requiere Gemini Developer API.

## ✅ SOLUCIÓN CORRECTA:

### 🔑 OBTENER GEMINI API KEY:
1. Ve a: https://aistudio.google.com/app/apikey
2. Crea un nuevo API Key
3. Copia la key completa

### 📝 CONFIGURAR EN GITHUB:
1. Ve a: GitHub Repository → Settings → Secrets and variables → Actions  
2. Agrega: `GEMINI_API_KEY`
3. Valor: La API key completa de Gemini

## 🧪 VERIFICACIÓN:

Una vez configurado, el workflow ejecutará:
```bash
python test_veo3_simple.py
```

Esto confirmará si Vertex AI está autenticado correctamente.

## 📊 RESULTADO ESPERADO:

- ✅ Veo 3 videos reales generados
- ❌ No más videos mock de fallback
- 🎬 Videos concatenados completos de 24 segundos