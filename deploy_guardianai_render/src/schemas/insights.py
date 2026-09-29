"""
Schemas Pydantic: Insights Preventivos de Saúde
"""
from typing import List
from pydantic import BaseModel, Field

class InsightItem(BaseModel):
    categoria: str = Field(..., description="Eixo do insight: 'saude', 'nutricao' ou 'rotina'")
    titulo: str = Field(..., description="Título conciso do insight preventivo")
    descricao: str = Field(..., description="Recomendação detalhada e personalizada")
    urgencia: str = Field(..., description="Nível de atenção: 'baixa' ou 'media'")

class InsightsResponse(BaseModel):
    insights: List[InsightItem] = Field(..., description="Lista de insights preventivos gerados para o animal")
