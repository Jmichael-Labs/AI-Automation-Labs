# 🔐 GITHUB SECRETS REQUERIDOS PARA VEO 3

## ⚠️ CONFIGURACIÓN CRÍTICA NECESARIA

Para que Veo 3 funcione en GitHub Actions, debes configurar estos secrets:

### 📋 SECRETS REQUERIDOS:

1. **GOOGLE_APPLICATION_CREDENTIALS**
   - Contenido del archivo JSON de service account
   - Proyecto: youtube-pro-469213
   - Debe tener permisos para Vertex AI

2. **TELEGRAM_GENERAL_TOKEN** (ya configurado)
   - Token del bot de Telegram

3. **REDDIT_CLIENT_ID** (ya configurado)
4. **REDDIT_CLIENT_SECRET** (ya configurado) 
5. **REDDIT_USERNAME** (ya configurado)
6. **REDDIT_PASSWORD** (ya configurado)
7. **EMAIL_CONTACT** (ya configurado)

## 🚨 PROBLEMA ACTUAL:

**Veo 3 falla porque GitHub Actions no tiene acceso al service account JSON.**

Sin `GOOGLE_APPLICATION_CREDENTIALS`, el GenAI Client no puede autenticarse con Vertex AI.

## ✅ SOLUCIÓN:

1. Ve a: GitHub Repository → Settings → Secrets and variables → Actions
2. Agrega: `GOOGLE_APPLICATION_CREDENTIALS` 
3. Valor: Todo el contenido del archivo JSON de service account

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