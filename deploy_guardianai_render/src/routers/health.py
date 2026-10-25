"""
Router de Health Check e Status da Aplicação
"""
from typing import Dict, Any
from fastapi import APIRouter
from src.core.config import AI_PROVIDER, GROQ_MODEL, GEMINI_MODEL, APP_TITLE, APP_VERSION

health_router = APIRouter(tags=["Health"])

@health_router.get("/")
def health_check() -> Dict[str, Any]:
    """
    Retorna o status operacional do microsserviço de IA e versões de motor.
    """
    return {
        "status": "online",
        "service": APP_TITLE,
        "provider": AI_PROVIDER,
        "model": f"{GROQ_MODEL if AI_PROVIDER == 'groq' else GEMINI_MODEL} / Semantic Knowledge Engine",
        "framework": "FastAPI + Clean Mobile Pipeline",
        "version": APP_VERSION
    }
