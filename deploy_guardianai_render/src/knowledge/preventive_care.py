"""
Base de Conhecimento: Matriz Clínica Preventiva por Porte, Idade e Espécie — Pet Guardian
Catálogo expandido de protocolos pediátricos, adultos, geriátricos e de manejo específico.
"""
from typing import Dict, Any, List

CHUNKS_PREVENTIVE_CARE: List[Dict[str, Any]] = [
    {
        "id": "prev_01",
        "source": "Guia de Cuidados Preventivos Pet Guardian",
        "category": "preventive_care",
        "title": "Protocolo Preventivo para Cães de Pequeno Porte (Saúde Oral, Traqueia e Coração)",
        "content": (
            "Cães de pequeno porte (Poodle, Shih Tzu, Spitz Alemão, Pinscher, Yorkshire, Chihuahua) possuem metabolismo acelerado e maior "
            "expectativa de vida, mas apresentam alta vulnerabilidade odontológica (doença periodontal precoce e acúmulo acelerado de tártaro "
            "com perda dentária e contaminação bacteriana sistêmica), colapso congênito de traqueia e predisposição genética à degeneração da "
            "válvula mitral (sopro cardíaco e tosse seca) a partir dos 6 anos. Diretrizes fundamentais: escovação dental diária com pasta "
            "veterinária sem enxágue, uso exclusivo de peitorais em vez de coleiras de pescoço para proteger a traqueia, avaliação periodontal "
            "anual e ecocardiograma periódico na Pet Guardian a partir dos 6 anos."
        ),
        "keywords": ["pequeno porte", "porte pequeno", "mini", "toy", "tartaro", "dentes", "valvula mitral", "colapso de traqueia", "peitoral", "escovacao"]
    },
    {
        "id": "prev_02",
        "source": "Guia de Cuidados Preventivos Pet Guardian",
        "category": "preventive_care",
        "title": "Protocolo Preventivo para Cães de Médio Porte (Manejo de Peso, Pele e Otites)",
        "content": (
            "Cães de porte médio (Beagle, Cocker Spaniel, Buldogue Francês, Schnauzer, Basset Hound) possuem tendência acentuada ao sobrepeso "
            "e à obesidade quando submetidos a rotinas sedentárias ou excesso de petiscos calóricos, gerando sobrecarga precoce nas articulações "
            "e pâncreas. Além disso, raças de orelhas caídas ou com dobras de pele têm alta prevalência de otites bacterianas/fúngicas e "
            "dermatite atópica. Diretrizes: manter 40 a 60 minutos diários de caminhadas ativas, secagem rigorosa de orelhas após banhos com "
            "limpadores auriculares prescritos, controle rígido de porções de ração na balança e check-up anual na Pet Guardian."
        ),
        "keywords": ["medio porte", "porte medio", "peso", "obesidade", "exercicio", "otite", "orelha", "pele", "dermatite", "caminhada"]
    },
    {
        "id": "prev_03",
        "source": "Guia de Cuidados Preventivos Pet Guardian",
        "category": "preventive_care",
        "title": "Protocolo Preventivo para Cães de Grande e Gigante Porte (Articulações e Torção Gástrica)",
        "content": (
            "Cães de porte grande e gigante (Labrador, Golden Retriever, Pastor Alemão, Rottweiler, Bernese, Dogue Alemão) têm vulnerabilidade "
            "crítica a afecções musculoesqueléticas (displasia coxofemoral e de cotovelo) e à síndrome fatal da Dilatação e Torção Vólvulo-Gástrica "
            "(DVG). Condutas inegociáveis: utilização obrigatória de comedouros lentos, fracionamento da ração em pelo menos 2 a 3 refeições "
            "diárias, repouso absoluto por 60 minutos antes e após as refeições (proibição estrita de brincadeiras, corridas ou agitação) e dietas "
            "suplementadas com condroprotetores (glicosamina, condroitina e ômega-3) para proteção das cartilagens."
        ),
        "keywords": ["grande porte", "porte grande", "gigante", "displasia coxofemoral", "articulacao", "torcao gastrica", "dvg", "comedouro lento", "condroitina"]
    },
    {
        "id": "prev_04",
        "source": "Guia de Cuidados Preventivos Pet Guardian",
        "category": "preventive_care",
        "title": "Protocolo Pediátrico Preventivo para Filhotes (Imunização e Janela de Socialização)",
        "content": (
            "Filhotes de cães e gatos (0 a 12 meses) passam pela janela mais crítica de formação biológica e comportamental. O protocolo "
            "vacinal pediátrico exige 3 a 4 doses de vacina múltipla (V8 ou V10 para cães / V3, V4 ou V5 para gatos) com intervalo de 21 a "
            "28 dias entre aplicações, seguida pela vacina antirrábica aos 4 meses e vacinas contra giárdia e gripe canina. Regra vital de ouro: "
            "o filhote NÃO deve passear na rua, em praças ou manter contato com animais não imunizados até 15 dias após a conclusão da última "
            "dose da vacina múltipla. Vermifugação periódica mensal e alimentação com ração Super Premium Filhotes garantem o desenvolvimento esquelético ideal."
        ),
        "keywords": ["filhote", "bebe", "puppy", "primeiras vacinas", "v8", "v10", "antirrabica", "socializacao", "passeio na rua", "vermifugo", "pediatrico"]
    },
    {
        "id": "prev_05",
        "source": "Guia de Cuidados Preventivos Pet Guardian",
        "category": "preventive_care",
        "title": "Protocolo Preventivo para Cães e Gatos Adultos (Manutenção da Imunidade e Antiparasitários)",
        "content": (
            "A fase adulta (1 a 7 anos) exige vigilância constante para manutenção da imunidade e prevenção de doenças crônicas silenciosas. "
            "Recomenda-se reforço anual rigoroso de todas as vacinas (múltipla, antirrábica e complementares como gripe e giardíase), "
            "controle parasitário ininterrupto com antipulgas, carrapaticidas (prevenção fundamental de erliquiose e babesiose) e vermífugos periódicos, "
            "além da prevenção da dirofilariose (verme do coração) em regiões litorâneas e quentes. A consulta anual na Pet Guardian com exames "
            "de sangue básicos (hemograma, função renal e hepática) assegura diagnóstico precoce de qualquer alteração metabólica."
        ),
        "keywords": ["adulto", "cao adulto", "gato adulto", "reforco vacinal", "antipulgas", "carrapato", "erliquiose", "verme do coracao", "check-up anual"]
    },
    {
        "id": "prev_06",
        "source": "Guia de Cuidados Preventivos Pet Guardian",
        "category": "preventive_care",
        "title": "Protocolo Geriátrico Preventivo para Pets Sênior / Idosos (Check-up Semestral e Conforto)",
        "content": (
            "Cães e gatos a partir de 7 anos entram na fase sênior/geriátrica, demandando cuidados proativos para prevenção e desaceleração "
            "de doenças degenerativas, como doença renal crônica, osteoartrite, insuficiência cardíaca congestiva e disfunção cognitiva canina. "
            "O acompanhamento veterinário na Pet Guardian deve se tornar impreterivelmente semestral, incluindo painel renal completo com SDMA, "
            "creatinina e urinálise, aferição de pressão arterial, ultrassonografia abdominal e avaliação ortopédica. Adaptações de conforto ambiental "
            "são fundamentais: camas ortopédicas macias, tapetes antiderrapantes, rampas de acesso e passeios leves e agradáveis."
        ),
        "keywords": ["senior", "idoso", "geriatrico", "velho", "check-up semestral", "sdma", "rins", "osteoartrite", "artrite", "adaptacoes", "pressao alta"]
    },
    {
        "id": "prev_07",
        "source": "Guia de Cuidados Preventivos Pet Guardian",
        "category": "preventive_care",
        "title": "Protocolo Específico de Saúde Urinária e Hidratação para Felinos (Prevenção de FLUTD)",
        "content": (
            "Gatos descendem de felinos do deserto e possuem baixa sede espontânea, concentrando excessivamente a urina. Isso gera predisposição "
            "crítica à Doença do Trato Urinário Inferior dos Felinos (FLUTD), formação de cálculos vesicais (estruvita e oxalato) e a emergência "
            "médica fatal de obstrução uretral em machos. Medidas preventivas obrigatórias: disponibilizar múltiplas fontes de água corrente limpa, "
            "fornecer alimentação úmida diária (sachês ou patês de boa qualidade), manter a proporção de caixas de areia (número de gatos + 1) "
            "sempre limpas e posicionadas em locais calmos, evitando o estresse que deflagra a cistite idiopática felina."
        ),
        "keywords": ["gato", "felino", "saude urinaria felina", "flutd", "cistite idiopatica", "obstrucao uretral", "beber agua", "fonte de agua", "sache"]
    },
    {
        "id": "prev_08",
        "source": "Guia de Cuidados Preventivos Pet Guardian",
        "category": "preventive_care",
        "title": "Manejo de Enriquecimento Ambiental e Prevenção de Bolas de Pelos em Gatos",
        "content": (
            "Gatos passam até um terço do dia se higienizando, engolindo pelos mortos com a língua espinhada. O acúmulo no estômago forma "
            "tricobezoares (bolas de pelo), provocando vômitos frequentes e até obstrução pilórica ou intestinal mecânica. Além disso, gatos "
            "que vivem em ambientes restritos sem estímulos desenvolvem obesidade e estresse crônico. Diretrizes: escovação regular da pelagem, "
            "oferecimento de graminha para gatos e pastas de malte lubrificantes, e enriquecimento ambiental com arranhadores verticais, prateleiras "
            "altas e brinquedos que simulem a caça."
        ),
        "keywords": ["bola de pelo", "tricobezoar", "escovacao de gato", "arranhador", "enriquecimento ambiental", "estresse felino", "pasta de malte"]
    }
]
