"""
Pacote Knowledge: Base de Conhecimento Estruturada em Chunks — Pet Guardian
"""
from typing import List, Dict, Any
from src.knowledge.toxicology import CHUNKS_TOXICOLOGY
from src.knowledge.preventive_care import CHUNKS_PREVENTIVE_CARE
from src.knowledge.faq import CHUNKS_FAQ

# Consolidação unificada de todos os chunks da Base de Conhecimento Pet Guardian
BASE_CHUNKS_RAG: List[Dict[str, Any]] = (
    CHUNKS_TOXICOLOGY +
    CHUNKS_PREVENTIVE_CARE +
    CHUNKS_FAQ
)

__all__ = [
    "CHUNKS_TOXICOLOGY",
    "CHUNKS_PREVENTIVE_CARE",
    "CHUNKS_FAQ",
    "BASE_CHUNKS_RAG",
]
