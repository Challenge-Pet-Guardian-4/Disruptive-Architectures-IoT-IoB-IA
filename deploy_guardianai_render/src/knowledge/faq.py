"""
Base de Conhecimento: Respostas Semânticas para Dúvidas Frequentes Cotidianas
"""

BASE_RESPOSTAS_COTIDIANAS = {
    "pao": {
        "palavras_chave": ["pao", "paes", "pão", "pães", "torrada", "massa"],
        "resposta": (
            "Sim, cães podem comer um pedacinho pequeno de pão simples (como pão francês ou pão de forma tradicional), mas apenas como um agrado muito ocasional.\n\n"
            "Cuidados essenciais que você deve ter:\n"
            "• Baixo valor nutritivo: O pão é rico em carboidratos e calorias, o que pode levar ao ganho de peso e desequilíbrio nutricional se oferecido com frequência.\n"
            "• Sem recheios ou temperos: Nunca ofereça pães que contenham alho, cebola, queijo gorduroso, passas ou adoçante xilitol.\n"
            "• Proibição de massa crua: Massas de pão cruas com fermento biológico são extremamente perigosas, pois o fermento continua crescendo no estômago do pet e libera álcool, causando intoxicação e dilatação gástrica.\n\n"
            "💡 Dica saudável: Se quiser agradar seu pet com petiscos naturais seguros, prefira pedacinhos de cenoura crua ou maçã sem sementes!"
        ),
        "categoria": "nutricao",
        "urgencia": "baixa"
    },
    "arroz": {
        "palavras_chave": ["arroz", "arroz branco", "arroz integral"],
        "resposta": (
            "Sim! O arroz branco ou integral cozido é seguro e muito bem digerido por cães e gatos.\n\n"
            "Como oferecer corretamente:\n"
            "• Sempre cozido apenas em água, estritamente sem sal, óleo, alho ou cebola.\n"
            "• É muito utilizado como suporte em dietas brandas quando o pet está se recuperando de episódios gastrointestinais leves (sempre sob orientação profissional)."
        ),
        "categoria": "nutricao",
        "urgencia": "baixa"
    },
    "ovo": {
        "palavras_chave": ["ovo", "ovos", "ovo cozido", "omelete"],
        "resposta": (
            "Sim! O ovo é uma excelente fonte de proteína de alto valor biológico, aminoácidos essenciais e vitaminas para cães e gatos.\n\n"
            "Recomendações:\n"
            "• Ofereça sempre 100% cozido (cozido ou mexido sem óleo, sal ou temperos).\n"
            "• Evite ovos crus devido ao risco de contaminação por Salmonella e presença de avidina (que reduz a absorção de biotina)."
        ),
        "categoria": "nutricao",
        "urgencia": "baixa"
    },
    "queijo_leite": {
        "palavras_chave": ["leite", "queijo", "iogurte", "laticinio", "laticinios", "requeijao", "manteiga"],
        "resposta": (
            "Com muita cautela! A maioria dos cães e gatos adultos não produz lactase suficiente, tornando-se intolerantes à lactose.\n\n"
            "Pontos de atenção:\n"
            "• Leite de vaca integral e queijos amarelos/gordurosos costumam provocar diarreia, gases e desconforto abdominal.\n"
            "• Se o seu pet não for intolerante, pequenas quantidades de queijo branco magro sem sal (como ricota ou cottage) ou iogurte natural desnatado sem açúcar podem ser oferecidos ocasionalmente."
        ),
        "categoria": "nutricao",
        "urgencia": "baixa"
    },
    "carne_frango": {
        "palavras_chave": ["frango", "carne", "peixe", "bife", "boi", "porco"],
        "resposta": (
            "Sim! Carnes magras (como peito de frango ou carne bovina moída magra) são ótimas fontes de nutrientes.\n\n"
            "Regras de segurança:\n"
            "• Devem ser sempre bem cozidas e preparadas exclusivamente sem sal, cebola, alho ou pimentas.\n"
            "• ⚠️ ATENÇÃO: NUNCA ofereça ossos cozidos (de frango ou costela). O cozimento altera a estrutura do osso, fazendo com que ele se estilhace em pontas agudas capazes de perfurar o esôfago, estômago ou intestinos do animal."
        ),
        "categoria": "nutricao",
        "urgencia": "baixa"
    },
    "frutas_gerais": {
        "palavras_chave": ["fruta", "frutas", "maca", "banana", "melancia", "mamao", "morango", "manga"],
        "resposta": (
            "Muitas frutas são excelentes petiscos hidratantes e nutritivos para cães!\n\n"
            "Frutas seguras e recomendadas:\n"
            "• Maçã: Sempre sem sementes e sem o miolo duro (as sementes contêm vestígios de cianeto).\n"
            "• Banana: Em rodelas moderadas devido ao teor de frutose e potássio.\n"
            "• Melancia e Melão: Em cubos frescos, estritamente sem casca e sem sementes.\n"
            "• Morango e Manga: Sem caroço e sem folhas.\n\n"
            "⛔ PROIBIDAS: Uvas e uvas-passas são tóxicas e causam falência renal aguda."
        ),
        "categoria": "nutricao",
        "urgencia": "baixa"
    },
    "vomito_diarreia": {
        "palavras_chave": ["vomito", "vomitando", "vomitou", "diarreia", "fezes moles", "mole", "desarranjo"],
        "resposta": (
            "Episódios isolados de vômito ou diarreia podem ocorrer por indiscrição alimentar leve, mas exigem atenção redobrada.\n\n"
            "O que você deve fazer:\n"
            "1. Mantenha água limpa e fresca sempre disponível para evitar desidratação.\n"
            "2. Não administre nenhum medicamento humano por conta própria.\n"
            "3. Se houver sangue nas fezes ou vômito, prostração, febre ou se os episódios se repetirem mais de 2 vezes no mesmo dia, leve seu pet imediatamente a um hospital veterinário."
        ),
        "categoria": "saude",
        "urgencia": "media"
    },
    "vacinas_geral": {
        "palavras_chave": ["vacina", "vacinas", "vacinacao", "v8", "v10", "antirrabica", "giardia", "gripe"],
        "resposta": (
            "A vacinação é o pilar mais importante da medicina preventiva para cães e gatos!\n\n"
            "Protocolos essenciais:\n"
            "• Filhotes: Iniciam com 3 a 4 doses de vacina múltipla (V8 ou V10 para cães / V3, V4 ou V5 para gatos) com intervalo de 21 a 28 dias, mais a vacina antirrábica aos 4 meses.\n"
            "• Importante: Filhotes só devem passear na rua ou ter contato com outros animais 15 dias após a conclusão do esquema vacinal.\n"
            "• Adultos e Idosos: Necessitam de reforço anual de todas as vacinas para manter a imunidade ativa."
        ),
        "categoria": "saude",
        "urgencia": "baixa"
    },
    "inducao_vomito": {
        "palavras_chave": ["agua oxigenada", "sal", "fazer vomitar", "induzir vomito", "vomitar logo", "forcar vomito"],
        "resposta": (
            "⛔ NÃO INDUZA O VÔMITO DO SEU PET EM CASA COM ÁGUA OXIGENADA OU SAL!\n\n"
            "Por que receitas caseiras de vômito são perigosas:\n"
            "• Água oxigenada (peróxido de hidrogênio) causa gastrite hemorrágica severa, úlceras e risco de embolia gasosa fatal.\n"
            "• Sal de cozinha em excesso provoca intoxicação por sódio (hipernatremia aguda), edema cerebral e convulsões.\n"
            "• Risco de broncoaspiração: O animal pode aspirar o vômito para os pulmões, gerando pneumonia aspirativa gravíssima.\n\n"
            "🚨 Conduta segura: Leve o pet imediatamente a uma clínica ou hospital veterinário 24h. Apenas a equipe médica possui eméticos seguros injetáveis e suporte intensivo."
        ),
        "categoria": "EMERGENCIA",
        "urgencia": "EMERGENCIA"
    },
    "racao": {
        "palavras_chave": ["racao", "rações", "racoes", "alimentar", "alimentacao", "comida de cachorro", "comida de gato"],
        "resposta": (
            "Para uma alimentação equilibrada e saudável do seu pet, siga estas recomendações essenciais:\n\n"
            "Diretrizes nutricionais:\n"
            "• Escolha rações completas (Premium Especial ou Super Premium) adequadas para a espécie, porte e faixa etária do animal.\n"
            "• Transição gradual: Ao trocar de ração, faça uma transição misturando a ração antiga com a nova ao longo de 7 a 10 dias para evitar desarranjos gastrointestinais.\n"
            "• Quantidade e fracionamento: Siga a tabela do fabricante no verso do pacote ajustada pelo peso e nível de atividade, fracionando em 2 a 3 refeições diárias.\n"
            "• Água limpa: Mantenha sempre água fresca abundante disponível próxima ao comedouro."
        ),
        "categoria": "nutricao",
        "urgencia": "baixa"
    },
    "remedios_humanos": {
        "palavras_chave": ["dipirona", "ibuprofeno", "aspirina", "dorflex", "remedio de gente", "remedio humano"],
        "resposta": (
            "⛔ NUNCA DÊ MEDICAMENTOS HUMANOS PARA CÃES OU GATOS POR CONTA PRÓPRIA!\n\n"
            "Anti-inflamatórios e analgésicos humanos (como Ibuprofeno, Aspirina, Diclofenaco e Paracetamol) possuem metabolismo incompatível com o fígado e rins de pets, podendo causar úlceras gástricas perfuradas, hemorragias e insuficiência renal aguda.\n\n"
            "👉 Qualquer medicação deve ser prescrita exclusivamente por um médico-veterinário com dosagem ajustada por peso e espécie."
        ),
        "categoria": "saude",
        "urgencia": "media"
    }
}
