"""
Schemas Pydantic: Conversação, Chat e Auditoria da IA
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from src.schemas.pet import PetContextPayload

class MensagemHistorico(BaseModel):
    sender: str = Field(..., description="Remetente da mensagem: 'user' ou 'assistant'/'model'")
    text: str = Field(..., description="Conteúdo textual da mensagem")

class ChatRequest(BaseModel):
    pergunta: str = Field(..., description="Dúvida, queixa ou relato enviado pelo tutor")
    petContext: Optional[PetContextPayload] = Field(default=None, description="Contexto biológico e clínico do pet ativo")
    historico: Optional[List[MensagemHistorico]] = Field(default=None, description="Histórico de mensagens recentes para memória conversacional")
    sessionId: Optional[str] = Field(default=None, description="Identificador único opcional da sessão")

class ChatResponse(BaseModel):
    resposta: str = Field(..., description="Resposta processada e sanitizada para visualização mobile")
    categoria: str = Field(default="saude", description="Categoria clínica: 'saude', 'nutricao', 'rotina', 'EMERGENCIA'")
    urgencia: str = Field(default="baixa", description="Classificação de gravidade: 'baixa', 'media', 'alta', 'EMERGENCIA'")
    acoes_recomendadas: Optional[List[str]] = Field(default=None, description="Orientações e checklist de ações sugeridas para o tutor")
    origem_resposta: str = Field(default="Guardian AI (PetGuardian Care)", description="Identificador do mecanismo responsável pela geração da resposta")
    sessionId: Optional[str] = Field(default=None, description="Identificador da sessão ativa no banco de dados")

class MensagemBancoItem(BaseModel):
    id: int = Field(..., description="ID sequencial da mensagem")
    session_id: str = Field(..., description="ID da sessão")
    pet_id: Optional[int] = Field(default=None, description="ID do pet associado")
    sender: str = Field(..., description="Remetente: 'user' ou 'model'")
    text: str = Field(..., description="Conteúdo da mensagem")
    timestamp: Optional[str] = Field(default=None, description="Data/hora do registro")

class AuditoriaBancoItem(BaseModel):
    id: int = Field(..., description="ID sequencial da auditoria")
    session_id: str = Field(..., description="ID da sessão")
    pet_id: Optional[int] = Field(default=None, description="ID do pet")
    nome_pet: Optional[str] = Field(default=None, description="Nome do pet")
    pergunta: str = Field(..., description="Pergunta do tutor")
    resposta: str = Field(..., description="Resposta clínica fornecida")
    categoria: str = Field(..., description="Categoria clínica")
    urgencia: str = Field(..., description="Nível de urgência")
    origem_resposta: str = Field(..., description="Origem da resposta")
    timestamp: Optional[str] = Field(default=None, description="Data/hora do registro")

class HistoricoResponse(BaseModel):
    total: int = Field(..., description="Total de mensagens retornadas")
    mensagens: List[MensagemBancoItem] = Field(..., description="Lista de mensagens da sessão ou pet")

class AuditoriaResponse(BaseModel):
    total: int = Field(..., description="Total de registros de auditoria retornados")
    auditorias: List[AuditoriaBancoItem] = Field(..., description="Lista de pareceres de triagem auditados")

class SessaoItem(BaseModel):
    session_id: str = Field(..., description="Identificador único da sessão de chat")
    titulo: str = Field(..., description="Título resumido da conversa (primeira pergunta do tutor)")
    total_mensagens: int = Field(default=0, description="Total de mensagens trocadas na conversa")
    last_activity: Optional[str] = Field(default=None, description="Data e hora da última interação")

class SessoesResponse(BaseModel):
    total: int = Field(..., description="Total de sessões encontradas")
    sessoes: List[SessaoItem] = Field(..., description="Lista de sessões de conversas anteriores")
