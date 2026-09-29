"""
Router de Health Check e Status da Aplicação
"""
from typing import Dict, Any
from fastapi import APIRouter
from src.core.config import MODEL_NAME, APP_TITLE, APP_VERSION

health_router = APIRouter(tags=["Health"])

@health_router.get("/")
def health_check() -> Dict[str, Any]:
    """
    Retorna o status operacional do microsserviço de IA e versões de motor.
    """
    return {
        "status": "online",
        "service": APP_TITLE,
        "model": f"{MODEL_NAME} / Semantic Knowledge Engine",
        "framework": "FastAPI + Clean Mobile Pipeline",
        "version": APP_VERSION
    }
