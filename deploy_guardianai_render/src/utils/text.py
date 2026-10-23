"""
Utilitários: Sanitização Textual para Mobile, Tokenização e Expansão Semântica — Pet Guardian
"""
import re
import unicodedata
from typing import List, Dict, Set

# Conjunto de stopwords em português para filtragem de ruído
STOPWORDS_PT: Set[str] = {
    "a", "o", "as", "os", "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas",
    "por", "para", "com", "sem", "sob", "sobre", "um", "uma", "uns", "umas", "e", "ou",
    "mas", "que", "se", "como", "eu", "ele", "ela", "eles", "elas", "meu", "minha", "meus",
    "minhas", "seu", "sua", "seus", "suas", "esse", "essa", "esses", "essas", "este", "esta",
    "estes", "estas", "aquele", "aquela", "aquilo", "oque", "pra", "pro", "pras", "pros",
    "ta", "esta", "estao", "estava", "tem", "qual", "quais", "quem", "foi", "era", "ser",
    "ter", "ha", "muito", "pouco", "bem", "mais", "menos", "ja", "ainda", "so", "sozinha",
    "aqui", "ali", "la", "fazer", "faco", "faz", "fazem", "dar", "dou", "da", "dao"
}

# Dicionário de expansão semântica para aproximar a linguagem do tutor aos termos técnicos da clínica Pet Guardian
MAPA_EXPANSAO_SEMANTICA: Dict[str, List[str]] = {
    "cacau": ["cacau", "chocolate", "teobromina", "intoxicacao", "toxico"],
    "chocolate": ["chocolate", "cacau", "teobromina", "bombom", "metilxantinas", "toxico"],
    "uva": ["uva", "passas", "tartarico", "nefrotoxico", "renal"],
    "passa": ["passas", "uva", "tartarico", "nefrotoxico", "renal"],
    "passas": ["passas", "uva", "tartarico", "nefrotoxico", "renal"],
    "panetone": ["passas", "uva", "chocolate", "toxico"],
    "cebola": ["cebola", "alho", "anemia", "hemolitica", "toxico"],
    "alho": ["alho", "cebola", "anemia", "hemolitica", "toxico"],
    "xilitol": ["xilitol", "adocante", "chiclete", "hipoglicemia", "toxico"],
    "macadamia": ["macadamia", "noz", "paresia", "neuromuscular", "toxico"],
    "cafe": ["cafe", "cafeina", "energetico", "taquicardia", "toxico"],
    "lirio": ["lirio", "planta", "necrose", "renal", "toxico", "felino"],
    "comigo": ["comigo", "espada", "planta", "oxalato", "asfixia", "toxico"],
    "espada": ["espada", "comigo", "planta", "oxalato", "asfixia", "toxico"],
    "raticida": ["raticida", "chumbinho", "veneno", "anticoagulante", "hemorragia", "toxico"],
    "chumbinho": ["chumbinho", "raticida", "veneno", "toxico", "emergencia"],
    "sanitaria": ["sanitaria", "cloro", "desinfetante", "queimadura", "corrosivo", "toxico"],
    "cloro": ["cloro", "sanitaria", "desinfetante", "queimadura", "toxico"],
    "filhote": ["filhote", "bebe", "puppy", "vacina", "v8", "v10", "imunizacao", "pediatrico"],
    "bebe": ["filhote", "bebe", "vacina", "pediatrico"],
    "puppy": ["filhote", "vacina", "pediatrico"],
    "idoso": ["senior", "idoso", "geriatrico", "check-up", "rins", "semestral"],
    "velho": ["senior", "idoso", "geriatrico", "check-up", "rins", "semestral"],
    "senior": ["senior", "idoso", "geriatrico", "check-up", "rins", "semestral"],
    "geriatrico": ["senior", "idoso", "geriatrico", "check-up", "rins"],
    "pequeno": ["pequeno", "tartaro", "dentes", "mitral", "traqueia", "escovacao"],
    "medio": ["medio", "peso", "obesidade", "exercicio", "otite", "pele"],
    "grande": ["grande", "displasia", "articulacao", "torcao", "gastrica", "comedouro"],
    "vomito": ["vomito", "diarreia", "gastrointestinal", "estomago", "inducao"],
    "vomitando": ["vomito", "diarreia", "gastrointestinal", "estomago"],
    "vomitou": ["vomito", "diarreia", "gastrointestinal", "estomago"],
    "diarreia": ["diarreia", "vomito", "gastrointestinal", "fezes"],
    "oxigenada": ["oxigenada", "sal", "inducao", "vomito", "proibicao"],
    "sal": ["sal", "oxigenada", "inducao", "vomito", "proibicao"],
    "vomitar": ["vomito", "inducao", "sal", "oxigenada"],
    "engasgo": ["engasgo", "heimlich", "asfixia", "garganta", "socorros"],
    "engasgado": ["engasgo", "heimlich", "asfixia", "garganta", "socorros"],
    "calor": ["insolacao", "calor", "hipertermia", "braquicefalico", "pug", "bulldog"],
    "insolacao": ["insolacao", "calor", "hipertermia", "braquicefalico"],
    "abelha": ["abelha", "picada", "edema", "anafilatico", "alergia"],
    "picada": ["picada", "abelha", "cobra", "edema", "anafilatico", "alergia"],
    "paracetamol": ["paracetamol", "dipirona", "ibuprofeno", "remedio", "medicamento", "humano", "letal"],
    "tylenol": ["paracetamol", "medicamento", "humano", "letal"],
    "dipirona": ["dipirona", "paracetamol", "ibuprofeno", "remedio", "medicamento", "humano"],
    "ibuprofeno": ["ibuprofeno", "paracetamol", "remedio", "medicamento", "humano", "ulceras"],
    "aspirina": ["aspirina", "remedio", "medicamento", "humano"],
    "remedio": ["medicamento", "remedio", "humano", "paracetamol", "farmacologico"],
    "medicamento": ["medicamento", "remedio", "humano", "farmacologico"],
    "racao": ["racao", "transicao", "alimentacao", "nutricao"],
    "fruta": ["fruta", "maca", "banana", "melancia", "petisco", "permitida"],
    "frutas": ["fruta", "maca", "banana", "melancia", "petisco", "permitida"],
    "legume": ["legumes", "cenoura", "abobora", "chuchu", "petisco"],
    "legumes": ["legumes", "cenoura", "abobora", "chuchu", "petisco"],
    "osso": ["osso", "perfuracao", "galinha", "cozido", "obstrucao"],
    "ossos": ["osso", "perfuracao", "galinha", "cozido", "obstrucao"],
    "gato": ["gato", "felino", "urinaria", "flutd", "agua", "sache", "areia"],
    "gatos": ["gato", "felino", "urinaria", "flutd", "agua", "sache", "areia"],
    "morfina": ["morfina", "tramadol", "opioide", "receita", "dosagem", "prescricao", "medicamento", "controlado"],
    "tramadol": ["tramadol", "morfina", "opioide", "receita", "dosagem", "prescricao", "controlado"],
    "receita": ["receita", "prescricao", "dosagem", "morfina", "antibiotico", "corticoide", "medicamento"],
    "prescricao": ["prescricao", "receita", "dosagem", "medicamento", "controlado"],
    "injetavel": ["injetavel", "morfina", "dosagem", "medicamento", "prescricao"],
    "dosagem": ["dosagem", "posologia", "receita", "prescricao", "medicamento", "morfina"],
    "antibiotico": ["antibiotico", "receita", "prescricao", "dosagem", "medicamento"],
    "corticoide": ["corticoide", "prednisolona", "dexametasona", "receita", "dosagem", "medicamento"],
    "vacina": ["vacina", "filhote", "imunizacao", "v8", "v10", "pediatrico"],
    "vacinas": ["vacina", "filhote", "imunizacao", "v8", "v10", "pediatrico"],
    "vacinacao": ["vacina", "filhote", "imunizacao", "pediatrico"],
    "dente": ["dentes", "tartaro", "escovacao", "pequeno", "oral"],
    "dentes": ["dentes", "tartaro", "escovacao", "pequeno", "oral"],
    "escovacao": ["escovacao", "dentes", "tartaro", "pequeno"],
    "tartaro": ["tartaro", "dentes", "escovacao", "pequeno"],
    "alimentacao": ["alimentacao", "nutricao", "racao", "transicao"],
    "nutricao": ["nutricao", "alimentacao", "racao", "transicao"],
    "displasia": ["displasia", "articulacao", "grande", "porte", "cartilagem"],
    "articulacao": ["articulacao", "displasia", "grande", "condroitina"],
    "articulacoes": ["articulacao", "displasia", "grande", "condroitina"],
    "checkup": ["check-up", "senior", "idoso", "geriatrico", "sdma", "semestral"],
    "sdma": ["sdma", "rins", "renal", "senior", "idoso", "check-up"]
}

def normalizar_texto(texto: str) -> str:
    """
    Remove acentuações e caracteres diacríticos, convertendo para minúsculas.
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

def tokenizar_com_ngrams(texto: str, n_max: int = 2) -> List[str]:
    """
    Normaliza o texto, divide em palavras alfanuméricas, remove stopwords
    e gera unigramas e bigramas para enriquecimento vetorial.
    """
    texto_norm = normalizar_texto(texto)
    palavras_brutas = re.findall(r'[a-z0-9]+', texto_norm)
    
    palavras = [p for p in palavras_brutas if (p not in STOPWORDS_PT and len(p) > 1) or p in {"v8", "v10"}]
    
    tokens: List[str] = list(palavras)
    
    if n_max >= 2 and len(palavras) >= 2:
        for i in range(len(palavras) - 1):
            bigrama = f"{palavras[i]}_{palavras[i+1]}"
            tokens.append(bigrama)
            
    return tokens

def expansao_semantica_veterinaria(tokens: List[str]) -> List[str]:
    """
    Expande a lista de tokens incluindo sinônimos clínicos veterinários
    específicos da Pet Guardian para aumentar a precisão na busca vetorial.
    """
    tokens_expandidos = list(tokens)
    for t in tokens:
        chave = t.split("_")[0]
        if chave in MAPA_EXPANSAO_SEMANTICA:
            for sinonimo in MAPA_EXPANSAO_SEMANTICA[chave]:
                if sinonimo not in tokens_expandidos:
                    tokens_expandidos.append(sinonimo)
    return tokens_expandidos
