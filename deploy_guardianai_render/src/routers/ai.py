"""
Router de IA Generativa, Triagem Clínica Preventiva e Persistência SQLite
"""
from typing import Optional
from fastapi import APIRouter, Query
from src.schemas.chat import (
    ChatRequest,
    ChatResponse,
    HistoricoResponse,
    AuditoriaResponse,
    MensagemBancoItem,
    AuditoriaBancoItem,
    SessaoItem,
    SessoesResponse
)
from src.schemas.pet import PetContextPayload
from src.schemas.insights import InsightsResponse
from src.services.chat_service import ChatService
from src.services.insights_service import InsightsService
from src.repositories.chat_repository import ChatRepository

ai_router = APIRouter(prefix="/ai", tags=["AI"])

@ai_router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Processa interação no chat clínico com contexto do animal e histórico multi-turnos,
    persistindo automaticamente a conversa e a auditoria da triagem no SQLite.
    """
    return ChatService.processar_chat(request)

@ai_router.post("/insights", response_model=InsightsResponse)
async def insights_endpoint(pet: PetContextPayload) -> InsightsResponse:
    """
    Gera insights preventivos personalizados de acordo com porte e idade do animal.
    """
    return InsightsService.gerar_insights(pet)

@ai_router.get("/history", response_model=HistoricoResponse)
def buscar_historico_endpoint(
    session_id: Optional[str] = Query(None, description="Filtrar por ID da sessão"),
    pet_id: Optional[int] = Query(None, description="Filtrar por ID do pet"),
    limit: int = Query(50, ge=1, le=200, description="Limite máximo de mensagens")
) -> HistoricoResponse:
    """
    Consulta o histórico de mensagens gravadas no SQLite por sessão ou por pet.
    """
    dados = ChatRepository.buscar_historico(session_id=session_id, pet_id=pet_id, limit=limit)
    itens = [MensagemBancoItem(**row) for row in dados]
    return HistoricoResponse(total=len(itens), mensagens=itens)

@ai_router.get("/audit", response_model=AuditoriaResponse)
def listar_auditorias_endpoint(
    pet_id: Optional[int] = Query(None, description="Filtrar por ID do pet"),
    limit: int = Query(20, ge=1, le=100, description="Limite máximo de auditorias")
) -> AuditoriaResponse:
    """
    Consulta as últimas triagens clínicas auditadas no banco de dados SQLite.
    """
    dados = ChatRepository.listar_auditorias(pet_id=pet_id, limit=limit)
    itens = [AuditoriaBancoItem(**row) for row in dados]
    return AuditoriaResponse(total=len(itens), auditorias=itens)

@ai_router.get("/sessions", response_model=SessoesResponse)
def listar_sessoes_endpoint(
    pet_id: Optional[int] = Query(None, description="Filtrar sessões por ID do pet"),
    limit: int = Query(30, ge=1, le=100, description="Limite de sessões retornadas")
) -> SessoesResponse:
    """
    Lista as conversas anteriores do pet (estilo ChatGPT/Claude) agrupadas por sessão,
    com título da 1ª pergunta, total de mensagens e data da última interação.
    """
    dados = ChatRepository.listar_sessoes(pet_id=pet_id, limit=limit)
    itens = [SessaoItem(**row) for row in dados]
    return SessoesResponse(total=len(itens), sessoes=itens)

@ai_router.delete("/sessions/{session_id}")
def excluir_sessao_endpoint(session_id: str) -> dict:
    """
    Exclui permanentemente uma sessão de conversa do histórico e da auditoria SQLite.
    """
    sucesso = ChatRepository.excluir_sessao(session_id)
    return {"status": "ok" if sucesso else "error", "session_id": session_id}
