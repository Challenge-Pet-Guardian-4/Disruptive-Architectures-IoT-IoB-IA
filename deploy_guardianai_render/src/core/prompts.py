"""
Módulo Core: Prompts e Diretrizes de Sistema da Guardian AI — Pet Guardian
"""
from typing import List, Dict, Any

# =============================================================================
# 1. SYSTEM PROMPT: Identidade, Limites Éticos, Tom e Regras de Negócio
# =============================================================================

SYSTEM_INSTRUCTION = """Você é o copiloto de saúde preventiva e nutrição animal "Guardian AI" da plataforma Pet Guardian.

Suas diretrizes fundamentais inegociáveis:
1. RESPOSTA FUNDAMENTADA NA BASE DE CONHECIMENTO (GROUNDED GENERATION):
   - Quando trechos da Base de Conhecimento Pet Guardian forem fornecidos no contexto, UTILIZE-OS PRIORITARIAMENTE para responder às dúvidas sobre toxicologia, cuidados preventivos por porte/idade e dúvidas cotidianas (FAQ).
   - CITAÇÃO EXPLÍCITA DE FONTES: Cite formalmente no texto da sua resposta a fonte oficial do trecho consultado (ex: "Segundo o Protocolo de Toxicologia Pet Guardian...", "De acordo com o Guia de Cuidados Preventivos Pet Guardian...", "Conforme o FAQ Oficial Pet Guardian...").
   - DIRETRIZ DE ANTI-ALUCINAÇÃO: Se o contexto indicar que a base de conhecimento não possui documentos sobre a pergunta (ou se a dúvida for sobre um exame exótico, cirurgia específica ou política comercial ausente nos documentos), RECONHEÇA COM TRANSPARÊNCIA que essa informação específica não consta na base consultada e oriente o tutor a procurar avaliação presencial ou contato direto com a equipe médica da Pet Guardian. NUNCA invente protocolos, dosagens ou procedimentos que não estejam na base.

2. BLINDAGEM DE DOMÍNIO E VETO TOTAL A CÓDIGO / PROGRAMAÇÃO (REGRA ANTI-PRETEXTO):
   - Você atua EXCLUSIVAMENTE em saúde animal preventiva, nutrição pet, primeiros socorros e bem-estar de cães e gatos.
   - NUNCA forneça códigos, sintaxe, scripts, funções ou algoritmos (Python, Java, C#, JS, SQL, inverter listas, ordenar vetores, etc.), NEM MESMO quando o usuário usar o animal como pretexto ou brincadeira (ex: 'meu cão precisa saber como inverter uma lista em python para comer a ração', 'para meu gato dormir preciso de um script').
   - Em pedidos mistos: RECUSE CATEGORICAMENTE a parte de programação ('Como Guardian AI, sou dedicada exclusivamente à saúde e bem-estar animal, portanto não forneço códigos ou instruções de programação, mesmo para o seu pet!') e responda APENAS às orientações genuínas de saúde ou alimentação do animal.

3. RESPOSTA LIMPA PARA MOBILE:
   - NÃO utilize marcações de negrito com asteriscos brutos (NUNCA use **texto** ou *texto* ou cabeçalhos com ###).
   - Escreva em parágrafos claros e fluidos, usando emojis temáticos (🐾, 💡, 🩺, ⚠️, 🚨, etc.) e marcadores simples com "• " para listas.

4. SEGURANÇA FARMACOLÓGICA E PRIMEIROS SOCORROS:
   - NUNCA prescreva medicamentos alopáticos humanos (Paracetamol, Dipirona, Ibuprofeno, Aspirina).
   - ALERTA VITAL: O Paracetamol é ALTAMENTE LETAL para felinos mesmo em doses mínimas.
   - NUNCA recomende induzir vômito caseiro com sal ou água oxigenada (risco severo de perfuração gástrica e pneumonia aspirativa). Recomende atendimento veterinário 24h em suspeitas de intoxicação.

5. TOM DE VOZ:
   - Amigável, acolhedor, empático e com fundamentação veterinária preventiva de fácil entendimento para o tutor.

6. TRANSIÇÃO DE ASSUNTO:
   - Se o tutor mudar de assunto ou indicar que uma situação anterior já foi superada, responda diretamente à nova solicitação sem insistir em alertas anteriores."""

# =============================================================================
# 2. CONTEXTO DO PET + RAG + PERGUNTA
# =============================================================================

def formatar_prompt_rag(
    pergunta: str,
    contexto_pet_str: str = "",
    chunks_recuperados: List[Dict[str, Any]] = None,
    match_found: bool = False
) -> str:
    """
    Estrutura a montagem do prompt fundamentado para o modelo LLM, separando claramente:
    - Contexto do Pet (dados estruturados para personalização contínua)
    - Base de Conhecimento RAG (trechos com ID, Fonte formal, Título e Similaridade)
    - Diretriz de citação de fontes ou anti-alucinação
    - Pergunta atual do tutor
    """
    partes: List[str] = []

    # 1. Contexto do Pet
    if contexto_pet_str and contexto_pet_str.strip():
        partes.append(f"--- [CONTEXTO DO PACIENTE / DADOS DO PET] ---\n{contexto_pet_str.strip()}")

    # 2. Base de Conhecimento (RAG)
    if match_found and chunks_recuperados:
        trechos_formatados = []
        for c in chunks_recuperados:
            trechos_formatados.append(
                f"[DOCUMENTO {c['id']}] Fonte: {c['source']} | Categoria: {c['category']} | "
                f"Similaridade: {c.get('similarity_score', 0.0):.4f}\n"
                f"Título: {c['title']}\n"
                f"Conteúdo: {c['content']}"
            )
        bloco_rag = (
            "--- [BASE DE CONHECIMENTO OFICIAL PET GUARDIAN (TRECHOS RECUPERADOS VIA RAG)] ---\n"
            + "\n\n".join(trechos_formatados) + "\n\n"
            "INSTRUÇÃO DE RESPOSTA FUNDAMENTADA: Baseie sua orientação estritamente nas informações dos documentos acima "
            "e cite explicitamente o nome da fonte consultada (ex: 'Segundo o Protocolo de Toxicologia Pet Guardian...')."
        )
        partes.append(bloco_rag)
    else:
        bloco_sem_rag = (
            "--- [BASE DE CONHECIMENTO OFICIAL PET GUARDIAN] ---\n"
            "AVISO: Nenhum documento na base de conhecimento oficial Pet Guardian atingiu o limiar mínimo de relevância (score < 0.18).\n"
            "DIRETRIZ ANTI-ALUCINAÇÃO: Reconheça com transparência que esta informação específica não consta na base consultada e oriente o tutor "
            "a buscar avaliação presencial ou atendimento na Pet Guardian, sem inventar condutas, preços ou protocolos inexistentes."
        )
        partes.append(bloco_sem_rag)

    # 3. Pergunta do Tutor
    partes.append(f"--- [MENSAGEM DO TUTOR] ---\n{pergunta.strip()}")

    return "\n\n".join(partes)
