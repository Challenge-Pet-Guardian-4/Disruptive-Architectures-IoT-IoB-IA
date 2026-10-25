"""
Base de Conhecimento: Comportamento, Adestramento e Bem-Estar — Pet Guardian
Orientações de manejo comportamental de cães e gatos baseadas em reforço positivo e saúde emocional.
"""
from typing import Dict, Any, List

_SOURCE = "Guia de Comportamento e Bem-Estar Pet Guardian"

CHUNKS_BEHAVIOR: List[Dict[str, Any]] = [
    {
        "id": "beh_01",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "behavior",
        "title": "Adestramento com Reforço Positivo e Janela de Socialização de Filhotes",
        "content": (
            "O adestramento mais seguro e eficaz utiliza reforço positivo: recompensar com petisco, carinho ou brincadeira o comportamento desejado "
            "imediatamente após ele ocorrer. Gritos, tapas e punições físicas geram medo, estresse crônico e podem aumentar a agressividade. "
            "Sessões curtas (5 a 10 minutos), comandos básicos (senta, fica, vem) e consistência de toda a família são fundamentais. "
            "Em cães, a janela de socialização vai de cerca de 3 a 14 semanas de vida: nesse período o filhote deve conhecer, de forma gradual e positiva, "
            "pessoas, sons, superfícies e outros animais saudáveis, respeitando o protocolo de vacinação antes de frequentar locais públicos."
        ),
        "keywords": ["adestramento", "treino", "treinar", "reforco positivo", "comando", "socializacao", "obediencia", "educar cachorro", "punicao", "castigo"]
    },
    {
        "id": "beh_02",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "behavior",
        "title": "Latidos Excessivos, Destruição de Objetos e Tédio em Cães",
        "content": (
            "Latidos constantes, destruição de móveis e escavação costumam indicar excesso de energia, tédio, medo ou falta de estímulo mental, e não 'birra'. "
            "Medidas recomendadas: passeios diários adequados ao porte e à idade, brinquedos recheáveis e interativos, tapetes de farejar, rodízio de brinquedos "
            "e momentos de treino. Identifique o gatilho (barulhos, pessoas na rua, solidão) e nunca puna o cão depois do fato, pois ele não associa a bronca ao ato. "
            "Se o comportamento surgir de repente, avalie causas médicas como dor, dificuldades cognitivas em idosos ou problemas de visão e audição."
        ),
        "keywords": ["latido", "latindo", "latir", "destruicao", "destruindo", "morde moveis", "cavar", "escavar", "tedio", "energia", "hiperativo", "enriquecimento"]
    },
    {
        "id": "beh_03",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "behavior",
        "title": "Gato Arranhando Móveis: Instinto, Arranhadores e Alternativas Seguras",
        "content": (
            "Arranhar é um comportamento natural e necessário dos gatos: serve para afiar e remover a capa das unhas, esticar a musculatura e marcar território "
            "com glândulas das patas. Em vez de repreender, ofereça arranhadores estáveis, altos o bastante para o gato se esticar por completo, de sisal ou papelão, "
            "posicionados perto dos locais de descanso e dos móveis preferidos. Use petiscos e catnip para atrair, e feromônios felinos sintéticos em casos de estresse. "
            "A retirada cirúrgica das unhas (onicectomia) causa dor crônica e problemas de comportamento e não é recomendada; mantenha as unhas aparadas regularmente."
        ),
        "keywords": ["gato arranhando", "arranhador", "arranha sofa", "arranhar", "unhas gato", "marcar territorio", "sisal", "catnip", "feromonio", "onicectomia"]
    },
    {
        "id": "beh_04",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "behavior",
        "title": "Gato Urinando Fora da Caixa de Areia: Causas Médicas e Manejo Ambiental",
        "content": (
            "Urinar fora da caixa é um sinal de alerta e deve ser investigado primeiro como problema de saúde: cistite, cálculos e obstrução urinária (FLUTD) são comuns, "
            "e a obstrução em machos é emergência fatal em 24 a 72 horas (esforço sem urinar, miados de dor, lamber a região genital). Descartada a causa médica, ajuste o ambiente: "
            "mantenha uma caixa por gato mais uma extra, em locais tranquilos e longe da comida, remova os resíduos diariamente, troque a areia com frequência, "
            "evite perfumes fortes e mudanças bruscas de areia. Estresse por mudança de rotina, novo animal ou reforma também desencadeia o comportamento."
        ),
        "keywords": ["gato xixi fora", "urinando fora da caixa", "caixa de areia", "areia sanitaria", "gato faz xixi", "cistite", "flutd", "obstrucao urinaria", "marcacao urina", "estresse gato"]
    },
    {
        "id": "beh_05",
        "source": _SOURCE,
        "urgency": "moderada",
        "category": "behavior",
        "title": "Agressividade, Rosnados e Mordidas: Sinais de Estresse e Quando Buscar Ajuda",
        "content": (
            "Rosnar, mostrar os dentes, enrijecer o corpo ou morder são formas de comunicação: o animal está avisando desconforto, medo, dor ou proteção de recursos (comida, brinquedo, espaço). "
            "Não puna o rosnado, pois isso elimina o aviso e torna a mordida imprevisível. Sinais precoces de estresse incluem lamber os lábios, bocejar, virar o rosto, orelhas para trás e cauda baixa. "
            "Mudança súbita para agressividade exige exame veterinário para descartar dor, problemas hormonais ou neurológicos. Em casos persistentes, procure um médico-veterinário comportamentalista, "
            "evite situações-gatilho e mantenha crianças sempre supervisionadas."
        ),
        "keywords": ["agressivo", "agressividade", "rosnando", "rosnar", "morder", "mordida", "mordeu", "medo", "protecao de comida", "estresse cachorro", "comportamentalista"]
    },
    {
        "id": "beh_06",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "behavior",
        "title": "Passeios, Exercício Físico e Enriquecimento Ambiental por Porte e Idade",
        "content": (
            "A necessidade de exercício varia: cães de pequeno porte costumam precisar de 30 a 60 minutos de atividade diária, enquanto raças ativas e de grande porte (Border Collie, Labrador, Pastor) "
            "podem exigir 1 a 2 horas, combinando caminhada, corrida e jogos. Filhotes em crescimento e cães idosos pedem atividades mais curtas e de baixo impacto. "
            "Evite exercício intenso nas horas de calor, teste o asfalto com a mão antes de passear (queimaduras nas patas) e redobre o cuidado com raças braquicefálicas (Pug, Buldogue), que sofrem com insolação. "
            "Para gatos, ofereça prateleiras, esconderijos, brinquedos de caça e brincadeiras diárias com varinhas para prevenir obesidade e tédio."
        ),
        "keywords": ["passeio", "passear", "exercicio", "atividade fisica", "caminhada", "gasto de energia", "asfalto quente", "sedentarismo", "brincadeira", "enriquecimento ambiental"]
    },
    {
        "id": "beh_07",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "behavior",
        "title": "Chegada de um Novo Pet em Casa e Apresentação Entre Animais",
        "content": (
            "A adaptação segue o princípio dos 3-3-3: cerca de 3 dias para se sentir seguro, 3 semanas para aprender a rotina e 3 meses para criar vínculo pleno. "
            "Prepare um espaço próprio com cama, água, comida e (para gatos) caixa de areia. Ao apresentar um novo animal a um residente, comece com odores (troca de mantas), "
            "depois contato visual por barreira e, só então, encontros curtos e supervisionados com recompensas. Gatos exigem apresentação ainda mais gradual, com ambientes separados por dias ou semanas. "
            "Mantenha vacinas, vermífugo e check-up do recém-chegado em dia antes do contato com os demais pets da casa."
        ),
        "keywords": ["novo pet", "adotei", "adaptacao", "apresentar gato", "apresentar cachorro", "novo filhote em casa", "convivencia entre pets", "ciume", "primeiro dia em casa"]
    },
]
