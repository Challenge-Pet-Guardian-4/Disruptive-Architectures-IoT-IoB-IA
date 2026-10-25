"""
Pacote Knowledge: Base de Conhecimento Estruturada em Chunks — Pet Guardian
"""
from typing import List, Dict, Any
from src.knowledge.toxicology import CHUNKS_TOXICOLOGY
from src.knowledge.preventive_care import CHUNKS_PREVENTIVE_CARE
from src.knowledge.faq import CHUNKS_FAQ
from src.knowledge.behavior import CHUNKS_BEHAVIOR
from src.knowledge.hygiene_skin import CHUNKS_HYGIENE_SKIN
from src.knowledge.reproduction import CHUNKS_REPRODUCTION
from src.knowledge.lifestyle import CHUNKS_LIFESTYLE
from src.knowledge.infectious_diseases import CHUNKS_INFECTIOUS_DISEASES

# Consolidação unificada de todos os chunks da Base de Conhecimento Pet Guardian
BASE_CHUNKS_RAG: List[Dict[str, Any]] = (
    CHUNKS_TOXICOLOGY +
    CHUNKS_PREVENTIVE_CARE +
    CHUNKS_FAQ +
    CHUNKS_BEHAVIOR +
    CHUNKS_HYGIENE_SKIN +
    CHUNKS_REPRODUCTION +
    CHUNKS_LIFESTYLE +
    CHUNKS_INFECTIOUS_DISEASES
)

__all__ = [
    "CHUNKS_TOXICOLOGY",
    "CHUNKS_PREVENTIVE_CARE",
    "CHUNKS_FAQ",
    "CHUNKS_BEHAVIOR",
    "CHUNKS_HYGIENE_SKIN",
    "CHUNKS_REPRODUCTION",
    "CHUNKS_LIFESTYLE",
    "CHUNKS_INFECTIOUS_DISEASES",
    "BASE_CHUNKS_RAG",
]
