"""
Serviço Orquestrador do Chat Clínico PetGuardian com Persistência SQLite
"""
import uuid
from typing import Optional, List, Dict, Any
from src.core.config import MODEL_NAME
from src.schemas.chat import ChatRequest, ChatResponse
from src.services.knowledge_service import KnowledgeService
from src.services.gemini_service import GeminiService
from src.repositories.chat_repository import ChatRepository
from src.utils.text import limpar_texto_mobile, normalizar_texto
from src.utils.guardrails import detectar_pedido_programacao, sanitizar_resposta_anti_codigo

class ChatService:
    """
    Orquestra o pipeline de triagem e conversação:
    1. Guardrail farmacológico emergencial (Paracetamol em felinos)
    2. Guardrail toxicológico determinístico (Alimentos proibidos)
    3. Inferência generativa contextual (Gemini) com histórico deslizante
    4. Fallback semântico (FAQ cotidiana)
    5. Blindagem contra evasão de domínio (Prompt injection de código)
    6. Fallback clínico contextual por porte e idade
    7. Persistência de mensagens e auditoria no SQLite (Fail-safe)
    """

    @classmethod
    def _finalizar_e_persistir(
        cls,
        response: ChatResponse,
        request: ChatRequest,
        session_id: str,
        pet_id: Optional[int],
        nome_pet: Optional[str]
    ) -> ChatResponse:
        """
        Atribui o sessionId ao response e grava o histórico e o parecer de auditoria no SQLite.
        """
        response.sessionId = session_id

        # Persistência assíncrona/segura no SQLite
        ChatRepository.salvar_mensagem(
            session_id=session_id,
            sender="user",
            text=request.pergunta,
            pet_id=pet_id
        )
        ChatRepository.salvar_mensagem(
            session_id=session_id,
            sender="model",
            text=response.resposta,
            pet_id=pet_id
        )
        ChatRepository.salvar_auditoria(
            session_id=session_id,
            pergunta=request.pergunta,
            resposta=response.resposta,
            categoria=response.categoria,
            urgencia=response.urgencia,
            origem_resposta=response.origem_resposta,
            pet_id=pet_id,
            nome_pet=nome_pet
        )

        return response

    @classmethod
    def processar_chat(cls, request: ChatRequest) -> ChatResponse:
        session_id = request.sessionId or f"sess_{uuid.uuid4().hex[:12]}"
        pet_id = request.petContext.id if request.petContext else None
        nome_pet = request.petContext.nome if request.petContext and request.petContext.nome else "seu pet"
        pergunta_norm = normalizar_texto(request.pergunta)

        # 1. Guardrail de Segurança Farmacológica / Paracetamol em Gatos (apenas pergunta atual)
        if "paracetamol" in pergunta_norm and any(k in pergunta_norm for k in ["gato", "felino", "mingau", "gatinho"]):
            texto_limpo = limpar_texto_mobile(
                "⛔ ALERTA VITAL: NUNCA DÊ PARACETAMOL PARA UM GATO!\n\n"
                "O Paracetamol é ALTAMENTE LETAL PARA FELINOS mesmo em doses mínimas. Os gatos não possuem a enzima necessária para metabolizar o medicamento, causando destruição rápida das hemácias (asfixia interna) e necrose hepática fulminante em poucas horas.\n\n"
                "🚨 O que fazer agora:\n"
                "• Não administre nenhum medicamento caseiro ou humano.\n"
                "• Se o animal ingeriu acidentalmente, leve IMEDIATAMENTE a um pronto-socorro veterinário 24h."
            )
            resp = ChatResponse(
                resposta=texto_limpo,
                categoria="EMERGENCIA",
                urgencia="EMERGENCIA",
                acoes_recomendadas=["Não medicar em casa", "Procurar clínica veterinária urgente"],
                origem_resposta="Guardrail de Segurança Farmacológica PetGuardian"
            )
            return cls._finalizar_e_persistir(resp, request, session_id, pet_id, nome_pet)

        # 2. Verificação de Alimentos Tóxicos Críticos
        dados_tox = KnowledgeService.verificar_alimento_toxico(request.pergunta)
        if dados_tox:
            chave = dados_tox["alimento"]
            urgencia_val = dados_tox["nivel_risco"]
            texto_alerta = (
                f"🚨 ALERTA TOXICOLÓGICO: {chave.upper()} É PERIGOSO PARA PETS!\n\n"
                f"• Toxina: {dados_tox['toxina']}\n"
                f"• Efeito no organismo: {dados_tox['mecanismo']}\n"
                f"• Sintomas de alerta: {dados_tox['sintomas']}\n\n"
                f"👉 Conduta recomendada: {dados_tox['conduta_imediata']}"
            )
            resp = ChatResponse(
                resposta=limpar_texto_mobile(texto_alerta),
                categoria="EMERGENCIA" if urgencia_val == "EMERGENCIA" else "SAUDE",
                urgencia=urgencia_val,
                acoes_recomendadas=["Levar ao hospital 24h", "Não induzir vômito caseiro"],
                origem_resposta="Base de Toxicologia Determinística PetGuardian"
            )
            return cls._finalizar_e_persistir(resp, request, session_id, pet_id, nome_pet)

        # 3. Tentativa de Inferência via Gemini com Memória Multi-turnos e Janela Deslizante
        contexto_pet_str = ""
        if request.petContext and request.petContext.nome:
            p = request.petContext
            contexto_pet_str = (
                f"[Dados do Pet: Nome={p.nome}, Raça={p.raca or 'SRD'}, "
                f"Porte={p.porte or 'médio'}, Idade={p.idade or 'não informada'} anos, "
                f"Peso={p.peso or 'não informado'}kg, Alergias={p.alergias or 'nenhuma'}]"
            )

        eh_pedido_programacao = detectar_pedido_programacao(request.pergunta)
        prompt_atual = f"{contexto_pet_str}\n\nPergunta do Tutor: {request.pergunta}" if contexto_pet_str else request.pergunta

        resposta_ia = GeminiService.gerar_resposta(prompt_atual, request.historico)
        if resposta_ia:
            texto_sem_codigo = sanitizar_resposta_anti_codigo(resposta_ia, eh_pedido_programacao)
            texto_limpo = limpar_texto_mobile(texto_sem_codigo)
            resp = ChatResponse(
                resposta=texto_limpo,
                categoria="saude",
                urgencia="baixa",
                acoes_recomendadas=["Acompanhar o bem-estar", "Manter hidratação regular"],
                origem_resposta=f"Guardian AI ({MODEL_NAME})"
            )
            return cls._finalizar_e_persistir(resp, request, session_id, pet_id, nome_pet)

        # 4. Fallback Semântico Inteligente para Perguntas Cotidianas
        dados_tema = KnowledgeService.consultar_faq_cotidiana(request.pergunta)
        if dados_tema:
            texto_base = dados_tema["resposta"]
            if eh_pedido_programacao:
                texto_base = sanitizar_resposta_anti_codigo(texto_base, True)
            resp = ChatResponse(
                resposta=limpar_texto_mobile(texto_base),
                categoria=dados_tema["categoria"],
                urgencia=dados_tema["urgencia"],
                acoes_recomendadas=["Manter rotina equilibrada", "Consultar veterinário em caso de dúvidas"],
                origem_resposta="Guardian AI (Base Semântica Especializada)"
            )
            return cls._finalizar_e_persistir(resp, request, session_id, pet_id, nome_pet)

        # 5. Se for puramente pergunta de programação fora de escopo sem tema pet correspondente
        if eh_pedido_programacao:
            resp = ChatResponse(
                resposta=limpar_texto_mobile(
                    "Como Guardian AI, sou dedicada exclusivamente à saúde, nutrição e bem-estar de cães e gatos. "
                    "Por isso, não forneço códigos, programação em Python ou instruções de desenvolvimento de software, "
                    "mesmo quando solicitados com o pet como pretexto!\n\n"
                    "Posso te ajudar com alguma orientação sobre alimentação, vacinas ou rotina de cuidados do seu pet?"
                ),
                categoria="saude",
                urgencia="baixa",
                acoes_recomendadas=["Dúvidas sobre nutrição animal", "Consultar rotina preventiva"],
                origem_resposta="Guardrail Anti-Pretexto e Blindagem de Domínio"
            )
            return cls._finalizar_e_persistir(resp, request, session_id, pet_id, nome_pet)

        # 6. Fallback Contextual por Porte e Idade
        porte_req = request.petContext.porte if request.petContext and request.petContext.porte else "medio"
        idade_num = request.petContext.idade if request.petContext and request.petContext.idade is not None else 3
        faixa_calc = "senior" if idade_num >= 7 else ("filhote" if idade_num <= 1 else "adulto")
        dados_cuidado = KnowledgeService.consultar_cuidados_porte_idade(porte_req, faixa_calc)

        resposta_contextual = (
            f"Olá! Analisei sua dúvida sobre o {nome_pet} ({dados_cuidado['fase_vida']}).\n\n"
            f"🐾 Orientações para a fase atual do {nome_pet}:\n"
            f"• Nutrição & Manejo: {dados_cuidado['recomendacao_nutricional']}\n"
            f"• Cuidados Clínicos: {dados_cuidado['alerta_porte']}\n"
            f"• Protocolo Preventivo: {dados_cuidado['protocolo_veterinario']}\n\n"
            f"Para diagnósticos específicos, alterações de comportamento ou sintomas agudos, consulte sempre um médico-veterinário presencial."
        )

        resp = ChatResponse(
            resposta=limpar_texto_mobile(resposta_contextual),
            categoria="saude",
            urgencia="baixa",
            acoes_recomendadas=["Check-up periódico", "Rotina de bem-estar ativa"],
            origem_resposta="Guardian AI (Mecanismo Preventivo)"
        )
        return cls._finalizar_e_persistir(resp, request, session_id, pet_id, nome_pet)
