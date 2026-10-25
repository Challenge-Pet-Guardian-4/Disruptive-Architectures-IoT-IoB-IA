"""
Base de Conhecimento: Reprodução, Castração, Gestação e Cuidados Neonatais — Pet Guardian
"""
from typing import Dict, Any, List

_SOURCE = "Guia de Reprodução e Castração Pet Guardian"

CHUNKS_REPRODUCTION: List[Dict[str, Any]] = [
    {
        "id": "rep_01",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "reproduction",
        "title": "Castração: Benefícios, Idade Indicada e Pós-Operatório",
        "content": (
            "A castração previne ninhadas indesejadas, reduz o risco de tumores mamários e testiculares, elimina a piometra nas fêmeas e diminui comportamentos como fuga, marcação de território e brigas. "
            "A idade ideal varia com espécie, raça e porte (em geral a partir de cerca de 6 meses; cães de grande porte podem se beneficiar de aguardar mais para o fechamento das articulações), "
            "e deve ser definida em consulta com exame pré-operatório. No pós-operatório: use colar elizabetano ou roupa cirúrgica, restrinja corridas e pulos por cerca de 10 a 14 dias, "
            "limpe a ferida conforme orientado, administre apenas medicamentos prescritos e retorne para avaliação dos pontos. Procure atendimento se houver sangramento, secreção com mau cheiro, "
            "apatia intensa ou pontos abertos."
        ),
        "keywords": ["castracao", "castrar", "castrado", "castrar cachorro", "castrar gata", "idade para castrar", "pos operatorio", "colar elizabetano", "cirurgia", "esterilizacao", "pontos"]
    },
    {
        "id": "rep_02",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "reproduction",
        "title": "Cio em Cadelas e Gatas: Sinais, Duração e Riscos dos Anticoncepcionais",
        "content": (
            "As cadelas costumam entrar no cio (estro) cerca de duas vezes por ano, com sangramento vulvar, aumento da vulva e atração de machos, durando aproximadamente 3 semanas. "
            "As gatas são poliéstricas sazonais: no cio miam alto, rolam no chão, adotam postura de elevação da região traseira e podem ficar férteis repetidamente. "
            "Durante o período fértil, mantenha a fêmea longe de machos inteiros e passeie com guia curta. Anticoncepcionais hormonais NÃO são recomendados, "
            "pois aumentam o risco de tumores mamários e infecções uterinas (piometra); a castração é o método seguro e definitivo. Converse com o veterinário sobre o momento ideal."
        ),
        "keywords": ["cio", "cadela no cio", "gata no cio", "estro", "sangramento vulvar", "cruzar", "anticoncepcional", "injecao para cio", "miando alto", "fertil", "cruzamento"]
    },
    {
        "id": "rep_03",
        "source": _SOURCE,
        "urgency": "EMERGENCIA",
        "category": "reproduction",
        "title": "Piometra: Infecção Uterina Grave em Fêmeas Não Castradas (Emergência)",
        "content": (
            "A piometra é uma infecção do útero que ocorre principalmente em cadelas e gatas não castradas, geralmente algumas semanas após o cio, e pode causar sepse e morte. "
            "Sinais: secreção vaginal de pus ou sangue com mau cheiro (pode não haver secreção na forma 'fechada'), apatia, perda de apetite, sede e urina excessivas, vômitos, febre e barriga aumentada. "
            "É uma EMERGÊNCIA cirúrgica: o tratamento padrão é a remoção do útero e dos ovários (ovariohisterectomia), associada a antibióticos e suporte intensivo. "
            "Não aguarde melhora espontânea e não medique em casa. A castração preventiva elimina o risco."
        ),
        "keywords": ["piometra", "infeccao no utero", "secrecao vaginal", "pus", "cadela apatica", "femea nao castrada", "sede excessiva", "barriga inchada femea", "utero", "emergencia cirurgica"]
    },
    {
        "id": "rep_04",
        "source": _SOURCE,
        "urgency": "moderada",
        "category": "reproduction",
        "title": "Gestação e Parto em Cadelas e Gatas: Cuidados e Sinais de Complicação (Distocia)",
        "content": (
            "A gestação dura cerca de 9 semanas (aproximadamente 63 dias). Realize pré-natal com ultrassom, ofereça ração de alta qualidade (para filhotes) nos terços finais, mantenha vermifugação e vacinas conforme orientação "
            "e prepare uma caixa de parto aquecida e tranquila. Sinais de distocia (parto complicado) que exigem ATENDIMENTO VETERINÁRIO IMEDIATO: contrações fortes por mais de 30 a 60 minutos sem nascimento, "
            "mais de 2 a 4 horas entre filhotes, secreção verde-escura antes do primeiro filhote, sangramento abundante, febre, prostração ou fêmea tentando sem sucesso. "
            "Não administre medicamentos para induzir o parto sem prescrição."
        ),
        "keywords": ["gestacao", "prenhez", "gravida", "cadela gravida", "gata gravida", "parto", "distocia", "trabalho de parto", "contracao", "ninhada", "pre natal", "filhotes nascendo"]
    },
    {
        "id": "rep_05",
        "source": _SOURCE,
        "urgency": "alta",
        "category": "reproduction",
        "title": "Cuidados Neonatais, Filhotes Órfãos e Desmame",
        "content": (
            "Recém-nascidos não regulam bem a temperatura: mantenha-os aquecidos (cerca de 30 a 32 °C na primeira semana) e longe de correntes de ar. Devem mamar com frequência e ganhar peso diariamente. "
            "Filhotes órfãos ou rejeitados precisam de leite substituto específico para a espécie (NUNCA leite de vaca puro), mamadeira ou seringa em posição correta (barriga para baixo), "
            "e estímulo manual para urinar e defecar após as mamadas; procure o veterinário imediatamente. O desmame ocorre gradualmente entre 4 e 8 semanas, com papinha de ração própria para filhotes. "
            "Sinais de alerta: choro constante, frio ao toque, barriga dura, recusa de mamada ou perda de peso."
        ),
        "keywords": ["recem nascido", "filhote orfao", "mamadeira", "leite para filhote", "desmame", "filhote nao mama", "neonatal", "leite de vaca", "aquecimento filhote", "filhote abandonado"]
    },
]
