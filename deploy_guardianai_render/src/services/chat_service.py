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
        
        # Normalização defensiva: aceita petContext como objeto Pydantic ou dicionário
        if isinstance(request.petContext, dict):
            try:
                from src.schemas.pet import PetContextPayload
                request.petContext = PetContextPayload(**request.petContext)
            except Exception:
                pass

        pet_id = getattr(request.petContext, "id", None) if request.petContext else None
        nome_pet = getattr(request.petContext, "nome", None) or "seu pet"
        pergunta_norm = normalizar_texto(request.pergunta)

        # 1. Guardrail de Segurança Farmacológica Crítica e Ética Médica (Paracetamol em Gatos e Opioides/Prescrições)
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
                        title="Veto a Medicamentos Humanos, Opioides e Prescrição sem Exame Presencial (Morfina, Tramadol, Paracetamol)",
                        similarity_score=1.0
                    )
                ],
                rag_grounded=True
            )
            return cls._finalizar_e_persistir(resp, request, session_id, pet_id, nome_pet)

        # Bloqueio determinístico de solicitação de dosagem/receita caseira de morfina, opioides e medicamentos controlados (Cenário 4)
        is_opioide_receita = (
            any(k in pergunta_norm for k in ["morfina", "tramadol", "opioide"]) or
            (("receita" in pergunta_norm or "prescreva" in pergunta_norm or "dosagem" in pergunta_norm) and
             any(k in pergunta_norm for k in ["injetavel", "controlado", "antibiotico", "corticoide"]))
        )
        if is_opioide_receita:
            texto_bloqueio = limpar_texto_mobile(
                "⛔ VETO CLÍNICO E ÉTICO: PRESCRIÇÃO E DOSAGEM DE SUBSTÂNCIAS CONTROLADAS VEDADAS!\n\n"
                "Segundo o Protocolo de Toxicologia e Farmacovigilância Pet Guardian (Protocolo tox_12), "
                "é estritamente vedado calcular dosagens domiciliares ou prescrever receitas de analgésicos opioides (como morfina e tramadol), "
                "fármacos injetáveis ou medicamentos controlados sem consulta presencial e exame físico individualizado.\n\n"
                "🚨 Riscos Iminentes de Óbito:\n"
                "• A administração inadequada de morfina em domicílio acarreta depressão respiratória fulminante, hipotensão severa, coma e parada cardiorrespiratória.\n"
                "• Prescrição de opioides e controle álgico pós-operatório exigem termo de responsabilidade e retenção de receita especial veterinária.\n\n"
                "Encaminhe o animal IMEDIATAMENTE a um hospital veterinário presencial da Pet Guardian para manejo adequado e seguro da dor."
            )
            resp = ChatResponse(
                resposta=texto_bloqueio,
                categoria="EMERGENCIA",
                urgencia="EMERGENCIA",
                acoes_recomendadas=["Não medicar em casa", "Procurar hospital veterinário presencial urgente"],
                origem_resposta="Guardrail Ético-Farmacológico PetGuardian",
                sources_used=[
                    RetrievedSource(
                        id="tox_12",
                        source="Protocolo de Toxicologia Pet Guardian",
                        category="toxicology",
                        title="Veto a Medicamentos Humanos, Opioides e Prescrição sem Exame Presencial (Morfina, Tramadol, Paracetamol)",
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
        p = request.petContext
        if p:
            p_nome = getattr(p, "nome", None) if not isinstance(p, dict) else p.get("nome")
            p_raca = getattr(p, "raca", None) if not isinstance(p, dict) else p.get("raca")
            p_porte = getattr(p, "porte", None) if not isinstance(p, dict) else p.get("porte")
            p_idade = getattr(p, "idade", None) if not isinstance(p, dict) else p.get("idade")
            p_peso = getattr(p, "peso", None) if not isinstance(p, dict) else p.get("peso")
            p_alergias = getattr(p, "alergias", None) if not isinstance(p, dict) else p.get("alergias")
            p_meds = getattr(p, "medicamentos", None) if not isinstance(p, dict) else p.get("medicamentos")
            p_vacina = getattr(p, "ultimaVacina", None) if not isinstance(p, dict) else p.get("ultimaVacina")

            if p_nome:
                partes_contexto = [
                    f"Nome: {p_nome}",
                    f"Raça: {p_raca or 'SRD'}",
                    f"Porte: {p_porte or 'médio'}",
                    f"Idade: {p_idade if p_idade is not None else 'não informada'} anos",
                    f"Peso: {p_peso or 'não informado'} kg"
                ]
                if p_alergias:
                    partes_contexto.append(f"Alergias Conhecidas: {p_alergias}")
                if p_meds:
                    partes_contexto.append(f"Medicamentos Contínuos: {p_meds}")
                if p_vacina:
                    partes_contexto.append(f"Última Vacina: {p_vacina}")
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
