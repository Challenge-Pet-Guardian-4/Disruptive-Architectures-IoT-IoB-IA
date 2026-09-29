"""
Pacote Knowledge: Bases de Conhecimento em Memória
"""
from src.knowledge.toxicology import BASE_ALIMENTOS_TOXICOS
from src.knowledge.preventive_care import BASE_CUIDADOS_PORTE_IDADE, BASE_FAIXA_ETARIA
from src.knowledge.faq import BASE_RESPOSTAS_COTIDIANAS

__all__ = [
    "BASE_ALIMENTOS_TOXICOS",
    "BASE_CUIDADOS_PORTE_IDADE",
    "BASE_FAIXA_ETARIA",
    "BASE_RESPOSTAS_COTIDIANAS",
]
