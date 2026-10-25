"""
Base de Conhecimento: Higiene, Pele, Pelagem e Controle de Parasitas — Pet Guardian
Orientações de higiene e dermatologia preventiva para cães e gatos.
"""
from typing import Dict, Any, List

_SOURCE = "Guia de Higiene e Dermatologia Pet Guardian"

CHUNKS_HYGIENE_SKIN: List[Dict[str, Any]] = [
    {
        "id": "hyg_01",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "hygiene_skin",
        "title": "Banho: Frequência Correta, Produtos Adequados e Secagem",
        "content": (
            "Cães saudáveis costumam tomar banho a cada 15 a 30 dias, conforme pelagem, estilo de vida e orientação veterinária; banhos excessivos ressecam a pele e removem a proteção natural. "
            "Use SEMPRE shampoo e condicionador veterinários: produtos humanos têm pH diferente e causam irritação e dermatites. Enxágue por completo, proteja os ouvidos para a água não entrar "
            "e seque muito bem, especialmente dobras de pele e orelhas, pois a umidade favorece fungos e otites. Gatos geralmente se autolimpam e raramente precisam de banho; "
            "quando necessário, use produtos específicos para felinos e minimize o estresse."
        ),
        "keywords": ["banho", "dar banho", "tomar banho", "shampoo", "frequencia do banho", "secar", "secagem", "condicionador", "higiene", "pelagem"]
    },
    {
        "id": "hyg_02",
        "source": _SOURCE,
        "urgency": "alta",
        "category": "hygiene_skin",
        "title": "Pulgas e Carrapatos: Prevenção, Doenças Transmitidas e Perigo da Permetrina em Gatos",
        "content": (
            "Pulgas causam coceira intensa, anemia em filhotes e dermatite alérgica; carrapatos transmitem doenças graves como erliquiose e babesiose (febre, apatia, gengivas pálidas e sangramentos). "
            "A prevenção deve ser contínua, com antiparasitários (comprimidos mastigáveis, pipetas ou coleiras) prescritos pelo veterinário de acordo com espécie, peso e idade, e tratamento do ambiente. "
            "ATENÇÃO: nunca aplique em gatos produtos de uso canino que contenham permetrina, pois são altamente tóxicos para felinos e provocam tremores, convulsões e podem levar à morte. "
            "Remova carrapatos com pinça adequada, sem esmagar, e observe o animal nos dias seguintes."
        ),
        "keywords": ["pulga", "pulgas", "carrapato", "carrapatos", "antipulgas", "coceira", "erliquiose", "babesiose", "doenca do carrapato", "permetrina", "coleira antipulgas", "ectoparasita"]
    },
    {
        "id": "hyg_03",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "hygiene_skin",
        "title": "Coceira, Alergias de Pele e Dermatite Alérgica: Causas e Conduta",
        "content": (
            "As principais causas de coceira em cães e gatos são alergia à picada de pulga (DAPP), alergias alimentares, dermatite atópica, sarna e fungos. "
            "Sinais: lambedura constante das patas, coçar-se até ferir, vermelhidão, perda de pelos em placas, cheiro forte e pele escurecida. "
            "O tratamento depende do diagnóstico correto, que pode envolver controle rigoroso de pulgas, dieta de exclusão supervisionada e exames de pele. "
            "Não utilize corticoides, pomadas humanas ou receitas caseiras por conta própria: mascaram o problema, causam efeitos colaterais e podem piorar infecções. "
            "Agende avaliação veterinária se a coceira durar mais de alguns dias ou houver feridas."
        ),
        "keywords": ["coceira", "coçando", "alergia de pele", "dermatite", "atopia", "sarna", "fungo", "micose", "queda de pelo", "lambendo patas", "feridas na pele", "vermelhidao"]
    },
    {
        "id": "hyg_04",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "hygiene_skin",
        "title": "Higiene dos Ouvidos e Otites: Sinais de Alerta e Limpeza Segura",
        "content": (
            "A otite é muito comum em cães de orelhas caídas ou peludas (Cocker, Basset, Poodle) e em animais alérgicos. Sinais: balançar a cabeça, coçar as orelhas, mau cheiro, secreção escura ou amarelada, "
            "vermelhidão e dor ao toque. A limpeza preventiva deve ser feita com solução ceruminolítica veterinária, aplicando o produto no canal, massageando a base da orelha e deixando o animal sacudir a cabeça; "
            "depois, limpe apenas a parte visível com gaze. NUNCA use cotonetes dentro do canal, água oxigenada, álcool ou vinagre. Em caso de sinais de infecção, procure o veterinário, "
            "pois o tratamento exige identificar o agente (bactéria, fungo ou ácaro)."
        ),
        "keywords": ["otite", "ouvido", "ouvidos", "orelha", "orelhas", "limpeza de ouvido", "balancando a cabeca", "secrecao no ouvido", "cheiro no ouvido", "cotonete", "cerume"]
    },
    {
        "id": "hyg_05",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "hygiene_skin",
        "title": "Corte de Unhas e Cuidados com as Patas e Almofadinhas",
        "content": (
            "Unhas longas alteram a postura, causam dor, quebram e podem encravar. O corte costuma ser necessário a cada 2 a 4 semanas; um sinal clássico é ouvir as unhas 'estalando' no piso. "
            "Use cortador adequado ao porte, corte apenas a ponta e evite a parte rosada (vascularizada) para não causar sangramento; em unhas escuras, corte pouco a pouco. "
            "Se sangrar, comprima com gaze limpa e use pó hemostático veterinário. Examine as almofadinhas após passeios em busca de cortes, espinhos e queimaduras por asfalto quente, "
            "e mantenha os pelos entre os coxins aparados. Faça o treinamento com petiscos desde filhote para facilitar a rotina."
        ),
        "keywords": ["unha", "unhas", "cortar unha", "corte de unhas", "unha encravada", "almofadinhas", "patas", "coxins", "unha sangrando", "cortador de unha"]
    },
    {
        "id": "hyg_06",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "hygiene_skin",
        "title": "Escovação, Troca de Pelos e Tosa: O Que Pode e o Que Evitar",
        "content": (
            "A escovação regular remove pelos mortos, previne nós e estimula a circulação: diária em pelagens longas, 2 a 3 vezes por semana nas curtas, e mais frequente na troca de pelos. "
            "A tosa higiênica (região íntima, patas e barriga) é recomendada; já a raspagem total de raças de pelagem dupla (Husky, Golden Retriever, Pastor Alemão, Lulu da Pomerânia) NÃO é indicada, "
            "pois prejudica a termorregulação, expõe a pele ao sol e o pelo pode crescer de forma irregular. Em dias quentes, ofereça água fresca e sombra. "
            "Nós muito apertados ('embolados') devem ser tratados por um profissional, nunca com tesoura solta, para evitar cortes na pele."
        ),
        "keywords": ["escovacao", "escovar", "pelo", "pelos", "tosa", "tosar", "raspar", "troca de pelo", "queda de pelo", "nos no pelo", "pelagem dupla", "husky"]
    },
    {
        "id": "hyg_07",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "hygiene_skin",
        "title": "Vermifugação: Frequência e Sinais de Verminose",
        "content": (
            "Vermes intestinais (lombrigas, ancilóstomos, giárdia) causam diarreia, barriga distendida, perda de peso, pelos opacos e, em filhotes, anemia e atraso no crescimento; "
            "alguns são transmissíveis aos humanos (zoonoses). O protocolo geralmente inicia nas primeiras semanas de vida e é repetido em intervalos curtos nos filhotes; em adultos, "
            "costuma ser repetido a cada 3 a 6 meses, conforme risco e orientação do veterinário. Utilize apenas vermífugos adequados à espécie e ao peso, nunca remédios caseiros, "
            "e recolha sempre as fezes para quebrar o ciclo de contaminação. Observar vermes nas fezes ou no vômito, ou arrastar o bumbum no chão, indica necessidade de consulta."
        ),
        "keywords": ["vermifugo", "vermifugacao", "vermifugar", "vermes", "verme", "verminose", "lombriga", "giardia", "barriga inchada", "arrastando o bumbum", "diarreia filhote", "antiparasitario interno", "quanto tempo vermifugar", "frequencia vermifugacao", "intervalo vermifugo", "de quanto em quanto", "quando vermifugar"]
    },
]
