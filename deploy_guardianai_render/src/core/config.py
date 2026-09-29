"""
Módulo Core: Configurações Globais da Aplicação
"""
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env se presente
load_dotenv()

# Metadados e versão
APP_TITLE = "PetGuardian / Clyvo Care — AI Microservice"
APP_DESCRIPTION = "API de IA Generativa e Triagem Preventiva para pets com respostas limpas e guardrails de segurança."
APP_VERSION = "2.0.0"

# Modelo Oficial de IA
MODEL_NAME = "gemini-3.5-flash-lite"

# Credenciais e Portas
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
PORT = int(os.environ.get("PORT", 8000))

# Configuração de CORS para comunicação fluida com Mobile (React Native / Expo) e Web
CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = False
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]
