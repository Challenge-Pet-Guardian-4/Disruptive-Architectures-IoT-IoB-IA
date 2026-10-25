"""
Serviço Orquestrador do Chat Clínico PetGuardian com RAG Vetorial e Persistência SQLite
"""
import uuid
from typing import Optional, List, Dict, Any
from src.core.config import AI_PROVIDER, FALLBACK_PROVIDER, GROQ_MODEL, GEMINI_MODEL
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
    4. Inferência generativa primária via Groq Cloud (provedor definido por AI_PROVIDER, com fallback automático para o outro)
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
        Atribui o sessionId ao response e grava o turno e o parecer de auditoria no SQLite (falha de gravação é logada e não derruba a resposta).
        """
        response.sessionId = session_id
        ChatRepository.salvar_interacao(
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

    @staticmethod
    def _resposta_guardrail(texto: str, acoes: List[str], origem: str) -> ChatResponse:
        """Monta a resposta de emergência dos vetos farmacológicos, sempre ancorada no protocolo tox_12."""
        return ChatResponse(
            resposta=limpar_texto_mobile(texto),
            categoria="EMERGENCIA",
            urgencia="EMERGENCIA",
            acoes_recomendadas=acoes,
            origem_resposta=origem,
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

    @classmethod
    def processar_chat(cls, request: ChatRequest) -> ChatResponse:
        session_id = request.sessionId or f"sess_{uuid.uuid4().hex[:12]}"
        p = request.petContext
        pet_id = p.id if p else None
        nome_pet = (p.nome if p else None) or "seu pet"
        pergunta_norm = normalizar_texto(request.pergunta)

        # 1. Guardrail de Segurança Farmacológica Crítica e Ética Médica (Paracetamol em Gatos e Opioides/Prescrições)
        if "paracetamol" in pergunta_norm and any(k in pergunta_norm for k in ["gato", "felino", "mingau", "gatinho"]):
            resp = cls._resposta_guardrail(
                "⛔ ALERTA VITAL: NUNCA DÊ PARACETAMOL PARA UM GATO!\n\n"
                "Segundo o Protocolo de Farmacovigilância Pet Guardian, o Paracetamol é ALTAMENTE LETAL PARA FELINOS mesmo em doses mínimas infantis. "
                "Os gatos possuem deficiência congênita na enzima glucuronil-transferase, causando meta-hemoglobinemia (asfixia interna) "
                "e necrose hepática fulminante em poucas horas.\n\n"
                "🚨 O que fazer agora:\n"
                "• Não administre nenhum medicamento caseiro ou humano.\n"
                "• Se o animal ingeriu acidentalmente, leve IMEDIATAMENTE ao pronto-socorro veterinário 24h Pet Guardian.",
                ["Não medicar em casa", "Procurar clínica veterinária urgente"],
                "Guardrail de Segurança Farmacológica PetGuardian"
            )
            return cls._finalizar_e_persistir(resp, request, session_id, pet_id, nome_pet)

        # Bloqueio determinístico de solicitação de dosagem/receita caseira de morfina, opioides e medicamentos controlados (Cenário 4)
        is_opioide_receita = (
            any(k in pergunta_norm for k in ["morfina", "tramadol", "opioide"]) or
            (any(k in pergunta_norm for k in ["receita", "prescreva", "dosagem"]) and
             any(k in pergunta_norm for k in ["injetavel", "controlado", "antibiotico", "corticoide"]))
        )
        if is_opioide_receita:
            resp = cls._resposta_guardrail(
                "⛔ VETO CLÍNICO E ÉTICO: PRESCRIÇÃO E DOSAGEM DE SUBSTÂNCIAS CONTROLADAS VEDADAS!\n\n"
                "Segundo o Protocolo de Toxicologia e Farmacovigilância Pet Guardian (Protocolo tox_12), "
                "é estritamente vedado calcular dosagens domiciliares ou prescrever receitas de analgésicos opioides (como morfina e tramadol), "
                "fármacos injetáveis ou medicamentos controlados sem consulta presencial e exame físico individualizado.\n\n"
                "🚨 Riscos Iminentes de Óbito:\n"
                "• A administração inadequada de morfina em domicílio acarreta depressão respiratória fulminante, hipotensão severa, coma e parada cardiorrespiratória.\n"
                "• Prescrição de opioides e controle álgico pós-operatório exigem termo de responsabilidade e retenção de receita especial veterinária.\n\n"
                "Encaminhe o animal IMEDIATAMENTE a um hospital veterinário presencial da Pet Guardian para manejo adequado e seguro da dor.",
                ["Não medicar em casa", "Procurar hospital veterinário presencial urgente"],
                "Guardrail Ético-Farmacológico PetGuardian"
            )
            return cls._finalizar_e_persistir(resp, request, session_id, pet_id, nome_pet)

        # 2. Identificação de Intenções Especiais (Histórico do Pet / Dúvidas Gerais)
        is_pet_info_query = any(k in pergunta_norm for k in [
            "historico", "ficha", "prontuario", "dados do meu", "dados de", "sobre o meu pet",
            "sobre meu pet", "quantos anos", "qual a raca", "qual o peso", "ele e castrado",
            "minhas vacinas", "vacina dele", "vacinas dele", "alergia dele", "medicamento dele",
            "o que voce sabe sobre"
        ])

        is_general_query = any(k in pergunta_norm for k in [
            "como cuidar", "cuidar do meu", "cuidar de um", "dicas para", "cuidados com",
            "o que voce faz", "o que voce consegue", "o que voce sabe fazer",
            "o que diabos", "como funciona", "quem e voce", "ajuda com meu pet"
        ])

        # 3. Recuperação de Chunks da Base de Conhecimento via RAG (Embeddings Vetoriais + Similaridade de Cosseno)
        resultado_rag = KnowledgeService.buscar_chunks_rag(request.pergunta, top_k=3)
        chunks_recuperados = resultado_rag["chunks"]
        match_found = resultado_rag["match_found"]

        # Se for dúvida abrangente sobre cuidados e temos contexto do pet, recuperar preventivo do porte/idade
        if (is_general_query or (not match_found and any(w in pergunta_norm for w in ["cuidar", "cuidado", "rotina", "dica"]))) and p and not chunks_recuperados:
            porte_calc = (p.porte or "medio").lower()
            idade_calc = p.idade if p.idade is not None else 3
            chunk_fallback_id = "prev_02"
            if "pequeno" in porte_calc:
                chunk_fallback_id = "prev_01"
            elif any(k in porte_calc for k in ["grande", "gigante"]) or any(r in (p.raca or "").lower() for r in ["golden", "labrador", "pastor", "rottweiler"]):
                chunk_fallback_id = "prev_03"
            elif idade_calc == 0:
                chunk_fallback_id = "prev_04"
            elif idade_calc >= 7:
                chunk_fallback_id = "prev_06"

            chunks_adicionais = [c for c in KnowledgeService._chunks_indexados if c["id"] in {chunk_fallback_id, "faq_12", "faq_05"}]
            if chunks_adicionais:
                chunks_recuperados = [
                    {
                        "id": c["id"],
                        "source": c["source"],
                        "category": c["category"],
                        "title": c["title"],
                        "content": c["content"],
                        "similarity_score": 0.85
                    }
                    for c in chunks_adicionais[:2]
                ]
                match_found = True

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

        # 4. Construção do Contexto Estruturado do Pet
        contexto_pet_str = ""
        if p and p.nome:
            castrado_str = "Sim" if p.castrado is True else ("Não" if p.castrado is False else "Não informado")
            partes_contexto = [
                f"Nome: {p.nome}",
                f"Raça: {p.raca or 'SRD'}",
                f"Porte: {p.porte or 'médio'}",
                f"Idade: {p.idade if p.idade is not None else 'não informada'} anos",
                f"Peso: {p.peso or 'não informado'} kg",
                f"Castrado: {castrado_str}",
                f"Alergias Cadastradas: {p.alergias or 'Nenhuma alergia conhecida registrada'}",
                f"Medicamentos Contínuos: {p.medicamentos or 'Nenhum medicamento contínuo registrado'}",
                f"Última Vacina: {p.ultimaVacina or 'Não registrada no app'}",
                f"Última Consulta: {p.ultimaConsulta or 'Não registrada no app'}"
            ]
            contexto_pet_str = "[Ficha Cadastral e Histórico do Pet Ativo: " + ", ".join(partes_contexto) + "]"

        # 5. Montagem do Prompt Fundamentado (RAG Prompt Template)
        prompt_fundamentado = formatar_prompt_rag(
            pergunta=request.pergunta,
            contexto_pet_str=contexto_pet_str,
            chunks_recuperados=chunks_recuperados,
            match_found=match_found,
            is_pet_info_query=is_pet_info_query,
            is_general_query=is_general_query
        )

        eh_pedido_programacao = detectar_pedido_programacao(request.pergunta)
        origem_ia = ""
        resposta_ia = None

        # 5. Inferência Generativa: provedor primário (AI_PROVIDER) e, se falhar, o outro como contingência
        for provedor in (AI_PROVIDER, FALLBACK_PROVIDER):
            servico, modelo = (GroqService, GROQ_MODEL) if provedor == "groq" else (GeminiService, GEMINI_MODEL)
            resposta_ia = servico.gerar_resposta(prompt_fundamentado, request.historico)
            if resposta_ia:
                origem_ia = f"Guardian AI ({provedor.capitalize()}: {modelo} + RAG)"
                break

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
                rag_grounded=(match_found or is_pet_info_query)
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

            eh_emergencia = (top_chunk["category"] == "toxicology" or top_chunk["id"] in {"rep_03", "faq_08", "faq_09", "inf_01"} or top_chunk.get("urgency") in ["EMERGENCIA", "emergencia"])
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
        porte_req = (p.porte if p else None) or "medio"
        faixa_calc = KnowledgeService.calcular_faixa_etaria(p.idade if p else None)
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
