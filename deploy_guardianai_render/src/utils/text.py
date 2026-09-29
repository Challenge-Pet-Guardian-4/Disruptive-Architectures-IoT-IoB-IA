"""
Utilitários: Sanitização e Normalização Textual para Mobile
"""
import re
import unicodedata

def normalizar_texto(texto: str) -> str:
    """
    Remove acentuações e caracteres diacríticos, convertendo para minúsculas.
    Útil para comparações insensíveis a acentos.
    """
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", str(texto))
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).strip().lower()

def limpar_texto_mobile(texto: str) -> str:
    """
    Remove marcadores brutos de Markdown (como **negrito**, # títulos, etc.)
    garantindo que o componente <Text> do React Native exiba um texto limpo,
    elegante e sem asteriscos.
    """
    if not texto:
        return ""
    
    # Remove marcações de negrito e itálico markdown (**texto** ou *texto* ou __texto__)
    t = re.sub(r'\*\*(.*?)\*\*', r'\1', texto)
    t = re.sub(r'__(.*?)__', r'\1', t)
    t = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'\1', t)
    
    # Remove marcadores de cabeçalho Markdown (###, ##, #)
    t = re.sub(r'^#{1,6}\s*', '', t, flags=re.MULTILINE)
    
    # Normaliza marcadores de lista
    t = re.sub(r'^\s*[\*\-]\s+', '• ', t, flags=re.MULTILINE)
    
    # Remove múltiplos espaços e quebras de linha excessivas (mais de 2 consecutivas)
    t = re.sub(r'\n{3,}', '\n\n', t)
    
    return t.strip()
