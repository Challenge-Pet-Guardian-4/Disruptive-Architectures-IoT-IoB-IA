"""
Base de Conhecimento: Estilo de Vida, Viagem, Posse Responsável e Legislação — Pet Guardian
"""
from typing import Dict, Any, List

_SOURCE = "Guia de Viagem e Posse Responsável Pet Guardian"

CHUNKS_LIFESTYLE: List[Dict[str, Any]] = [
    {
        "id": "life_01",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "lifestyle",
        "title": "Viagem de Carro com Cães e Gatos: Segurança e Perigo do Veículo Fechado",
        "content": (
            "Transporte o animal preso: caixa de transporte fixada ou cinto de segurança específico para pets; animais soltos viram projéteis em freadas e distraem o motorista. "
            "Ofereça uma refeição leve algumas horas antes da viagem para reduzir enjoo, faça paradas a cada 2 horas para água e necessidades e mantenha o ambiente ventilado. "
            "NUNCA deixe o pet sozinho dentro do carro, nem com as janelas entreabertas: em poucos minutos a temperatura interna sobe e causa hipertermia (golpe de calor) fatal, "
            "principalmente em raças braquicefálicas. Leve água, comida, medicamentos, documentos e uma manta com o cheiro dele."
        ),
        "keywords": ["viagem de carro", "viajar com cachorro", "viajar com gato", "caixa de transporte", "cinto de seguranca pet", "enjoo", "deixar no carro", "carro fechado", "estrada", "enjoo no carro"]
    },
    {
        "id": "life_02",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "lifestyle",
        "title": "Viagem de Avião, Ônibus e Hospedagem Pet Friendly: Documentos e Regras",
        "content": (
            "As regras para transportar animais em aviões, ônibus e hotéis variam conforme a companhia e o destino, por isso consulte a empresa com antecedência. "
            "Em geral são solicitados: caixa de transporte com tamanho e ventilação adequados, atestado de saúde emitido por médico-veterinário, carteira de vacinação com antirrábica em dia e, em viagens internacionais, "
            "exigências adicionais do país de destino (certificados e exames, que podem levar meses). Raças braquicefálicas (Pug, Buldogue, Persa) costumam ter restrições para voo em porão devido ao risco respiratório. "
            "Acostume o animal à caixa antes da viagem e converse com o veterinário sobre o uso de qualquer calmante: nunca medique por conta própria."
        ),
        "keywords": ["viagem de aviao", "avião", "aviao com pet", "onibus", "hotel pet friendly", "atestado de saude", "carteira de vacinacao", "viagem internacional", "companhia aerea", "caixa iata", "braquicefalico voo"]
    },
    {
        "id": "life_03",
        "source": _SOURCE,
        "urgency": "alta",
        "category": "lifestyle",
        "title": "Maus-Tratos e Abandono de Animais: Crime Previsto em Lei (Lei 9.605/98 e Lei 14.064/2020)",
        "content": (
            "No Brasil, abusar, maltratar, ferir, mutilar ou abandonar animais é crime previsto no artigo 32 da Lei de Crimes Ambientais (Lei 9.605/98). "
            "A Lei 14.064/2020 (Lei Sansão) aumentou a punição quando a vítima é cão ou gato: reclusão de 2 a 5 anos, multa e proibição de guarda. "
            "Constituem maus-tratos, entre outros, manter o animal sem água, alimento, abrigo, atendimento veterinário, acorrentado de forma permanente ou em local sem higiene. "
            "Denúncias podem ser feitas à polícia (190), à delegacia, a órgãos ambientais ou de proteção animal do município. Se não puder mais cuidar do pet, procure adoção responsável em vez de abandoná-lo."
        ),
        "keywords": ["maus tratos", "abandono", "abandonar", "lei sansao", "crime", "denuncia", "lei 9605", "lei 14064", "acorrentado", "protecao animal", "direito dos animais", "adocao responsavel"]
    },
    {
        "id": "life_04",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "lifestyle",
        "title": "Posse Responsável: Identificação, Vacinação, Planejamento e Custos",
        "content": (
            "Ter um pet é um compromisso de 10 a 20 anos. A posse responsável inclui: identificação (plaquinha na coleira e/ou microchip com cadastro atualizado), vacinação e vermifugação em dia, "
            "castração, passeios com guia e recolhimento das fezes, ambiente seguro (telas em janelas e sacadas para gatos) e acompanhamento veterinário regular. "
            "Planeje os custos mensais e a reserva para emergências: ração de qualidade, antiparasitários, banho e tosa, consultas, vacinas e eventuais cirurgias. "
            "Considere um plano de saúde pet ou uma reserva financeira, e defina quem cuidará do animal em viagens ou imprevistos."
        ),
        "keywords": ["posse responsavel", "microchip", "plaquinha", "identificacao", "custos de um pet", "gasto mensal", "plano de saude pet", "tela de protecao", "telar janela", "ter um pet", "compromisso"]
    },
    {
        "id": "life_05",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "lifestyle",
        "title": "Adoção e Escolha do Primeiro Pet: Porte, Rotina e Check-up Inicial",
        "content": (
            "Antes de adotar, avalie espaço, tempo disponível, orçamento, presença de crianças, alergias na família e o nível de energia da raça ou do animal; adotar um animal adulto com temperamento conhecido "
            "costuma ser mais previsível que um filhote. Nos primeiros dias, leve o pet ao veterinário para exame clínico, atualização de vacinas e vermífugo, teste de FIV/FeLV em gatos e orientação nutricional, "
            "mantendo-o isolado de outros animais da casa até a liberação. Prepare previamente comedouro, bebedouro, cama, coleira com identificação, brinquedos e, para gatos, caixa de areia e arranhador."
        ),
        "keywords": ["adotar", "adocao", "primeiro pet", "escolher raca", "adotar cachorro", "adotar gato", "vira lata", "srd", "check-up inicial", "filhote ou adulto", "fiv felv", "teste de fiv"]
    },
    {
        "id": "life_06",
        "source": _SOURCE,
        "urgency": "baixa",
        "category": "lifestyle",
        "title": "Pets e Crianças: Convivência Segura e Prevenção de Mordidas",
        "content": (
            "Crianças e animais devem conviver sempre sob supervisão de um adulto, pois a maioria das mordidas ocorre com animais conhecidos da família. "
            "Ensine a criança a não puxar orelhas ou rabo, não abraçar apertado, não incomodar o pet enquanto come, dorme ou está no seu cantinho, e a respeitar sinais de desconforto (afastar-se, rosnar, orelhas para trás). "
            "Ofereça ao animal um local de refúgio seguro. Mantenha vacinas (antirrábica) e vermifugação em dia e lave as mãos após o contato. "
            "Em caso de mordida, lave a ferida com água e sabão por vários minutos e procure atendimento médico; notifique a vigilância sanitária local conforme orientação."
        ),
        "keywords": ["crianca", "criancas", "bebe e cachorro", "mordida crianca", "convivencia", "supervisao", "pet e crianca", "mordeu a crianca", "antirrabica", "gestante e gato", "toxoplasmose"]
    },
    {
        "id": "life_07",
        "source": _SOURCE,
        "urgency": "alta",
        "category": "lifestyle",
        "title": "Kit de Primeiros Socorros Pet e Plano de Emergência",
        "content": (
            "Mantenha em casa um kit com: gaze e ataduras, fita adesiva hipoalergênica, soro fisiológico, termômetro digital, tesoura de ponta arredondada, pinça, luvas, seringa sem agulha, cobertor térmico, "
            "focinheira ou tira de tecido (animais com dor podem morder) e a lista de contatos. Anote o telefone e o endereço do hospital veterinário 24h mais próximo e de um centro de controle de intoxicações. "
            "Temperatura normal de cães e gatos: cerca de 38 a 39,2 °C. Em emergências, mantenha a calma, estabilize o animal e leve-o rapidamente ao atendimento. "
            "O kit NÃO substitui o veterinário e não deve incluir medicamentos humanos como paracetamol, dipirona ou ibuprofeno."
        ),
        "keywords": ["kit de primeiros socorros", "primeiros socorros", "emergencia", "hospital 24h", "temperatura normal", "febre cachorro", "termometro", "caixa de remedios", "plano de emergencia", "ataduras"]
    },
]
