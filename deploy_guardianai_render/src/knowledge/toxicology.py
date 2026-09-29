"""
Base de Conhecimento: Toxicologia Veterinária Curada
"""

BASE_ALIMENTOS_TOXICOS = {
    "chocolate": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Teobromina e Cafeína",
        "mecanismo": "Metabolização muito lenta pelo fígado de cães e gatos, gerando hiperestimulação neurológica e cardiovascular.",
        "sintomas": "Taquicardia, tremores musculares, vômitos, diarreia, arritmias e convulsões.",
        "conduta_imediata": "Levar imediatamente a um hospital veterinário 24h. Não induzir vômito com água oxigenada ou sal em casa."
    },
    "cacau": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Teobromina concentrada",
        "mecanismo": "Toxicidade extrema equivalente ao chocolate amargo puro.",
        "sintomas": "Convulsões, hipertermia e risco iminente de parada cardiorrespiratória.",
        "conduta_imediata": "Emergência clínica imediata. Levar ao pronto-socorro veterinário 24h."
    },
    "uva": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Ácido tartárico e derivados nefrotóxicos",
        "mecanismo": "Provoca necrose tubular renal aguda mesmo em quantidades mínimas.",
        "sintomas": "Vômitos nas primeiras horas, letargia, dor abdominal e ausência de urina (anúria).",
        "conduta_imediata": "Hospitalização imediata 24h com fluidoterapia intravenosa e monitoramento renal."
    },
    "uva-passa": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Ácido tartárico altamente concentrado",
        "mecanismo": "Potencial nefrotóxico ainda superior ao da uva fresca.",
        "sintomas": "Falência renal rápida, vômitos e apatia profunda.",
        "conduta_imediata": "Hospitalização imediata 24h."
    },
    "cebola": {
        "status": "toxico",
        "nivel_risco": "ALTO",
        "toxina": "Dissulfeto de alilpropila e compostos sulfurados",
        "mecanismo": "Oxidação da hemoglobina e destruição das hemácias (anemia hemolítica severa).",
        "sintomas": "Fraqueza intensa, gengivas pálidas ou azuladas, urina avermelhada/escura e respiração ofegante.",
        "conduta_imediata": "Consulta veterinária urgente para avaliação hematológica."
    },
    "alho": {
        "status": "toxico",
        "nivel_risco": "ALTO",
        "toxina": "Tiossulfatos concentrados",
        "mecanismo": "Destruição oxidativa das hemácias, cerca de 5 vezes mais tóxico que a cebola.",
        "sintomas": "Letargia, salivação, vômitos e mucosas pálidas.",
        "conduta_imediata": "Atendimento veterinário rápido no mesmo dia."
    },
    "xilitol": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Adoçante artificial (presente em chicletes, pastas e doces diet)",
        "mecanismo": "Liberação fulminante de insulina, gerando choque hipoglicêmico severo e necrose hepática aguda.",
        "sintomas": "Desorientação, fraqueza, andar cambaleante, convulsões e colapso em 30 a 60 minutos.",
        "conduta_imediata": "Emergência médica máxima. Correr imediatamente para o pronto-socorro veterinário 24h."
    },
    "macadamia": {
        "status": "toxico",
        "nivel_risco": "ALTO",
        "toxina": "Composto neurotóxico vegetal",
        "mecanismo": "Bloqueio neuromuscular temporário em cães.",
        "sintomas": "Fraqueza nas patas traseiras, febre, tremores e vômito.",
        "conduta_imediata": "Avaliação veterinária presencial."
    },
    "cafe": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Metilxantinas (Cafeína pura)",
        "mecanismo": "Superestimulação do sistema nervoso central e sobrecarga cardíaca aguda.",
        "sintomas": "Agitação extrema, taquicardia, arritmias, tremores e convulsões.",
        "conduta_imediata": "Atendimento veterinário urgente 24h."
    }
}
