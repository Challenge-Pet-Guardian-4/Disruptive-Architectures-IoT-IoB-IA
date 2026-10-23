"""
Base de Conhecimento: Dúvidas Frequentes, Nutrição, Primeiros Socorros e Comportamento — Pet Guardian
Catálogo expandido de orientações cotidianas, condutas seguras e primeiros socorros.
"""
from typing import Dict, Any, List

CHUNKS_FAQ: List[Dict[str, Any]] = [
    {
        "id": "faq_01",
        "source": "FAQ Oficial Pet Guardian",
        "category": "faq",
        "title": "Frutas Seguras e Permitidas para Cães (Petiscos Naturais)",
        "content": (
            "Muitas frutas são excelentes petiscos hidratantes, ricos em fibras e vitaminas para cães, desde que oferecidas com moderação. "
            "Frutas seguras recomendadas: Maçã e Pera (estritamente sem o miolo duro e sem sementes, que contêm glicosídeos cianogênicos tóxicos), "
            "Banana (em rodelas moderadas devido ao teor de carboidratos e potássio), Melancia e Melão (frescos em cubos, estritamente sem casca "
            "e sem sementes), Mamão (em cubos sem sementes, ótimo para motilidade intestinal) e Manga ou Morango (higienizados e sem caroço). "
            "FRUTAS PROIBIDAS: Uvas e passas (falência renal aguda), abacate (toxina persina) e carambola (caramboxina neurotóxica)."
        ),
        "keywords": ["frutas permitidas", "fruta segura", "maca", "banana", "melancia", "melao", "mamao", "morango", "manga", "petisco natural"]
    },
    {
        "id": "faq_02",
        "source": "FAQ Oficial Pet Guardian",
        "category": "faq",
        "title": "Legumes e Vegetais Seguros para Cães (Enriquecimento Nutricional)",
        "content": (
            "Legumes são excelentes opções de baixa caloria para enriquecimento alimentar e saciedade de cães em controle de peso. "
            "Vegetais seguros: Cenoura (crua para mastigação mecânica e limpeza dental, ou cozida), Abóbora cozida (rica em fibras que regulam "
            "tanto fezes amolecidas quanto constipação), Chuchu e Abobrinha cozidos em água (altamente hidratantes e leves) e Batata-doce ou "
            "Batata comum (SEMPRE bem cozidas em água pura; batatas cruas contêm solanina, um alcaloide tóxico). Regra de ouro: preparar sempre "
            "sem adição de sal, óleo, cebola, alho ou caldos industrializados."
        ),
        "keywords": ["legumes", "vegetais", "cenoura", "abobora", "chuchu", "abobrinha", "batata doce", "legume cozido", "baixa caloria"]
    },
    {
        "id": "faq_03",
        "source": "FAQ Oficial Pet Guardian",
        "category": "faq",
        "title": "Proteínas Seguras (Frango, Carnes e Ovos) e o Perigo Fatal de Ossos Cozidos",
        "content": (
            "Carnes magras cozidas (peito de frango, carne bovina moída sem gordura e peixe sem espinhas) e ovos 100% cozidos são excelentes fontes "
            "proteicas de alto valor biológico para cães e gatos em dietas caseiras prescritas ou agrados. Devem ser preparados exclusivamente em "
            "água, sem sal, cebola ou alho. ALERTA GRAVÍSSIMO: JAMAIS ofereça ossos cozidos (ossos de frango, costela ou churrasco). O cozimento altera "
            "a estrutura do colágeno ósseo, tornando o osso quebradiço e lascado em pontas agulhadas que perfuram o esôfago, estômago e intestinos, "
            "provocando peritonite séptica e hemorragias fatais que demandam cirurgia de emergência na Pet Guardian."
        ),
        "keywords": ["frango cozido", "carne cozida", "ovo cozido", "osso cozido", "osso de galinha", "perfuracao intestinal", "churrasco"]
    },
    {
        "id": "faq_04",
        "source": "FAQ Oficial Pet Guardian",
        "category": "faq",
        "title": "Pão, Massas e Laticínios (Intolerância à Lactose e Carboidratos)",
        "content": (
            "Pães simples e assados (como pão francês tradicional ou de forma) podem ser oferecidos apenas em pedacinhos minúsculos e de forma "
            "muito ocasional, pois possuem calorias vazias que predispõem à obesidade e diabetes. NUNCA ofereça massa crua com fermento biológico. "
            "Quanto a leite e queijos: a grande maioria dos cães e gatos adultos não produz a enzima lactase após o desmame, tornando-se intolerantes "
            "à lactose. O consumo de leite de vaca integral ou queijos gordurosos provoca cólicas abdominais, gases e diarreia osmótica severa. "
            "Pequenas porções de queijo branco magro sem sal (ricota/cottage) ou iogurte natural desnatado sem açúcar podem ser tolerados esporadicamente."
        ),
        "keywords": ["pao", "pao frances", "torrada", "massa", "leite", "lactose", "queijo", "iogurte", "diarreia por leite", "intolerancia a lactose"]
    },
    {
        "id": "faq_05",
        "source": "FAQ Oficial Pet Guardian",
        "category": "faq",
        "title": "Diretrizes de Nutrição: Escolha e Transição Gradual de Ração",
        "content": (
            "Para assegurar o aporte ideal de nutrientes, opte por rações completas (Premium Especial ou Super Premium) adequadas para a espécie, "
            "faixa etária e porte do animal. Diretriz de ouro na troca de ração: NUNCA troque a marca ou tipo de ração abruptamente. A microbiota "
            "intestinal necessita de 7 a 10 dias para adaptação: dias 1 a 3 (75% antiga + 25% nova), dias 4 a 6 (50% antiga + 50% nova) e dias "
            "7 a 9 (25% antiga + 75% nova), passando para 100% no décimo dia. Isso previne gastrites, vômitos e diarreias de transição. "
            "Fracione a porção diária indicada na tabela do fabricante em 2 a 3 refeições."
        ),
        "keywords": ["racao", "troca de racao", "transicao gradual", "super premium", "alimentacao", "comida de cachorro", "comida de gato"]
    },
    {
        "id": "faq_06",
        "source": "FAQ Oficial Pet Guardian",
        "category": "faq",
        "title": "Manejo Inicial de Sintomas Gastrointestinais (Vômitos e Diarreia)",
        "content": (
            "Episódios isolados de vômito ou fezes amolecidas podem decorrer de indiscreções alimentares leves, mas exigem vigilância redobrada. "
            "Conduta inicial: manter água limpa e fresca sempre disponível para prevenir a desidratação rápida. NUNCA administre medicamentos humanos "
            "para dor, febre ou vômito (como Paracetamol, Dipirona ou Ibuprofeno). SINAIS DE ALERTA DE EMERGÊNCIA: presença de sangue vivo ou escuro "
            "(borra de café) nas fezes ou vômito, prostração intensa, febre, vômitos repetidos mais de 2 vezes no mesmo dia ou abdômen rígido e doloroso. "
            "Nesses casos, leve o pet imediatamente ao pronto-socorro 24h Pet Guardian."
        ),
        "keywords": ["vomito", "diarreia", "fezes moles", "sangue nas fezes", "desidratacao", "gastrite", "indiscrecao alimentar", "prostracao"]
    },
    {
        "id": "faq_07",
        "source": "FAQ Oficial Pet Guardian",
        "category": "faq",
        "title": "Proibição Vital de Indução Caseira de Vômito com Água Oxigenada ou Sal",
        "content": (
            "É TERMINANTEMENTE PROIBIDO tentar induzir o vômito do animal em casa utilizando água oxigenada (peróxido de hidrogênio) ou sal de cozinha. "
            "A água oxigenada causa gastrite ulcerativa hemorrágica profunda, necrose do epitélio esofágico e risco de embolia gasosa fatal na circulação. "
            "O sal de cozinha provoca hipernatremia aguda fulminante (intoxicação por sódio), edema cerebral e convulsões. Além disso, há o perigo agudo "
            "de broncoaspiração do vômito cáustico para os pulmões, gerando pneumonia aspirativa de altíssima mortalidade. "
            "Conduta correta: em qualquer suspeita de ingestão tóxica, leve o pet imediatamente à Pet Guardian para lavagem gástrica segura com equipe médica."
        ),
        "keywords": ["induzir vomito", "agua oxigenada", "sal", "fazer vomitar", "forcar vomito", "peroxido de hidrogenio", "vomito caseiro", "sal de cozinha"]
    },
    {
        "id": "faq_08",
        "source": "FAQ Oficial Pet Guardian",
        "category": "faq",
        "title": "Primeiros Socorros para Engasgo e Obstrução de Vias Aéreas (Manobra de Heimlich)",
        "content": (
            "Se o animal engasgar com brinquedos, pedras ou ossos, apresentando angústia respiratória, salivação excessiva, patas na boca e mucosas "
            "roxas/azuladas (cianose): 1. Abra a boca com cuidado puxando a língua para a frente; se o objeto estiver visível e acessível na garganta, "
            "retire-o com os dedos ou pinça sem empurrá-lo para o fundo. 2. Se o objeto não sair e o animal perder o ar, realize a Manobra de Heimlich: "
            "para cães médios e grandes em pé, abrace o abdômen do animal por trás, posicione as mãos fechadas logo abaixo da última costela e aplique "
            "pressões rápidas e firmes para cima e para a frente (em direção ao peito). Para cães pequenos e gatos, aplique compressões suaves no tórax. "
            "Corra imediatamente para a emergência veterinária Pet Guardian."
        ),
        "keywords": ["engasgo", "engasgado", "manobra de heimlich", "objeto na garganta", "sufocamento", "asfixia", "cianose", "primeiros socorros engasgo"]
    },
    {
        "id": "faq_09",
        "source": "FAQ Oficial Pet Guardian",
        "category": "faq",
        "title": "Insolação, Golpe de Calor e Hipertermia (Atenção a Cães Braquicefálicos)",
        "content": (
            "Cães não transpiram pela pele, regulando a temperatura quase exclusivamente pela respiração ofegante. Em dias quentes, ambientes fechados "
            "ou carros (nunca deixe um pet no carro!), o animal pode sofrer Golpe de Calor (intermação), elevando a temperatura corporal acima de 40.5°C. "
            "Cães braquicefálicos (focinho curto como Buldogue, Pug, Shih Tzu, Boston Terrier) têm alto risco fatal. Sintomas: respiração extremamente rápida, "
            "salivação grossa, gengivas vermelho-escuras, fraqueza, andar cambaleante e colapso. Primeiros socorros: retire do sol imediatamente, molhe o corpo "
            "com água fresca em temperatura ambiente (NUNCA água gelada ou gelo, que causa choque térmico e vasoconstrição) e leve voando à Pet Guardian."
        ),
        "keywords": ["insolacao", "golpe de calor", "intermacao", "calor", "braquicefalico", "pug", "bulldog", "hipertermia", "ofegante"]
    },
    {
        "id": "faq_10",
        "source": "FAQ Oficial Pet Guardian",
        "category": "faq",
        "title": "Picadas de Insetos, Aranhas, Abelhas e Cobras (Reações Anafiláticas)",
        "content": (
            "Picadas de abelhas, vespas, formigas ou contato com lagartas podem provocar desde inchaço local até choque anafilático severo. "
            "Se o pet foi picado e apresentar inchaço rápido no focinho, ao redor dos olhos ou no pescoço (edema facial/angioedema), vômitos, "
            "urticária ou dificuldade respiratória (roncos e asfixia por edema de glote), trata-se de EMERGÊNCIA MÉDICA. NUNCA aplique remédios humanos "
            "como antialérgicos ou corticoides sem cálculo de dosagem por peso. No caso de picada de cobra ou aranha, mantenha o animal o mais calmo "
            "e imóvel possível e transporte imediatamente para aplicação de soro antiofídico na emergência Pet Guardian."
        ),
        "keywords": ["picada de abelha", "picada de inseto", "picada de cobra", "aranha", "edema facial", "focinho inchado", "alergia picada", "choque anafilatico"]
    },
    {
        "id": "faq_11",
        "source": "FAQ Oficial Pet Guardian",
        "category": "faq",
        "title": "Manejo Comportamental: Ansiedade de Separação e Medo de Trovões/Fogos",
        "content": (
            "O medo de barulhos altos (fogos de artifício, tempestades) e a ansiedade de separação (quando o tutor sai de casa) geram pânico, "
            "destruição de portas, latidos incessantes e tentativas de fuga com risco de atropelamento. Medidas de bem-estar: 1. Crie um 'refúgio seguro' "
            "em cômodo interno com janelas e cortinas fechadas, cama confortável, peça de roupa com o cheiro do tutor e som ambiente com ruído branco "
            "ou música suave. 2. Nunca puna o animal por medo; acolha-o com tranquilidade sem supervalorizar o desespero. 3. Para ansiedade crônica, "
            "utilize brinquedos de enriquecimento ambiental que liberem comida aos poucos (Kongs recheados congelados) e consulte os veterinários "
            "comportamentalistas da Pet Guardian para terapias de dessensibilização e suporte nutracêutico seguro."
        ),
        "keywords": ["ansiedade de separacao", "medo de fogos", "trovao", "barulho alto", "estresse pet", "latido", "comportamento", "enriquecimento"]
    }
]
