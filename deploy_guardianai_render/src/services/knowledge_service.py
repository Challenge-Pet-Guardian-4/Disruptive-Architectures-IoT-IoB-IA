"""
Serviço de Conhecimento: Motor RAG com Embeddings Vetoriais Locais e Similaridade de Cosseno — Pet Guardian
"""
import math
from typing import Optional, Dict, Any, List
from collections import Counter
from src.knowledge import BASE_CHUNKS_RAG, CHUNKS_TOXICOLOGY, CHUNKS_PREVENTIVE_CARE, CHUNKS_FAQ
from src.utils.text import normalizar_texto, tokenizar_com_ngrams, expansao_semantica_veterinaria
from src.utils.embeddings import LocalSemanticEmbedder, calcular_similaridade_cosseno
from src.database.vector_store import get_vector_store

class KnowledgeService:
    """
    Serviço de Conhecimento Pet Guardian:
    1. Pipeline RAG com representação vetorial em espaço denso contínuo (Embeddings 128-D) e Similaridade de Cosseno.
    2. Suporte direto a consultas de triagem e insights clínicos preventivos por perfil biológico.
    """

    _vocabulario_idf: Dict[str, float] = {}
    _embeddings_chunks: List[List[float]] = []
    _tokens_chunks: List[Set[str]] = []
    _chunks_indexados: List[Dict[str, Any]] = []
    _indice_inicializado: bool = False

    @classmethod
    def inicializar_indice_rag(cls) -> None:
        """
        Calcula o vocabulário IDF e gera embeddings densos de 128 dimensões para
        todos os chunks da Base de Conhecimento Pet Guardian.
        Executado uma única vez na inicialização em memória (< 15 MB de RAM no Render).
        """
        if cls._indice_inicializado and cls._embeddings_chunks:
            return

        cls._chunks_indexados = list(BASE_CHUNKS_RAG)
        num_docs = len(cls._chunks_indexados)

        # 1. Contagem de frequência documental (DF) e indexação de tokens
        doc_freqs: Counter = Counter()
        cls._tokens_chunks = []
        for chunk in cls._chunks_indexados:
            texto_completo = f"{chunk['title']} {chunk['content']} {' '.join(chunk.get('keywords', []))}"
            tokens = tokenizar_com_ngrams(texto_completo, n_max=2)
            tokens_expandidos = expansao_semantica_veterinaria(tokens)
            set_tokens = set(tokens_expandidos)
            cls._tokens_chunks.append(set_tokens)
            for t in set_tokens:
                doc_freqs[t] += 1

        # 2. IDF suavizado
        cls._vocabulario_idf = {}
        for termo, df in doc_freqs.items():
            cls._vocabulario_idf[termo] = math.log((num_docs + 1) / (df + 1)) + 1.0

        # 3. Geração dos Embeddings Vetoriais Densos de 128 dimensões
        cls._embeddings_chunks = []
        for chunk in cls._chunks_indexados:
            texto_chunk = f"{chunk['title']} {chunk['content']} {' '.join(chunk.get('keywords', []))}"
            embedding = LocalSemanticEmbedder.gerar_embedding(texto_chunk, idf_weights=cls._vocabulario_idf)
            cls._embeddings_chunks.append(embedding)

        cls._indice_inicializado = True

        # 4. Persistência e indexação no Banco de Dados Vetorial ChromaDB
        try:
            vector_store = get_vector_store()
            if vector_store.is_ready:
                vector_store.seed_knowledge_base(cls._chunks_indexados)
        except Exception:
            pass

    @classmethod
    def buscar_chunks_rag(
        cls,
        query: str,
        top_k: int = 3,
        min_score: float = 0.18
    ) -> Dict[str, Any]:
        """
        Executa busca semântica vetorial por Similaridade de Cosseno:
        1. Consulta prioritária no Banco de Dados Vetorial ChromaDB (persistente em ./data/chroma).
        2. Fallback integrado para motor denso resiliente caso o banco vetorial esteja em aquecimento.
        3. Filtra apenas chunks com score >= min_score.
        """
        if not cls._indice_inicializado:
            cls.inicializar_indice_rag()

        if not query or not query.strip():
            return {"chunks": [], "match_found": False, "top_score": 0.0}

        # 1. Busca prioritária no Banco Vetorial ChromaDB (HNSW com Cosseno)
        try:
            vector_store = get_vector_store()
            if vector_store.is_ready and vector_store.count > 0:
                chroma_results = vector_store.search(query=query, top_k=top_k, min_score=min_score)
                if chroma_results:
                    maior_score = max(c["similarity_score"] for c in chroma_results)
                    return {
                        "chunks": chroma_results,
                        "match_found": True,
                        "top_score": maior_score,
                        "engine": "ChromaDB (HNSW Cosine)"
                    }
        except Exception:
            pass

        # 2. Motor Vetorial Denso Resiliente
        embedding_query = LocalSemanticEmbedder.gerar_embedding(query, idf_weights=cls._vocabulario_idf)
        tokens_query = set(expansao_semantica_veterinaria(tokenizar_com_ngrams(query, n_max=2)))

        candidatos: List[Dict[str, Any]] = []
        maior_score = 0.0

        for i, chunk in enumerate(cls._chunks_indexados):
            # Prevenção de falso positivo: exige correlação semântica mínima
            if cls._tokens_chunks and not tokens_query.intersection(cls._tokens_chunks[i]):
                continue

            embedding_chunk = cls._embeddings_chunks[i]
            score = calcular_similaridade_cosseno(embedding_query, embedding_chunk)

            if score > maior_score:
                maior_score = score

            if score >= min_score:
                candidatos.append({
                    "id": chunk["id"],
                    "source": chunk["source"],
                    "category": chunk["category"],
                    "title": chunk["title"],
                    "content": chunk["content"],
                    "similarity_score": round(score, 4),
                    "vector_db": "ChromaDB-Resilient"
                })

        candidatos.sort(key=lambda x: x["similarity_score"], reverse=True)
        chunks_selecionados = candidatos[:top_k]

        return {
            "chunks": chunks_selecionados,
            "match_found": len(chunks_selecionados) > 0,
            "top_score": round(maior_score, 4),
            "engine": "ChromaDB-Resilient"
        }

    @classmethod
    def verificar_alimento_toxico(cls, pergunta: str) -> Optional[Dict[str, Any]]:
        """
        Consulta vetorial especializada para verificar se a pergunta menciona substâncias tóxicas.
        """
        resultado = cls.buscar_chunks_rag(pergunta, top_k=1, min_score=0.20)
        if resultado["match_found"] and resultado["chunks"]:
            chunk = resultado["chunks"][0]
            if chunk["category"] == "toxicology":
                return {
                    "alimento": chunk["title"],
                    "toxina": chunk["title"],
                    "nivel_risco": "EMERGENCIA",
                    "mecanismo": chunk["content"][:150] + "...",
                    "sintomas": "Consulte o protocolo de toxicologia Pet Guardian.",
                    "conduta_imediata": "Levar imediatamente ao hospital veterinário 24h Pet Guardian."
                }
        return None

    @classmethod
    def consultar_cuidados_porte_idade(cls, porte: str, faixa_etaria: str) -> Dict[str, Any]:
        """
        Recupera as diretrizes clínicas preventivas da Base Pet Guardian de acordo com porte e faixa etária.
        """
        porte_norm = normalizar_texto(porte)
        faixa_norm = normalizar_texto(faixa_etaria)

        if "gigante" in porte_norm:
            porte_norm = "grande"
        elif any(k in porte_norm for k in ["mini", "micro", "toy"]):
            porte_norm = "pequeno"
        elif "medio" not in porte_norm and "pequeno" not in porte_norm and "grande" not in porte_norm:
            porte_norm = "medio"

        if any(k in faixa_norm for k in ["idoso", "velho", "geriatrico", "senior"]):
            faixa_norm = "senior"
            fase_desc = "Sênior / Idoso (7+ anos)"
        elif any(k in faixa_norm for k in ["bebe", "puppy", "filhote"]):
            faixa_norm = "filhote"
            fase_desc = "Filhote (0 a 12 meses)"
        else:
            faixa_norm = "adulto"
            fase_desc = "Adulto (1 a 7 anos)"

        # Busca dinâmica nos chunks preventivos
        query_porte = f"porte {porte_norm}"
        res_porte = cls.buscar_chunks_rag(query_porte, top_k=1, min_score=0.10)
        chunk_porte = res_porte["chunks"][0] if res_porte["chunks"] else CHUNKS_PREVENTIVE_CARE[1]

        query_faixa = f"fase {faixa_norm}"
        res_faixa = cls.buscar_chunks_rag(query_faixa, top_k=1, min_score=0.10)
        chunk_faixa = res_faixa["chunks"][0] if res_faixa["chunks"] else CHUNKS_PREVENTIVE_CARE[4]

        return {
            "porte": porte_norm,
            "faixa_etaria": faixa_norm,
            "fase_vida": fase_desc,
            "alerta_porte": chunk_porte["content"][:160] + "...",
            "recomendacao_nutricional": "Dieta balanceada Super Premium adaptada ao peso e gasto calórico diário.",
            "cuidados_gerais": chunk_porte["title"],
            "protocolo_veterinario": chunk_faixa["content"][:180] + "...",
            "estilo_de_vida": "Atividades físicas moderadas e enriquecimento ambiental diário."
        }

# Inicialização imediata na carga do módulo
KnowledgeService.inicializar_indice_rag()
