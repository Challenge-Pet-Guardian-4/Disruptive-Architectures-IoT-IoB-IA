"""
Módulo Core: Configurações Globais da Aplicação
"""
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Metadados e versão
APP_TITLE = "PetGuardian — AI Microservice"
APP_DESCRIPTION = "API de IA Generativa e Triagem Preventiva para pets com respostas limpas e guardrails de segurança."
APP_VERSION = "2.0.0"

# Provedor e Modelo Oficial de IA
AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")
MODEL_NAME = os.environ.get("MODEL_NAME", "openai/gpt-oss-120b")
FALLBACK_MODEL_NAME = os.environ.get("FALLBACK_MODEL_NAME", "gemini-3.5-flash-lite")

# Credenciais e Portas
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
PORT = int(os.environ.get("PORT", 8000))

# Configuração de CORS para comunicação fluida com Mobile (React Native / Expo) e Web
CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = False
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]
