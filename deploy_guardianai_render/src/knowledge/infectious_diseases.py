"""
Base de Conhecimento: Doenças Infecciosas e Vacinais — Pet Guardian
Orientações clínicas sobre as principais viroses, zoonoses e infecções de cães e gatos.
"""
from typing import Dict, Any, List

_SOURCE = "Protocolo de Doenças Infecciosas Pet Guardian"

CHUNKS_INFECTIOUS_DISEASES: List[Dict[str, Any]] = [
    {
        "id": "inf_01",
        "source": _SOURCE,
        "category": "infectious_diseases",
        "urgency": "EMERGENCIA",
        "title": "Parvovirose e Cinomose Canina: Sinais de Alerta, Contágio e Emergência Crítica",
        "content": (
            "Parvovirose e cinomose são viroses altamente contagiosas e letais, especialmente para filhotes não imunizados ou com vacinação incompleta. "
            "A parvovirose ataca o trato gastrointestinal, provocando vômitos incontroláveis, diarreia fétida com sangue vivo, desidratação fulminante e apatia extrema. "
            "A cinomose apresenta fases respiratória (secreção ocular e nasal, tosse), gastrointestinal e neurológica (tremores musculares, convulsões e mioclonias). "
            "Ambas exigem internação em isolamento e suporte intensivo imediato no pronto-socorro da Pet Guardian. "
            "A única forma eficaz de prevenção é o esquema rigoroso de vacinas múltiplas (V8/V10) a partir das 6 a 8 semanas, proibindo contato com a rua antes da imunização completa."
        ),
        "keywords": ["parvovirose", "parvo", "cinomose", "vomito com sangue", "diarreia com sangue", "fezes com sangue", "secrecao no nariz", "secrecao ocular", "mioclonia", "v8", "v10", "filhote apatico"]
    },
    {
        "id": "inf_02",
        "source": _SOURCE,
        "category": "infectious_diseases",
        "urgency": "alta",
        "title": "FIV e FeLV em Gatos: Vírus da Imunodeficiência e Leucemia Felina",
        "content": (
            "FIV (Vírus da Imunodeficiência Felina, 'AIDS felina') e FeLV (Vírus da Leucemia Felina) são retrovírus graves exclusivos de gatos, não transmissíveis a humanos ou cães. "
            "A FIV é transmitida principalmente por mordidas e brigas entre gatos que têm acesso à rua; a FeLV é transmitida por contato próximo amigável (saliva em lambedura mútua, potes compartilhados). "
            "Gatos positivos necessitam de vida estritamente indoor (sem acesso à rua), enriquecimento ambiental sem estresse, alimentação de alta digestibilidade e check-up semestral. "
            "Todo gato recém-adotado deve ser testado (teste rápido SNAP ELISA / PCR) antes de ser introduzido a outros felinos da casa. A vacina quíntupla (V5) protege contra FeLV em gatos negativos."
        ),
        "keywords": ["fiv", "felv", "aids felina", "leucemia felina", "teste fiv felv", "v5", "quintupula", "gato positivo", "acesso a rua", "mordida de gato"]
    },
    {
        "id": "inf_03",
        "source": _SOURCE,
        "category": "infectious_diseases",
        "urgency": "moderada",
        "title": "Tosse dos Canis (Traqueobronquite Infecciosa): Sintomas e Prevenção",
        "content": (
            "A tosse dos canis ('gripe canina') é uma síndrome respiratória altamente contagiosa causada por agentes como Bordetella bronchiseptica e vírus da parainfluenza. "
            "O sintoma clássico é uma tosse seca, alta, estridente e em acessos frequentes, muitas vezes acompanhada de ânsia ou vômito de espuma branca, o que frequentemente faz o tutor acreditar que o pet engasgou com um osso ou objeto. "
            "O animal geralmente mantém o apetite e a disposição nas formas brandas, mas filhotes e idosos podem evoluir para pneumonia. "
            "A transmissão ocorre em creches, hotéis, parques e exposições. A prevenção é realizada por meio da vacina específica (intranasal, oral ou injetável), recomendada anualmente para animais sociáveis."
        ),
        "keywords": ["tosse dos canis", "tosse de cachorro", "gripe canina", "cachorro tossindo", "parece engasgado", "espuma branca", "bordetella", "traqueobronquite", "creche canina"]
    },
    {
        "id": "inf_04",
        "source": _SOURCE,
        "category": "infectious_diseases",
        "urgency": "alta",
        "title": "Leishmaniose Visceral Canina: Transmissão, Zoonose e Medidas Preventivas",
        "content": (
            "A leishmaniose visceral é uma doença crônica grave e uma zoonose (pode infectar seres humanos), causada pelo protozoário Leishmania infantum. "
            "A transmissão NÃO ocorre por mordida, saliva ou carinho do cão, mas EXCLUSIVAMENTE pela picada da fêmea do mosquito-palha (Lutzomyia longipalpis), comum no entardecer e em áreas com matéria orgânica. "
            "Sinais clínicos em cães: emagrecimento progressivo, crescimento anormal das unhas (onicogrifose), lesões de pele ao redor dos olhos e focinho, perda de pelos, feridas de difícil cicatrização e problemas renais. "
            "A prevenção primária essencial consiste no uso contínuo de coleiras repelentes à base de deltametrina e inseticidas no ambiente. O diagnóstico precoce e o acompanhamento veterinário são obrigatórios."
        ),
        "keywords": ["leishmaniose", "leishmaniose canina", "mosquito palha", "coleira repelente", "deltametrina", "onicogrifose", "unha crescendo muito", "ferida no focinho", "zoonose"]
    },
    {
        "id": "inf_05",
        "source": _SOURCE,
        "category": "infectious_diseases",
        "urgency": "moderada",
        "title": "Giardíase e Parasitoses Intestinais: Contágio Hídrico e Higiene Ambiental",
        "content": (
            "A giárdia é um protozoário microscópico que coloniza o intestino delgado de cães, gatos e seres humanos. "
            "A infecção ocorre pela ingestão de cistos presentes em água parada, poças na rua, fezes contaminadas ou gramados de parques. "
            "Provoca diarreia pastosa ou líquida intermitente, esverdeada ou amarelada, com muco, odor muito forte e gases, além de perda de peso sem febre aparente. "
            "O tratamento deve ser prescrito pelo veterinário e incluir SEMPRE todos os animais da residência simultaneamente, combinado com rigorosa desinfecção ambiental com amônia quaternária, pois os cistos resistem ao cloro comum. "
            "Recolha sempre as fezes imediatamente e ofereça exclusivamente água filtrada ou potável ao pet."
        ),
        "keywords": ["giardia", "giardiase", "fezes com muco", "diarreia pastosa", "diarreia amarela", "agua parada", "amonia quaternaria", "parasita intestinal", "poca de agua"]
    }
]
