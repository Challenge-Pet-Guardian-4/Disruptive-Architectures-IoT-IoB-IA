"""
Módulo Core: Configurações Globais da Aplicação
"""
import os
from pathlib import Path

def _carregar_env_manual(caminho: Path) -> None:
    """Fallback nativo para carregar arquivos .env caso python-dotenv não esteja instalado."""
    if not caminho.is_file():
        return
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha or linha.startswith("#") or "=" not in linha:
                    continue
                chave, valor = linha.split("=", 1)
                chave = chave.strip()
                valor = valor.strip().strip("'\"")
                if chave:
                    os.environ[chave] = valor
    except Exception:
        pass

# 1. Carrega via python-dotenv se disponível
try:
    from dotenv import load_dotenv  # type: ignore[import-not-found]  # pyright: ignore[reportMissingImports]
    load_dotenv()
except ImportError:
    pass

# 2. Garante o carregamento dos arquivos .env tanto na raiz quanto no deploy_guardianai_render
_dir_deploy = Path(__file__).resolve().parent.parent.parent
_env_deploy = _dir_deploy / ".env"
_env_raiz = _dir_deploy.parent / ".env"

if _env_deploy.is_file():
    _carregar_env_manual(_env_deploy)
elif _env_raiz.is_file():
    _carregar_env_manual(_env_raiz)

# Metadados e versão
APP_TITLE = "PetGuardian — AI Microservice"
APP_DESCRIPTION = "API de IA Generativa e Triagem Preventiva para pets com respostas limpas e guardrails de segurança."
APP_VERSION = "2.0.0"

# Modelos Padrão de Homologação da Sprint 4
DEFAULT_AI_PROVIDER = "groq"
DEFAULT_MODEL_NAME = "openai/gpt-oss-120b"
DEFAULT_FALLBACK_MODEL_NAME = "gemini-3.5-flash-lite"

# Provedor e Modelos Ativos:
# Usa prioritariamente o que o usuário configurou no .env; se vazio ou não informado, usa os modelos padrão
AI_PROVIDER = os.environ.get("AI_PROVIDER", "").strip() or DEFAULT_AI_PROVIDER
MODEL_NAME = os.environ.get("MODEL_NAME", "").strip() or DEFAULT_MODEL_NAME
FALLBACK_MODEL_NAME = os.environ.get("FALLBACK_MODEL_NAME", "").strip() or DEFAULT_FALLBACK_MODEL_NAME

# Credenciais e Portas
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
PORT = int(os.environ.get("PORT", 8000))

# Configuração de CORS para comunicação fluida com Mobile (React Native / Expo) e Web
CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = False
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]
