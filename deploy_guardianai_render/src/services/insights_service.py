"""
Serviço de Geração de Insights Clínico-Preventivos
"""
from typing import List
from src.schemas.pet import PetContextPayload
from src.schemas.insights import InsightItem, InsightsResponse
from src.services.knowledge_service import KnowledgeService

class InsightsService:
    """
    Coordena a geração de recomendações e alertas preventivos personalizados
    para o perfil do animal com base em porte e faixa etária.
    """

    @staticmethod
    def gerar_insights(pet: PetContextPayload) -> InsightsResponse:
        nome_pet = pet.nome or "Seu pet"
        porte = pet.porte or "medio"
        idade = pet.idade if pet.idade is not None else 3
        faixa = "senior" if idade >= 7 else ("filhote" if idade <= 1 else "adulto")

        dados = KnowledgeService.consultar_cuidados_porte_idade(porte, faixa)

        insights_list: List[InsightItem] = [
            InsightItem(
                categoria="saude",
                titulo=f"Cuidado Preventivo ({dados['fase_vida']})",
                descricao=dados["alerta_porte"],
                urgencia="baixa" if faixa != "senior" else "media"
            ),
            InsightItem(
                categoria="nutricao",
                titulo="Manejo Alimentar & Nutrição",
                descricao=dados["recomendacao_nutricional"],
                urgencia="baixa"
            ),
            InsightItem(
                categoria="rotina",
                titulo="Protocolo Veterinário Periódico",
                descricao=dados["protocolo_veterinario"],
                urgencia="baixa"
            )
        ]

        return InsightsResponse(insights=insights_list)
