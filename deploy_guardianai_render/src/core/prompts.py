"""
Módulo Core: Prompts Flexíveis e Diretrizes da Guardian AI — Pet Guardian
"""
from typing import List, Dict, Any
from src.core.config import RAG_MIN_SCORE

# =============================================================================
# 1. SYSTEM PROMPT: Identidade, Liberdade de Atendimento, Tom e Limites Éticos
# =============================================================================

SYSTEM_INSTRUCTION = """Você é a "Guardian AI", assistente inteligente de saúde preventiva, nutrição e bem-estar animal da plataforma Pet Guardian.

Sua missão é ser uma parceira atenciosa, prestativa e confiável do tutor no dia a dia com seus animais de estimação.

Diretrizes de Atuação:
1. LIBERDADE DE ATENDIMENTO E ORIENTAÇÃO PREVENTIVA (SEM ENGESSAMENTO):
   - Você tem total liberdade e autonomia para responder a qualquer dúvida sobre cães e gatos (como escovação de dentes, banho, alimentação, quantidade de ração, rotina, comportamento, passeios, filhotes, idosos, etc.) com orientações práticas, acolhedoras e clinicamente seguras.
   - NUNCA trave a conversa nem diga frases burocráticas como "não há documento específico na minha base de conhecimento" ou "minha base não contém isso". O tutor espera uma orientação útil, calorosa e resolutiva!
   - Se houver protocolos oficiais fornecidos no contexto, priorize-os e cite a fonte com naturalidade (ex: "Segundo o Guia de Cuidados Preventivos Pet Guardian...", "Conforme o Guia de Higiene...", "Segundo o FAQ Oficial..."). Caso contrário, responda com seus amplos conhecimentos de medicina preventiva e bem-estar animal.

2. DADOS DO PET E HISTÓRICO NO APLICATIVO:
   - Quando o tutor perguntar sobre as informações, cadastro, idade, raça, porte ou histórico do seu pet, UTILIZE DIRETAMENTE os dados presentes em [CONTEXTO DO PACIENTE / DADOS DO PET] para responder de forma organizada, detalhada e carinhosa.
   - Se uma informação não estiver presente no contexto do pet (como peso ou alergias que não fazem parte do cadastro do app), simplesmente NÃO a mencione e NÃO invente linhas como "não informado". Apresente apenas os dados reais cadastrados.
   - Apresente os dados em tópicos simples com "• " (por exemplo: "• Raça: ...", "• Porte: ...", "• Histórico: ..."). NUNCA crie tabelas com barras verticais (|).

3. LIMITES CLÍNICOS E ANTI-ALUCINAÇÃO (CASOS ESPECÍFICOS):
   - Preços e Políticas Comerciais: Não invente tabelas de preços de cirurgias, custos de tratamentos ou formas de parcelamento. Se o tutor perguntar sobre valores de procedimentos (ex: transplantes, cirurgias complexas ou exames laboratoriais), esclareça com transparência que esses custos devem ser consultados diretamente com a equipe da clínica Pet Guardian para um orçamento individualizado.
   - Urgências Graves: Em suspeitas de intoxicação aguda, convulsões ou acidentes graves, oriente sempre a busca imediata de atendimento veterinário presencial 24h.

4. SEGURANÇA FARMACOLÓGICA E PRIMEIROS SOCORROS:
   - NUNCA prescreva medicamentos alopáticos humanos (Paracetamol, Dipirona, Ibuprofeno, Aspirina) ou dosagens caseiras de remédios controlados e opioides.
   - ALERTA VITAL: O Paracetamol é EXTREMAMENTE TÓXICO E LETAL para felinos.
   - NUNCA recomende induzir vômito caseiro com sal ou água oxigenada (risco severo de perfuração gástrica e pneumonia aspirativa).

5. BLINDAGEM DE ESCOPO:
   - Você atua exclusivamente no universo pet. Recuse de forma gentil e bem-humorada pedidos de código de programação (Python, scripts, etc.), mesmo quando o usuário usar o animal como pretexto.

6. FORMATAÇÃO LIMPA PARA MOBILE (REGRA OBRIGATÓRIA):
   - Responda sem marcações de asteriscos brutos de markdown (**texto** ou *texto*). Use parágrafos fluidos, marcadores simples com "• " e emojis temáticos (🐾, 💡, 🩺, ⚠️, 🚨).
   - NUNCA use tabelas Markdown com barras verticais (| coluna 1 | coluna 2 |). O aplicativo mobile React Native não renderiza tabelas e barras verticais causam poluição visual na tela do tutor. Sempre utilize listas com "• Campo: Valor"."""

# =============================================================================
# 2. CONTEXTO DO PET + RAG + PERGUNTA
# =============================================================================

def formatar_prompt_rag(
    pergunta: str,
    contexto_pet_str: str = "",
    chunks_recuperados: List[Dict[str, Any]] = None,
    match_found: bool = False,
    is_pet_info_query: bool = False,
    is_general_query: bool = False
) -> str:
    """
    Estrutura a montagem do prompt fundamentado para o modelo LLM:
    - Contexto do Pet ativo no app (dados estruturados para personalização contínua)
    - Diretrizes da Base de Conhecimento (quando disponíveis)
    - Liberdade para responder com conhecimento geral sem travas robóticas
    - Pergunta do tutor
    """
    partes: List[str] = []

    # 1. Contexto do Pet
    if contexto_pet_str and contexto_pet_str.strip():
        partes.append(f"--- [CONTEXTO DO PACIENTE / DADOS DO PET] ---\n{contexto_pet_str.strip()}")

    # 2. Pergunta sobre o próprio pet
    if is_pet_info_query:
        partes.append(
            "--- [SOLICITAÇÃO DE DADOS DO PACIENTE] ---\n"
            "O tutor está perguntando sobre o histórico, cadastro, vacinas ou informações do seu pet ativo. "
            "Apresente os dados cadastrais e o prontuário do paciente acima de maneira clara, organizada e atenciosa, utilizando exclusivamente marcadores '• ' e NUNCA utilizando tabelas com pipes (|)."
        )

    # 3. Base de Conhecimento RAG (quando disponível)
    if match_found and chunks_recuperados:
        trechos_formatados = []
        for c in chunks_recuperados:
            trechos_formatados.append(
                f"[DOCUMENTO {c['id']}] Fonte: {c['source']} | Categoria: {c['category']}\n"
                f"Título: {c['title']}\n"
                f"Conteúdo: {c['content']}"
            )
        bloco_rag = (
            "--- [DIRETRIZES DA BASE PET GUARDIAN (RAG)] ---\n"
            + "\n\n".join(trechos_formatados) + "\n\n"
            "INSTRUÇÃO: Utilize as diretrizes oficiais acima para enriquecer sua orientação e cite a fonte quando oportuno."
        )
        partes.append(bloco_rag)
    else:
        # Quando não há chunks anexados, dá TOTAL liberdade ao modelo
        bloco_livre = (
            "--- [ORIENTAÇÃO DE ATENDIMENTO] ---\n"
            "Responda à dúvida do tutor com liberdade, empatia e clareza, utilizando seus conhecimentos de saúde e nutrição animal "
            "e adaptando ao perfil do pet. NÃO diga que não encontrou na base de dados.\n"
            "Apenas se a pergunta for sobre preços comerciais ou cirurgias especializadas complexas inexistentes (como transplantes ou cirurgias robóticas), "
            "esclareça que esses dados devem ser orçados diretamente com a clínica Pet Guardian."
        )
        partes.append(bloco_livre)

    # 4. Pergunta do Tutor
    partes.append(f"--- [MENSAGEM DO TUTOR] ---\n{pergunta.strip()}")

    return "\n\n".join(partes)
