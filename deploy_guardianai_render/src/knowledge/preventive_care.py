"""
Base de Conhecimento: Matriz Clínica Preventiva por Porte e Idade
"""

BASE_CUIDADOS_PORTE_IDADE = {
    "pequeno": {
        "alerta_clinico": "Propensão natural a acúmulo de tártaro nos dentes e alterações na válvula mitral após a meia-idade.",
        "nutricao": "Metabolismo acelerado, necessitando de grãos menores e maior densidade energética balanceada.",
        "cuidados_gerais": "Escovação dental frequente e acompanhamento cardiológico regular a partir dos 6 anos."
    },
    "medio": {
        "alerta_clinico": "Tendência ao ganho de peso se não mantiver uma rotina diária de passeios e atividades físicas.",
        "nutricao": "Alimentação balanceada com controle calórico e petiscos apenas como agrado moderado.",
        "cuidados_gerais": "Recomenda-se cerca de 40 a 60 minutos de exercícios e enriquecimento ambiental diários."
    },
    "grande": {
        "alerta_clinico": "Maior vulnerabilidade articular (displasia) e risco de dilatação/torção gástrica.",
        "nutricao": "Dietas ricas em protetores articulares (condroitina e glicosamina) e uso de comedouros lentos.",
        "cuidados_gerais": "Evitar exercícios intensos logo antes ou após as refeições para proteger o sistema digestivo."
    }
}

BASE_FAIXA_ETARIA = {
    "filhote": {
        "fase": "Filhote (0 a 12 meses)",
        "protocolo": "Esquema vacinal inicial completo (V8/V10 + Antirrábica) e vermifugação periódica. Passeios externos liberados apenas após a imunização completa.",
        "socializacao": "Fase de ouro para socialização com diferentes estímulos, sons e toques amigáveis."
    },
    "adulto": {
        "fase": "Adulto (1 a 7 anos)",
        "protocolo": "Reforço anual de vacinas, prevenção contínua contra pulgas/carrapatos e exames de rotina anuais.",
        "socializacao": "Manutenção do peso saudável através de rotina ativa e estímulos mentais."
    },
    "senior": {
        "fase": "Sênior / Idoso (7+ anos)",
        "protocolo": "Check-up veterinário semestral com exames laboratoriais (rins, fígado, hemograma) e avaliação cardíaca.",
        "socializacao": "Ambiente confortável com camas macias, tapetes antiderrapantes e caminhadas leves."
    }
}
