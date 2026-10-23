"""
Base de Conhecimento: Toxicologia Veterinária Curada — Pet Guardian
Catálogo expandido de alimentos, plantas residenciais, produtos químicos e fármacos tóxicos.
"""
from typing import Dict, Any, List

CHUNKS_TOXICOLOGY: List[Dict[str, Any]] = [
    {
        "id": "tox_01",
        "source": "Protocolo de Toxicologia Pet Guardian",
        "category": "toxicology",
        "title": "Intoxicação por Chocolate e Derivados (Teobromina)",
        "content": (
            "O chocolate contém teobromina e cafeína, metilxantinas que cães e gatos metabolizam muito lentamente. "
            "A ingestão provoca hiperestimulação neurológica e sobrecarga cardiovascular aguda. Os sintomas incluem "
            "taquicardia, arritmias, tremores musculares, vômitos, diarreia, salivação excessiva e convulsões. Trata-se de uma "
            "emergência veterinária máxima. Conduta imediata: levar o animal sem demora ao pronto-socorro veterinário 24h Pet Guardian. "
            "Nunca tente induzir vômito caseiro com água oxigenada ou sal, pois há alto risco de necrose gástrica e pneumonia aspirativa."
        ),
        "keywords": ["chocolate", "barra de chocolate", "bombom", "achocolatado", "teobromina", "metilxantinas", "intoxicacao por chocolate", "doce de chocolate"]
    },
    {
        "id": "tox_02",
        "source": "Protocolo de Toxicologia Pet Guardian",
        "category": "toxicology",
        "title": "Intoxicação Grave por Cacau Puro e Bolos/Doces de Cacau",
        "content": (
            "O cacau puro e derivados concentrados (como pó de cacau, chocolate amargo ou bolo de cacau) possuem altíssima concentração "
            "de teobromina, sendo consideravelmente mais letais que o chocolate ao leite. Mesmo pequenos pedaços de produtos com cacau "
            "ingeridos por cães podem desencadear convulsões severas, hipertermia, arritmias cardíacas graves e colapso respiratório. "
            "Trata-se de emergência médica máxima: o tutor deve encaminhar o pet sem demora ao pronto-socorro da Pet Guardian para lavagem "
            "gástrica assistida, fluidoterapia intravenosa e suporte intensivo. Não tente métodos caseiros."
        ),
        "keywords": ["cacau", "bolo de cacau", "cacau em po", "torta de cacau", "chocolate amargo", "bolo de chocolate", "teobromina concentrada"]
    },
    {
        "id": "tox_03",
        "source": "Protocolo de Toxicologia Pet Guardian",
        "category": "toxicology",
        "title": "Toxicidade Renal Aguda por Uvas Frescas e Uvas-Passas",
        "content": (
            "Uvas frescas e uvas-passas contêm ácido tartárico e compostos nefrotóxicos com sensibilidade idiossincrática em cães. "
            "Mesmo uma única uva fresca ou passa pode deflagrar necrose tubular renal aguda severa em poucas horas. Os sinais iniciais incluem "
            "vômitos nas primeiras 2 horas, letargia profunda, dor abdominal, diarreia e posterior anúria (ausência de urina por falência renal). "
            "Conduta: hospitalização imediata 24h na Pet Guardian para fluidoterapia intravenosa contínua antes do estabelecimento da lesão renal irreversível."
        ),
        "keywords": ["uva", "uvas", "uva passa", "uvas passas", "passas", "panetone", "acido tartarico", "insuficiencia renal aguda", "falencia renal"]
    },
    {
        "id": "tox_04",
        "source": "Protocolo de Toxicologia Pet Guardian",
        "category": "toxicology",
        "title": "Anemia Hemolítica Severa por Cebola, Alho e Alho-Poró",
        "content": (
            "Cebola, alho, alho-poró e cebolinha contêm dissulfeto de alilpropila e tiossulfatos que provocam dano oxidativo severo à "
            "hemoglobina de cães e gatos, gerando corpúsculos de Heinz e destruição maciça das hemácias (anemia hemolítica). O alho é cerca "
            "de 5 vezes mais concentrado e tóxico que a cebola. Sintomas surgem dias após a ingestão: apatia extrema, fraqueza, gengivas pálidas "
            "ou amareladas (icterícia), urina escura/avermelhada e respiração ofegante. Exige avaliação veterinária com hemograma urgente e suporte clínico."
        ),
        "keywords": ["cebola", "alho", "tempero", "alho poro", "cebolinha", "comida temperada", "anemia hemolitica", "hemacias", "corpos de heinz"]
    },
    {
        "id": "tox_05",
        "source": "Protocolo de Toxicologia Pet Guardian",
        "category": "toxicology",
        "title": "Choque Hipoglicêmico Fulminante e Falência Hepática por Xilitol",
        "content": (
            "O xilitol é um adoçante artificial presente em chicletes, pastas de dente, balas sem açúcar, doces dietéticos e produtos de panificação. "
            "No organismo canino, desencadeia uma liberação massiva e fulminante de insulina pelo pâncreas, provocando choque hipoglicêmico profundo "
            "em 30 a 60 minutos (andar cambaleante, fraqueza motora, convulsões) e necrose hepática aguda em 24 a 48 horas. Conduta: "
            "emergência médica máxima em hospital veterinário 24h Pet Guardian para infusão glicêmica intravenosa contínua e hepatoprotetores."
        ),
        "keywords": ["xilitol", "xylitol", "adocante", "chiclete", "bala diet", "pasta de dente", "sem acucar", "hipoglicemia", "insulina"]
    },
    {
        "id": "tox_06",
        "source": "Protocolo de Toxicologia Pet Guardian",
        "category": "toxicology",
        "title": "Toxicidade Neuromuscular por Nozes de Macadâmia",
        "content": (
            "As nozes de macadâmia possuem compostos botânicos que causam intoxicação neuromuscular específica em cães. "
            "Os sintomas clínicos manifestam-se em 6 a 24 horas após a ingestão e incluem paresia e fraqueza evidente nas patas traseiras, "
            "incapacidade de ficar em pé, tremores musculares, febre (hipertermia), vômitos e depressão. Exige consulta presencial na Pet Guardian "
            "para controle de dor e monitoramento clínico até a regressão dos sintomas."
        ),
        "keywords": ["macadamia", "noz de macadamia", "nozes", "castanha", "oleaginosas", "paresia", "fraqueza nas patas", "tremores"]
    },
    {
        "id": "tox_07",
        "source": "Protocolo de Toxicologia Pet Guardian",
        "category": "toxicology",
        "title": "Intoxicação Cardíaca por Café, Borra de Café e Energéticos",
        "content": (
            "Café moído, grãos, borra de café, chás pretos/verdes concentrados e energéticos contêm altas doses de cafeína pura. "
            "A ingestão provoca superestimulação aguda do sistema nervoso central, taquicardia severa, hipertensão arterial, arritmias ventriculares, "
            "hipertermia e convulsões em cães e gatos. Conduta recomendada: atendimento veterinário emergencial 24h imediato com suporte cardiovascular "
            "e estabilização hemodinâmica."
        ),
        "keywords": ["cafe", "po de cafe", "borra de cafe", "cafeina", "energetico", "capsula de cafe", "taquicardia", "cha preto", "cha verde"]
    },
    {
        "id": "tox_08",
        "source": "Protocolo de Toxicologia Pet Guardian",
        "category": "toxicology",
        "title": "Plantas Tóxicas Residenciais: Lírio (Letalidade Extrema para Felinos)",
        "content": (
            "Todas as partes do lírio (Lilium spp. e Hemerocallis spp.), incluindo pétalas, folhas, pólen e até a água do vaso, são "
            "EXTREMAMENTE FATAIS para gatos. A ingestão ou lambedura de grãos de pólen do pelo causa necrose tubular renal aguda irreversível "
            "em menos de 48 a 72 horas. Sintomas iniciais: vômitos, salivação, anorexia e letargia. O tratamento com fluidoterapia intensiva "
            "deve ser iniciado nas primeiras 6 horas após o contato no hospital veterinário Pet Guardian para evitar o óbito do felino."
        ),
        "keywords": ["lirio", "lirios", "planta toxica gato", "planta venenosa", "agua do vaso", "polen de lirio", "falencia renal felina"]
    },
    {
        "id": "tox_09",
        "source": "Protocolo de Toxicologia Pet Guardian",
        "category": "toxicology",
        "title": "Plantas Ornamentais Tóxicas: Comigo-Ninguém-Pode e Espada-de-São-Jorge",
        "content": (
            "Plantas residenciais como Comigo-Ninguém-Pode (Dieffenbachia), Espada-de-São-Jorge, Costela-de-Adão e Jiboia possuem cristais "
            "insolúveis de oxalato de cálcio em forma de agulha (ráfides). Ao mastigar a folha, as ráfides perfuram a mucosa bucal, causando "
            "dor intensa, queimação, salivação copiosa, edema grave de língua e lábios e risco iminente de asfixia por edema de glote. "
            "Conduta: lavar a boca com água corrente com cautela e levar imediatamente a um atendimento veterinário presencial."
        ),
        "keywords": ["comigo ninguem pode", "espada de sao jorge", "costela de adao", "jiboia", "planta toxica cachorro", "oxalato de calcio", "edema de glote"]
    },
    {
        "id": "tox_10",
        "source": "Protocolo de Toxicologia Pet Guardian",
        "category": "toxicology",
        "title": "Intoxicação por Produtos Químicos: Raticidas (Chumbinho / Anticoagulantes)",
        "content": (
            "Raticidas anticoagulantes (cumarínicos) inibem a síntese de vitamina K no fígado, impedindo a coagulação sanguínea. "
            "Os sintomas surgem após 2 a 5 dias com hemorragias internas espontâneas, gengivas pálidas, hematomas na pele, sangue na urina/fezes "
            "e tosse com sangue. Já o raticida clandestino 'chumbinho' (aldicarbe/carbamato) causa salivação excessiva, pupilas contraídas (miose), "
            "convulsões e asfixia em minutos. Conduta: correr imediatamente para o hospital veterinário 24h Pet Guardian com antídotos específicos."
        ),
        "keywords": ["raticida", "veneno de rato", "chumbinho", "veneno", "anticoagulante", "hemorragia interna", "vitamina k", "salivacao intensa"]
    },
    {
        "id": "tox_11",
        "source": "Protocolo de Toxicologia Pet Guardian",
        "category": "toxicology",
        "title": "Intoxicação por Produtos de Limpeza Domésticos (Água Sanitária e Cloro)",
        "content": (
            "Água sanitária, cloro concentrado, desinfetantes com amônia quaternária e soda cáustica são substâncias altamente corrosivas. "
            "A ingestão causa queimaduras cáusticas severas na língua, esôfago e estômago, salivação espumosa e vômitos sanguinolentos. "
            "NUNCA tente induzir o vômito, pois a substância cáustica queima novamente o esôfago na volta. NUNCA ofereça leite ou vinagre caseiro. "
            "Encaminhe o animal imediatamente para suporte médico intensivo e proteção de mucosa na Pet Guardian."
        ),
        "keywords": ["agua sanitaria", "cloro", "desinfetante", "amonia", "produto de limpeza", "queimadura quimica", "corrosivo"]
    },
    {
        "id": "tox_12",
        "source": "Protocolo de Toxicologia Pet Guardian",
        "category": "toxicology",
        "title": "Veto a Medicamentos Humanos, Opioides e Prescrição sem Exame Presencial (Morfina, Tramadol, Paracetamol)",
        "content": (
            "Medicamentos de uso humano, analgésicos opioides (morfina, tramadol), antibióticos e corticoides administrados sem avaliação presencial "
            "são ESTRITAMENTE PROIBIDOS e podem ser FATAIS para pets. A indicação de receitas ou dosagem de morfina injetável e fármacos controlados "
            "em domicílio é expressamente vedada pelo risco iminente de depressão respiratória grave, coma e óbito. "
            "O Paracetamol é ALTAMENTE LETAL para gatos mesmo em doses mínimas (meta-hemoglobinemia e asfixia). "
            "Anti-inflamatórios como Ibuprofeno causam hemorragias digestivas graves. Qualquer alívio de dor ou prescrição exige exame clínico presencial urgente."
        ),
        "keywords": ["morfina", "tramadol", "receita", "dosagem", "prescricao", "injetavel", "opioide", "antibiotico", "corticoide", "paracetamol", "tylenol", "ibuprofeno", "aspirina", "diclofenaco", "remedio humano"]
    },
    {
        "id": "tox_13",
        "source": "Protocolo de Toxicologia Pet Guardian",
        "category": "toxicology",
        "title": "Perigo de Abacate (Toxina Persina) e Carambola (Caramboxina)",
        "content": (
            "O abacate contém a toxina persina nas folhas, casca e polpa, que provoca distúrbios gastrointestinais severos (vômitos e diarreias) "
            "e congestão miocárdica em animais domésticos, além do enorme risco mecânico de asfixia e obstrução intestinal pelo caroço. "
            "A carambola contém caramboxina e altos teores de oxalato, provocando nefrotoxicidade e convulsões em pets com qualquer grau de "
            "comprometimento renal. Ambas as frutas devem ser categoricamente excluídas da dieta pet."
        ),
        "keywords": ["abacate", "persina", "carambola", "caramboxina", "fruta proibida", "caroco de abacate", "obstrucao por caroco"]
    },
    {
        "id": "tox_14",
        "source": "Protocolo de Toxicologia Pet Guardian",
        "category": "toxicology",
        "title": "Perigo Fatal de Bebidas Alcoólicas e Massas de Pão Fermentadas Cruas",
        "content": (
            "Cães e gatos são extremamente sensíveis ao etanol. O álcool presente em cervejas, vinhos, licores e perfumes é rapidamente absorvido, "
            "provocando acidose metabólica severa, depressão do sistema nervoso central, hipotermia, convulsões e parada respiratória. "
            "Além disso, massas cruas de pão ou pizza com fermento biológico vivo continuam a fermentar e crescer no estômago quente do cão, "
            "produzindo etanol e grande quantidade de gás, deflagrando dilatação gástrica aguda e intoxicação alcoólica simultânea."
        ),
        "keywords": ["alcool", "cerveja", "vinho", "massa crua", "massa de pao com fermento", "fermentacao estomacal", "etanol"]
    }
]
