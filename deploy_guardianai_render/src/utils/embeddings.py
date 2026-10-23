"""
Módulo de Embeddings Vetoriais Locais e Similaridade de Cosseno — Pet Guardian

Arquitetura Vetorial:
1. Modelo Principal: all-MiniLM-L6-v2 (ONNX / ChromaDB) — Vetores densos de 384 dimensões em ./data/chroma.
2. Motor Resiliente Integrado: LocalSemanticEmbedder — Vetores densos de 128 dimensões com L2-norm e produto escalar.
3. Compatibilidade com Modelos Google / Hugging Face: Suporte transparente via ChromaDB Embedding Functions.
"""
import math
import hashlib
from typing import List, Dict, Set, Optional
from src.utils.text import normalizar_texto, tokenizar_com_ngrams, expansao_semantica_veterinaria

class LocalSemanticEmbedder:
    """
    Motor local de Embeddings Semânticos Densos.
    Gera vetores densos normalizados em R^D (L2-norm = 1.0) para qualquer texto ou query.
    Permite busca vetorial contínua com Similaridade de Cosseno exata sem requerer
    frameworks pesados (PyTorch/TensorFlow) que estourariam o limite de 512 MB de RAM do Render.
    """

    DIMENSAO: int = 128

    @classmethod
    def _hash_termo_para_dimensao(cls, termo: str) -> tuple[int, float]:
        """
        Projeta deterministicamente um termo tokenizado em uma das D dimensões com sinal (+1 ou -1).
        Utiliza Murmur/MD5 hashing para garantir distribuição uniforme e dispersão estocástica.
        """
        h = int(hashlib.md5(termo.encode("utf-8")).hexdigest(), 16)
        indice = h % cls.DIMENSAO
        sinal = 1.0 if ((h >> 8) & 1) == 1 else -1.0
        return indice, sinal

    @classmethod
    def gerar_embedding(cls, texto: str, idf_weights: Dict[str, float] = None) -> List[float]:
        """
        Gera o vetor denso L2-normalizado de 128 dimensões para o texto fornecido.
        Aplica tokenização, n-grams, expansão semântica e ponderação de frequência.
        """
        if not texto or not texto.strip():
            return [0.0] * cls.DIMENSAO

        tokens = tokenizar_com_ngrams(texto, n_max=2)
        tokens_expandidos = expansao_semantica_veterinaria(tokens)
        
        vetor_denso = [0.0] * cls.DIMENSAO

        if not tokens_expandidos:
            return vetor_denso

        # Frequência de termos e acumulação na projeção densa
        contagem: Dict[str, int] = {}
        for t in tokens_expandidos:
            contagem[t] = contagem.get(t, 0) + 1

        for termo, freq in contagem.items():
            peso_tf = 1.0 + math.log(freq)
            peso_idf = idf_weights.get(termo, 1.5) if idf_weights else 1.0
            peso_final = peso_tf * peso_idf

            idx, sinal = cls._hash_termo_para_dimensao(termo)
            vetor_denso[idx] += sinal * peso_final

        # Normalização L2 (norma euclidiana unitária)
        norma = math.sqrt(sum(x * x for x in vetor_denso))
        if norma > 0.0:
            vetor_denso = [round(x / norma, 6) for x in vetor_denso]

        return vetor_denso

def calcular_similaridade_cosseno(vetor_a: List[float], vetor_b: List[float]) -> float:
    """
    Calcula a Similaridade de Cosseno entre dois vetores densos normalizados:
    cos(u, v) = u . v / (||u|| * ||v||)
    
    Como ambos os vetores gerados pelo LocalSemanticEmbedder são L2-normalizados (||v|| = 1.0),
    a similaridade de cosseno equivale diretamente ao produto escalar: sum(u_i * v_i).
    Retorna valor no intervalo [0.0, 1.0] arredondado em 4 casas decimais.
    """
    if not vetor_a or not vetor_b or len(vetor_a) != len(vetor_b):
        return 0.0

    produto_escalar = sum(a * b for a, b in zip(vetor_a, vetor_b))
    
    # Restrição aos limites de similaridade positiva para relevância semântica
    similaridade = max(0.0, min(1.0, produto_escalar))
    return round(similaridade, 4)
