"""
Serviço de Conhecimento: Consultas Determinísticas e Semânticas
"""
from typing import Optional, Dict, Any
from src.knowledge.toxicology import BASE_ALIMENTOS_TOXICOS
from src.knowledge.preventive_care import BASE_CUIDADOS_PORTE_IDADE, BASE_FAIXA_ETARIA
from src.knowledge.faq import BASE_RESPOSTAS_COTIDIANAS
from src.utils.text import normalizar_texto

class KnowledgeService:
    """
    Encapsula consultas determinísticas em memória para dados de toxicologia,
    protocolos clínicos preventivos por porte e idade e dúvidas cotidianas frequentes.
    """

    @staticmethod
    def verificar_alimento_toxico(pergunta: str) -> Optional[Dict[str, Any]]:
        """
        Varre a pergunta normalizada para identificar se cita algum alimento de risco catalogado.
        Retorna o dicionário de dados da toxina ou None.
        """
        pergunta_norm = normalizar_texto(pergunta)
        for chave, dados_tox in BASE_ALIMENTOS_TOXICOS.items():
            if chave in pergunta_norm:
                return {
                    "alimento": chave,
                    **dados_tox
                }
        return None

    @staticmethod
    def consultar_cuidados_porte_idade(porte: str, faixa_etaria: str) -> Dict[str, Any]:
        """
        Cruza o porte e a faixa etária do animal, retornando a matriz clínica preventiva.
        """
        porte_norm = normalizar_texto(porte)
        faixa_norm = normalizar_texto(faixa_etaria)
        
        if "gigante" in porte_norm:
            porte_norm = "grande"
        elif any(k in porte_norm for k in ["mini", "micro", "toy"]):
            porte_norm = "pequeno"

        if any(k in faixa_norm for k in ["idoso", "velho", "geriatrico", "senior"]):
            faixa_norm = "senior"
        elif any(k in faixa_norm for k in ["bebe", "puppy", "filhote"]):
            faixa_norm = "filhote"
        elif any(k in faixa_norm for k in ["jovem", "adulto"]):
            faixa_norm = "adulto"

        dados_porte = BASE_CUIDADOS_PORTE_IDADE.get(porte_norm, BASE_CUIDADOS_PORTE_IDADE["medio"])
        dados_faixa = BASE_FAIXA_ETARIA.get(faixa_norm, BASE_FAIXA_ETARIA["adulto"])

        return {
            "porte": porte_norm,
            "faixa_etaria": faixa_norm,
            "fase_vida": dados_faixa["fase"],
            "alerta_porte": dados_porte["alerta_clinico"],
            "recomendacao_nutricional": dados_porte["nutricao"],
            "cuidados_gerais": dados_porte["cuidados_gerais"],
            "protocolo_veterinario": dados_faixa["protocolo"],
            "estilo_de_vida": dados_faixa["socializacao"]
        }

    @staticmethod
    def consultar_faq_cotidiana(pergunta: str) -> Optional[Dict[str, Any]]:
        """
        Busca correspondência temática para perguntas cotidianas catalogadas.
        """
        pergunta_norm = normalizar_texto(pergunta)
        for chave_tema, dados_tema in BASE_RESPOSTAS_COTIDIANAS.items():
            if any(palavra in pergunta_norm for palavra in dados_tema["palavras_chave"]):
                return dados_tema
        return None
