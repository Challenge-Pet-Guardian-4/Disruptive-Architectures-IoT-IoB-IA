"""
Utilitários: Guardrails Anti-Pretexto e Sanitização de Código
"""
import re
from src.utils.text import normalizar_texto

TERMOS_PROGRAMACAO_OFFTOPIC = [
    "inverter uma lista", "inverter lista", "em python", "codigo em python", "código em python",
    "funcao em python", "função em python", "script em python", "programacao", "programação",
    "algoritmo", "javascript", "linguagem python", "def ", "print(", "reverse()", "vetor",
    "matriz", "codigo java", "código java", "script", "desenvolva um codigo", "crie um codigo"
]

def detectar_pedido_programacao(texto: str) -> bool:
    """
    Verifica se a pergunta do usuário contém tentativas de obter código ou scripts de programação.
    """
    texto_norm = normalizar_texto(texto)
    return any(termo in texto_norm for termo in TERMOS_PROGRAMACAO_OFFTOPIC)

def sanitizar_resposta_anti_codigo(texto: str, pedido_tinha_programacao: bool) -> str:
    """
    Remove blocos de código ou trechos de sintaxe Python que a LLM possa ter gerado
    indevidamente e adiciona a nota de recusa de escopo.
    """
    if not texto:
        return ""
    
    # Remove blocos de código ```...```
    texto_limpo = re.sub(r'```[\s\S]*?```', '', texto)
    
    # Remove linhas que contenham declarações de código típicas
    linhas_filtradas = []
    for linha in texto_limpo.split('\n'):
        l_strip = linha.strip()
        if (l_strip.startswith('def ') or l_strip.startswith('print(') or 
            '[::-1]' in l_strip or '.reverse()' in l_strip or l_strip.startswith('import ')):
            continue
        linhas_filtradas.append(linha)
    
    texto_final = '\n'.join(linhas_filtradas).strip()
    
    if pedido_tinha_programacao:
        aviso_escopo = (
            "\n\n💡 Nota de Escopo: Como Guardian AI, sou dedicada exclusivamente à saúde e bem-estar animal, "
            "portanto não forneço códigos ou instruções de programação (como em Python), mesmo para o seu pet!"
        )
        if "não forneço códigos" not in texto_final and "dedicada exclusivamente" not in texto_final:
            texto_final += aviso_escopo
            
    return texto_final.strip()
