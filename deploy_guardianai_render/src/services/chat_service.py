"""
Serviço Orquestrador do Chat Clínico PetGuardian com RAG Vetorial e Persistência SQLite
"""
import uuid
from typing import Optional, List, Dict, Any
from src.core.config import MODEL_NAME
from src.core.prompts import formatar_prompt_rag
from src.schemas.chat import ChatRequest, ChatResponse, RetrievedSource
from src.services.knowledge_service import KnowledgeService
from src.services.groq_service import GroqService
from src.services.gemini_service import GeminiService
from src.repositories.chat_repository import ChatRepository
from src.utils.text import limpar_texto_mobile, normalizar_texto
from src.utils.guardrails import detectar_pedido_programacao, sanitizar_resposta_anti_codigo

class ChatService:
    """
    Orquestra o pipeline completo de triagem e conversação com RAG:
    1. Guardrail farmacológico emergencial vital (Paracetamol em felinos)
    2. Recuperação vetorial de trechos (RAG) por Similaridade de Cosseno em espaço contínuo de Embeddings
    3. Construção de Prompt Fundamentado (System Prompt + Contexto do Pet + RAG Chunks + Anti-Alucinação)
    4. Inferência generativa primária via Groq Cloud (LPU openai/gpt-oss-120b com fallback Gemini)
    5. Fallback fundamentado direto da Base de Conhecimento Pet Guardian
    6. Blindagem de domínio contra evasão de escopo (tentativas de código / programação)
    7. Persistência de mensagens, auditoria de triagem e fontes utilizadas no SQLite (Fail-safe)
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

        # 1. Guardrail de Segurança Farmacológica Crítica (Paracetamol em Gatos)
        if "paracetamol" in pergunta_norm and any(k in pergunta_norm for k in ["gato", "felino", "mingau", "gatinho"]):
            texto_limpo = limpar_texto_mobile(
                "⛔ ALERTA VITAL: NUNCA DÊ PARACETAMOL PARA UM GATO!\n\n"
                "Segundo o Protocolo de Farmacovigilância Pet Guardian, o Paracetamol é ALTAMENTE LETAL PARA FELINOS mesmo em doses mínimas infantis. "
                "Os gatos possuem deficiência congênita na enzima glucuronil-transferase, causando meta-hemoglobinemia (asfixia interna) "
                "e necrose hepática fulminante em poucas horas.\n\n"
                "🚨 O que fazer agora:\n"
                "• Não administre nenhum medicamento caseiro ou humano.\n"
                "• Se o animal ingeriu acidentalmente, leve IMEDIATAMENTE ao pronto-socorro veterinário 24h Pet Guardian."
            )
            resp = ChatResponse(
                resposta=texto_limpo,
                categoria="EMERGENCIA",
                urgencia="EMERGENCIA",
                acoes_recomendadas=["Não medicar em casa", "Procurar clínica veterinária urgente"],
                origem_resposta="Guardrail de Segurança Farmacológica PetGuardian",
                sources_used=[
                    RetrievedSource(
                        id="tox_12",
                        source="Protocolo de Toxicologia Pet Guardian",
                        category="toxicology",
                        title="Veto Absoluto a Medicamentos Humanos (Paracetamol, Ibuprofeno e Dipirona)",
                        similarity_score=1.0
                    )
                ],
                rag_grounded=True
            )
            return cls._finalizar_e_persistir(resp, request, session_id, pet_id, nome_pet)

        # 2. Recuperação de Chunks da Base de Conhecimento via RAG (Embeddings Vetoriais + Similaridade de Cosseno)
        resultado_rag = KnowledgeService.buscar_chunks_rag(request.pergunta, top_k=3, min_score=0.18)
        chunks_recuperados = resultado_rag["chunks"]
        match_found = resultado_rag["match_found"]

        sources_used = [
            RetrievedSource(
                id=c["id"],
                source=c["source"],
                category=c["category"],
                title=c["title"],
                similarity_score=c["similarity_score"]
            )
            for c in chunks_recuperados
        ]

        # 3. Construção do Contexto Estruturado do Pet
        contexto_pet_str = ""
        if request.petContext and request.petContext.nome:
            p = request.petContext
            partes_contexto = [
                f"Nome: {p.nome}",
                f"Raça: {p.raca or 'SRD'}",
                f"Porte: {p.porte or 'médio'}",
                f"Idade: {p.idade if p.idade is not None else 'não informada'} anos",
                f"Peso: {p.peso or 'não informado'} kg"
            ]
            if p.alergias:
                partes_contexto.append(f"Alergias Conhecidas: {p.alergias}")
            if p.medicamentos:
                partes_contexto.append(f"Medicamentos Contínuos: {p.medicamentos}")
            if p.ultimaVacina:
                partes_contexto.append(f"Última Vacina: {p.ultimaVacina}")
            contexto_pet_str = "[Dados do Pet Ativo: " + ", ".join(partes_contexto) + "]"

        # 4. Montagem do Prompt Fundamentado (RAG Prompt Template)
        prompt_fundamentado = formatar_prompt_rag(
            pergunta=request.pergunta,
            contexto_pet_str=contexto_pet_str,
            chunks_recuperados=chunks_recuperados,
            match_found=match_found
        )

        eh_pedido_programacao = detectar_pedido_programacao(request.pergunta)
        origem_ia = f"Guardian AI (Groq: {MODEL_NAME} + RAG)"

        # 5. Inferência Generativa Primária (Groq Cloud LPU)
        resposta_ia = GroqService.gerar_resposta(prompt_fundamentado, request.historico)

        # 5.1. Fallback de Contingência: Google Gemini (caso Groq oscile ou atinja cota)
        if not resposta_ia:
            resposta_ia = GeminiService.gerar_resposta(prompt_fundamentado, request.historico)
            if resposta_ia:
                origem_ia = "Guardian AI (Fallback Gemini + RAG)"

        # 6. Processamento da Resposta Generativa
        if resposta_ia:
            texto_sem_codigo = sanitizar_resposta_anti_codigo(resposta_ia, eh_pedido_programacao)
            texto_limpo = limpar_texto_mobile(texto_sem_codigo)

            # Classificação de severidade e ações baseadas nos chunks RAG ou na resposta
            eh_emergencia = (
                any(c.get("category") == "toxicology" for c in chunks_recuperados) or
                "emergencia" in texto_limpo.lower() or
                ("hospital" in texto_limpo.lower() and "24h" in texto_limpo.lower())
            )

            categoria_val = "EMERGENCIA" if eh_emergencia else "saude"
            urgencia_val = "EMERGENCIA" if eh_emergencia else "baixa"
            acoes = (
                ["Levar imediatamente ao hospital 24h", "Não induzir vômito caseiro"]
                if eh_emergencia else
                ["Acompanhar o bem-estar", "Consultar equipe médica da Pet Guardian"]
            )

            resp = ChatResponse(
                resposta=texto_limpo,
                categoria=categoria_val,
                urgencia=urgencia_val,
                acoes_recomendadas=acoes,
                origem_resposta=origem_ia,
                sources_used=sources_used,
                rag_grounded=match_found
            )
            return cls._finalizar_e_persistir(resp, request, session_id, pet_id, nome_pet)

        # 7. Fallback Fundamentado Direto em Chunks RAG (quando as LLMs externas estão indisponíveis)
        if match_found and chunks_recuperados:
            top_chunk = chunks_recuperados[0]
            texto_fallback_rag = (
                f"Segundo o {top_chunk['source']} ({top_chunk['title']}):\n\n"
                f"{top_chunk['content']}\n\n"
                f"💡 Para um parecer personalizado sobre o {nome_pet}, procure o atendimento da Pet Guardian."
            )
            if eh_pedido_programacao:
                texto_fallback_rag = sanitizar_resposta_anti_codigo(texto_fallback_rag, True)

            eh_emergencia = top_chunk["category"] == "toxicology"
            resp = ChatResponse(
                resposta=limpar_texto_mobile(texto_fallback_rag),
                categoria="EMERGENCIA" if eh_emergencia else "saude",
                urgencia="EMERGENCIA" if eh_emergencia else "baixa",
                acoes_recomendadas=["Buscar suporte veterinário presencial", "Seguir protocolo da Pet Guardian"],
                origem_resposta="Guardian AI (Base RAG Determinística Pet Guardian)",
                sources_used=sources_used,
                rag_grounded=True
            )
            return cls._finalizar_e_persistir(resp, request, session_id, pet_id, nome_pet)

        # 8. Se for pergunta de programação fora de escopo sem match na base
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
                origem_resposta="Guardrail Anti-Pretexto e Blindagem de Domínio",
                sources_used=[],
                rag_grounded=False
            )
            return cls._finalizar_e_persistir(resp, request, session_id, pet_id, nome_pet)

        # 9. Fallback Preventivo Contextual por Porte e Idade (quando não há match na base nem LLM online)
        porte_req = request.petContext.porte if request.petContext and request.petContext.porte else "medio"
        idade_num = request.petContext.idade if request.petContext and request.petContext.idade is not None else 3
        faixa_calc = "senior" if idade_num >= 7 else ("filhote" if idade_num <= 1 else "adulto")
        dados_cuidado = KnowledgeService.consultar_cuidados_porte_idade(porte_req, faixa_calc)

        resposta_contextual = (
            f"Olá! Analisei sua dúvida sobre o {nome_pet} ({dados_cuidado['fase_vida']}).\n\n"
            f"🐾 De acordo com o Guia de Cuidados Preventivos Pet Guardian:\n"
            f"• Nutrição & Manejo: {dados_cuidado['recomendacao_nutricional']}\n"
            f"• Cuidados Clínicos: {dados_cuidado['alerta_porte']}\n"
            f"• Protocolo Preventivo: {dados_cuidado['protocolo_veterinario']}\n\n"
            f"Essa dúvida específica não consta na base consultada. Para diagnósticos ou sintomas clínicos, consulte a Pet Guardian."
        )

        resp = ChatResponse(
            resposta=limpar_texto_mobile(resposta_contextual),
            categoria="saude",
            urgencia="baixa",
            acoes_recomendadas=["Check-up periódico", "Rotina de bem-estar ativa"],
            origem_resposta="Guardian AI (Mecanismo Preventivo Pet Guardian)",
            sources_used=[],
            rag_grounded=False
        )
        return cls._finalizar_e_persistir(resp, request, session_id, pet_id, nome_pet)
