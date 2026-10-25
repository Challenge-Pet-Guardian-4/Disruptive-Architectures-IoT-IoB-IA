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
    "sdma": ["sdma", "rins", "renal", "senior", "idoso", "check-up"],
    # Expansões das áreas de comportamento, higiene/pele, reprodução e estilo de vida
    "late": ["late", "latido", "latir", "destruicao", "tedio", "energia", "enriquecimento"],
    "latindo": ["latindo", "latido", "latir", "destruicao", "tedio", "energia", "enriquecimento"],
    "latido": ["latido", "latir", "destruicao", "tedio", "energia", "enriquecimento"],
    "latir": ["latir", "latido", "destruicao", "tedio", "energia", "enriquecimento"],
    "destroi": ["destroi", "latido", "latir", "destruicao", "tedio", "energia", "enriquecimento"],
    "destruindo": ["destruindo", "latido", "latir", "destruicao", "tedio", "energia", "enriquecimento"],
    "destruiu": ["destruiu", "latido", "latir", "destruicao", "tedio", "energia", "enriquecimento"],
    "adestrar": ["adestrar", "adestramento", "treino", "reforco", "positivo", "socializacao"],
    "adestrador": ["adestrador", "adestramento", "treino", "reforco", "positivo", "socializacao"],
    "adestramento": ["adestramento", "treino", "reforco", "positivo", "socializacao"],
    "treinar": ["treinar", "adestramento", "treino", "reforco", "positivo", "socializacao"],
    "treino": ["treino", "adestramento", "reforco", "positivo", "socializacao"],
    "gritar": ["gritar", "adestramento", "treino", "reforco", "positivo", "socializacao"],
    "educar": ["educar", "adestramento", "treino", "reforco", "positivo", "socializacao"],
    "rosnou": ["rosnou", "agressividade", "rosnar", "mordida", "medo", "estresse"],
    "rosnando": ["rosnando", "agressividade", "rosnar", "mordida", "medo", "estresse"],
    "rosnar": ["rosnar", "agressividade", "mordida", "medo", "estresse"],
    "mordeu": ["mordeu", "agressividade", "rosnar", "mordida", "medo", "estresse"],
    "morder": ["morder", "agressividade", "rosnar", "mordida", "medo", "estresse"],
    "mordida": ["mordida", "agressividade", "rosnar", "medo", "estresse"],
    "agressivo": ["agressivo", "agressividade", "rosnar", "mordida", "medo", "estresse"],
    "cocando": ["cocando", "coceira", "dermatite", "alergia", "pele", "pulgas"],
    "coca": ["coca", "coceira", "dermatite", "alergia", "pele", "pulgas"],
    "coceira": ["coceira", "dermatite", "alergia", "pele", "pulgas"],
    "alergia": ["alergia", "coceira", "dermatite", "pele", "pulgas"],
    "dermatite": ["dermatite", "coceira", "alergia", "pele", "pulgas"],
    "vermifugar": ["vermifugar", "vermifugacao", "vermifugo", "verminose", "vermes", "frequencia", "intervalo"],
    "vermifugo": ["vermifugo", "vermifugacao", "verminose", "vermes", "frequencia"],
    "verme": ["verme", "vermifugacao", "vermifugo", "verminose", "vermes"],
    "vermes": ["vermes", "vermifugacao", "vermifugo", "verminose"],
    "verminose": ["verminose", "vermifugacao", "vermifugo", "vermes"],
    "custos": ["custos", "posse", "responsavel", "planejamento", "mensal"],
    "custo": ["custo", "custos", "posse", "responsavel", "planejamento", "mensal"],
    "gasto": ["gasto", "custos", "posse", "responsavel", "planejamento", "mensal"],
    "gastos": ["gastos", "custos", "posse", "responsavel", "planejamento", "mensal"],
    "crianca": ["crianca", "criancas", "convivencia", "supervisao", "mordida", "pet"],
    "criancas": ["criancas", "convivencia", "supervisao", "mordida", "pet"],
    "filho": ["filho", "criancas", "convivencia", "supervisao", "mordida", "pet"],
    "filha": ["filha", "criancas", "convivencia", "supervisao", "mordida", "pet"],
    "banho": ["banho", "shampoo", "frequencia", "higiene"],
    "shampoo": ["shampoo", "banho", "frequencia", "higiene"],
    "unha": ["unha", "unhas", "corte", "almofadinhas", "patas"],
    "unhas": ["unhas", "corte", "almofadinhas", "patas"],
    "castrar": ["castrar", "castracao", "cirurgia", "esterilizacao", "pos"],
    "castracao": ["castracao", "castrar", "cirurgia", "esterilizacao", "pos"],
    "castrada": ["castrada", "castracao", "castrar", "cirurgia", "esterilizacao", "pos"],
    "castrado": ["castrado", "castracao", "castrar", "cirurgia", "esterilizacao", "pos"],
    "cio": ["cio", "gestacao", "parto", "fertil", "cadela", "gata"],
    "gravida": ["gravida", "cio", "gestacao", "parto", "fertil", "cadela", "gata"],
    "prenhe": ["prenhe", "cio", "gestacao", "parto", "fertil", "cadela", "gata"],
    "parto": ["parto", "cio", "gestacao", "fertil", "cadela", "gata"],
    "viagem": ["viagem", "viajar", "transporte", "caixa", "documentos"],
    "viajar": ["viajar", "viagem", "transporte", "caixa", "documentos"],
    "aviao": ["aviao", "viagem", "viajar", "transporte", "caixa", "documentos"],
    "carro": ["carro", "viagem", "viajar", "transporte", "caixa", "documentos"],
    "adotar": ["adotar", "adocao", "primeiro", "checkup", "adaptacao"],
    "adocao": ["adocao", "adotar", "primeiro", "checkup", "adaptacao"],
    "adotei": ["adotei", "adocao", "adotar", "primeiro", "checkup", "adaptacao"],
    "abandonar": ["abandonar", "abandono", "crime", "lei", "maus", "tratos", "denuncia"],
    "abandono": ["abandono", "crime", "lei", "maus", "tratos", "denuncia"],
    "crime": ["crime", "abandono", "lei", "maus", "tratos", "denuncia"],
    "lei": ["lei", "abandono", "crime", "maus", "tratos", "denuncia"],
    "ouvido": ["ouvido", "otite", "orelha", "limpeza", "cotonete"],
    "ouvidos": ["ouvidos", "otite", "ouvido", "orelha", "limpeza", "cotonete"],
    "orelha": ["orelha", "otite", "ouvido", "limpeza", "cotonete"],
    "orelhas": ["orelhas", "otite", "ouvido", "orelha", "limpeza", "cotonete"],
    "pulga": ["pulga", "pulgas", "carrapatos", "antipulgas", "erliquiose", "permetrina"],
    "pulgas": ["pulgas", "carrapatos", "antipulgas", "erliquiose", "permetrina"],
    "carrapato": ["carrapato", "pulgas", "carrapatos", "antipulgas", "erliquiose", "permetrina"],
    "carrapatos": ["carrapatos", "pulgas", "antipulgas", "erliquiose", "permetrina"],
    # Doenças infecciosas e viroses
    "parvovirose": ["parvovirose", "parvo", "cinomose", "vomito", "sangue", "letargia"],
    "parvo": ["parvovirose", "parvo", "cinomose", "vomito", "sangue"],
    "cinomose": ["cinomose", "parvovirose", "mioclonia", "secrecao", "tosse"],
    "fiv": ["fiv", "felv", "aids", "felina", "imunodeficiencia", "gato"],
    "felv": ["felv", "fiv", "leucemia", "felina", "v5", "gato"],
    "tosse": ["tosse", "canis", "gripe", "canina", "traqueobronquite", "bordetella", "engasgo"],
    "leishmaniose": ["leishmaniose", "mosquito", "palha", "deltametrina", "coleira", "zoonose"],
    "giardia": ["giardia", "giardiase", "fezes", "muco", "diarreia", "amonia"],
    "giardiase": ["giardiase", "giardia", "fezes", "muco", "diarreia", "amonia"]
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
    
    # Radicais ("~arran" para arranha/arranhando/arranhador) aproximam flexões do português sem dicionário externo
    radicais = [f"~{p.rstrip('s')[:5]}" for p in palavras if len(p) >= 5]
    tokens: List[str] = list(palavras) + radicais
    
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
