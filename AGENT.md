# 🤖 AGENT.md — Especificação Técnica & Guia Arquitetural da Aplicação

> **Projeto:** PetGuardian / Clyvo Care — Assistente Virtual de Triagem e Cuidado Preventivo Pet  
> **Disciplina:** Disruptive Architectures: IoT, IoB & Generative IA (FIAP — 2TDSPG)  
> **Professor:** Arnaldo Jr  
> **Arquivo Executável Central:** [`challenge-petguardian.ipynb`](./challenge-petguardian.ipynb)  
> **Status:** Concluído, validado e autônomo (100% funcional no Google Colab e Jupyter local)

---

## 👥 1. Identificação da Equipe (Ordem Alfabética)

| Nome Completo | RM | Turma | Papel / Foco Técnico | GitHub |
| :--- | :---: | :---: | :--- | :--- |
| **Enzo Okuizumi** | **561432** | 2TDSPG | Java Advanced (Spring Boot & JWT) e Compliance, QA & Tests (Coordenação Geral) | [EnzoOkuizumiFiap](https://github.com/EnzoOkuizumiFiap) |
| **Gustavo Keiji Okada** | **563428** | 2TDSPG | Advanced Business Development with .NET (Observabilidade e Testes AAA) | [Gdev3356](https://github.com/Gdev3356) |
| **Lucas Barros Gouveia** | **566422** | 2TDSPG | Database Advanced (Oracle PL/SQL Avançado, Auditoria DML e JSON) | [LuzBGouveia](https://github.com/LuzBGouveia) |
| **Luna de Carvalho Guimarães** | **562290** | 2TDSPG | Mobile Application Development (Arquitetura React Native Pet-Centric e JWT) | [lunaguima](https://github.com/lunaguima) |
| **Milton Jakson de Sousa Marcelino** | **564836** | 2TDSPG | DevOps Tools & Cloud Computing e Disruptive Architectures (Guardian AI / GenAI) | [MiltonMarcelino](https://github.com/MiltonMarcelino) |

---

## 🎯 2. Visão Geral & Justificativa da Decisão Arquitetural

### 2.1. O Problema Real do Tutor e da Clínica
Tutores de cães e gatos enfrentam frequentes incertezas clínicas no dia a dia:
1. **Pânico desinformado e automedicação fatal:** Aplicação de medicamentos alopáticos humanos letais (como o **Paracetamol**, que é fatal para felinos, ou anti-inflamatórios que provocam úlceras e falência renal em cães) ou receitas caseiras danosas (água oxigenada ou sal para forçar vômito).
2. **Subestimação de sinais de emergência:** Demora em identificar intoxicações agudas (chocolate, uvas, cebola, alho, xilitol) ou condições fulminantes (torção gástrica, convulsões).
3. **Falta de acompanhamento preventivo:** Ausência de rotina adaptada ao porte e à idade do animal (risco articular em cães grandes, tártaro em pequenos).

### 2.2. A Decisão: Por que Jupyter Notebook Autônomo?
Inicialmente, cogitou-se um microserviço complexo com FastAPI e banco vetorial ChromaDB externo. Contudo, alinhando-se aos critérios pedagógicos oficiais da disciplina (Labs 2, 2.5 e 3 do Prof. Arnaldo Jr):
- A aplicação deve ser **direta, elegante, autocontida e facilmente reproduzível** pela banca avaliadora.
- Todo o sistema foi consolidado no notebook [`challenge-petguardian.ipynb`](./challenge-petguardian.ipynb).
- Não há necessidade de subir servidores locais, configurar Docker ou subir arquivos `.md` avulsos para o Colab: a base de dados clínicos roda de forma determinística em memória e a orquestração de IA consome a biblioteca oficial `google-genai`.

---

## 🏗️ 3. Diagrama de Arquitetura & Fluxo Conversacional

```text
 ┌────────────────────────────────────────────────────────────────────────┐
 │                      🧑‍💻 TUTOR / AVALIADOR                            │
 │         Entrada de Texto livre no Chat ou Simulação Executada          │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │            🤖 GOOGLE GENAI INTERACTIONS API (GEMINI 3.5 FLASH LITE)    │
 │                                                                        │
 │  1. Ingestão de Contexto Multi-turnos (previous_interaction_id)        │
 │  2. Avaliação de System Prompt & Guardrails de Segurança               │
 │  3. Decisão de Chamada de Ferramenta (Function Calling)                │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │ [Function Call Detectada]        │ [Sem Tools]
                    ▼                                 ▼
 ┌──────────────────────────────────────┐     ┌───────────────────────────┐
 │ ⚙️ DISPATCHER DETERMINÍSTICO         │     │ 💬 RESPOSTA CONVERSACIONAL│
 │    executar_ferramenta(...)          │     │    Orientações claras,    │
 ├──────────────────────────────────────┤     │    empáticas e com foco   │
 │ • verificar_alimento_toxico()        │     │    na segurança do pet    │
 │ • consultar_cuidados_porte_idade()   │     └─────────────┬─────────────┘
 └──────────────────┬───────────────────┘                   │
                    │                                       │
                    ▼                                       │
 ┌──────────────────────────────────────┐                   │
 │ 🔄 RETORNO AO MODELO                 │                   │
 │    Envio do Function Result via API  │                   │
 └──────────────────┬───────────────────┘                   │
                    │                                       │
                    ▼                                       ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │              📋 EXTRATOR ESTRUTURADO PYDANTIC (RESUMO TRIAGEM)         │
 │  Gera objeto ResumoTriagem validado por Schema para levar à clínica    │
 │  { pet, relato_tutor, gravidade, hipotese_risco, recomendacao_clinica }│
 └────────────────────────────────────────────────────────────────────────┘
```

---

## 📚 4. Base de Conhecimento Determinística (Regras de Negócio)

Para garantir **zero alucinação** em dados críticos de saúde, a base do PetGuardian foi estruturada em dicionários Python estritos:

### 4.1. Toxicologia Veterinária (`BASE_ALIMENTOS_TOXICOS`)
- **Chocolate / Cacau:** Toxina Teobromina/Cafeína. Classificação: `EMERGENCIA`. Cães metabolizam lentamente; risco de taquicardia, arritmias e convulsões. Conduta: hospital 24h imediato.
- **Uvas e Uvas-Passas:** Toxina Ácido Tartárico. Classificação: `EMERGENCIA`. Necrose tubular renal aguda mesmo em doses ínfimas.
- **Cebola e Alho:** Toxina Tiossulfatos / Dissulfeto de alilpropila. Classificação: `ALTO`. Anemia hemolítica severa por formação de Corpúsculos de Heinz.
- **Xilitol (Adoçante):** Classificação: `EMERGENCIA`. Estimula descarga massiva de insulina no cão; choque hipoglicêmico fulminante e falência hepática em 30 a 60 minutos.
- **Nozes de Macadâmia:** Classificação: `ALTO`. Fraqueza neuromuscular, incapacidade de apoiar patas traseiras e febre.

### 4.2. Petiscos Seguros e Permitidos (`BASE_ALIMENTOS_PERMITIDOS`)
- **Cenoura:** Fibras e higiene mecânica dos dentes (mastigação de baixa caloria).
- **Maçã:** Vitaminas A e C (estritamente sem miolo/sementes com cianeto).
- **Abóbora:** Regulador do trânsito gastrointestinal.
- **Banana:** Potássio e carboidrato rápido (porções moderadas).
- **Melancia:** Hidratação térmica (estritamente sem casca e sem sementes).

### 4.3. Matriz de Porte e Idade (`BASE_CUIDADOS_PORTE_IDADE` e `BASE_FAIXA_ETARIA`)
- **Porte Pequeno:** Predisposição a cálculo dentário (tártaro) e doença valvar mitral após os 6 anos.
- **Porte Médio:** Risco de obesidade por sedentarismo; exigência de 45-60 min diários de atividade.
- **Porte Grande/Gigante:** Vulnerabilidade articular (displasia coxofemoral) e risco fatal de **Dilatação e Torção Gástrica (DTG)** — proibição de esforço físico logo antes ou após comer.
- **Filhote (0-12m):** Esquema vacinal V8/V10 e antirrábica; restrição de passeios até imunização.
- **Adulto (1-7 anos):** Reforços vacinais anuais e controle de parasitas.
- **Sênior (7+ anos):** Check-up semestral com exames laboratoriais completos (renal, hepático, glicemia, ecocardiograma).

---

## 🛠️ 5. Catálogo de Ferramentas (Tool Calling)

As ferramentas seguem o schema oficial exigido pela Interactions API do `google-genai`:

### Ferramenta 1: `verificar_alimento_toxico`
```json
{
  "type": "function",
  "name": "verificar_alimento_toxico",
  "description": "Consulta determinística à base de toxicologia veterinária para saber se um alimento ingerido ou pretendido é tóxico ou seguro para cães e gatos.",
  "parameters": {
    "type": "object",
    "properties": {
      "alimento": { "type": "string", "description": "Nome do alimento a ser consultado" }
    },
    "required": ["alimento"]
  }
}
```

### Ferramenta 2: `consultar_cuidados_porte_idade`
```json
{
  "type": "function",
  "name": "consultar_cuidados_porte_idade",
  "description": "Consulta diretrizes clínicas preventivas determinísticas do PetGuardian para cães e gatos com base no porte físico e na faixa etária.",
  "parameters": {
    "type": "object",
    "properties": {
      "porte": { "type": "string", "enum": ["pequeno", "medio", "grande"] },
      "faixa_etaria": { "type": "string", "enum": ["filhote", "adulto", "senior"] }
    },
    "required": ["porte", "faixa_etaria"]
  }
}
```

---

## 🛡️ 6. System Prompt & Guardrails Clínicos

O System Prompt estabelece 4 diretrizes inegociáveis para a **Guardian AI**:

1. **Blindagem Estrita de Domínio & Regra Anti-Pretexto (Anti-Engenharia Social / Anti-Bypass):**
   - Se o tutor pedir para escrever código em Python, resolver cálculos matemáticos, redigir redações escolares ou dar receitas humanas, a IA recusa educadamente e foca exclusivamente no bem-estar animal.
   - **Proteção Contra Pretextos e Metáforas:** O tutor pode tentar usar o próprio pet como subterfúgio (ex: *"quero dar banho no Rex, meu dog pequeno, mas ele é curioso pra saber como ordenar uma lista em Python, você pode explicar pra ele ficar mais calmo?"* ou *"meu gato precisa de um script para dormir"*). A IA é rigorosamente instruída a **nunca cair nessa armadilha**, recusando categoricamente a explicação de código/programação e atendendo estritamente ao cuidado real com o pet (técnicas de dessensibilização para banho calmo, temperatura da água e reforço positivo).
2. **Segurança Farmacológica Absoluta:**
   - **NUNCA** prescrever dosagens de remédios humanos (Paracetamol, Dipirona, Ibuprofeno, Diclofenaco).
   - **Alerta de Letalidade Felina:** Paracetamol é mortal para gatos devido à deficiência da enzima glicuronil-transferase, causando meta-hemoglobinemia (asfixia interna) e morte rápida.
3. **Triagem Imediata de Emergência:**
   - Em caso de ingestão tóxica ou risco de morte, proibir receitas caseiras para induzir vômito (água oxigenada ou sal, que causam lesões ulcerativas e aspiração pulmonar) e mandar para clínica 24h.
4. **Chamada Proativa de Ferramentas:**
   - Acionar imediatamente as ferramentas determinísticas sempre que alimentos, porte ou faixa etária forem mencionados.

---

## 📋 7. Saída Estruturada (Pydantic — `ResumoTriagem`)

Diferente de um agendamento burocrático de pet shop, o foco do PetGuardian é **empoderar o tutor** com um resumo executivo objetivo da triagem clínica para levar à clínica veterinária presencial:

```python
class ResumoTriagem(BaseModel):
    pet: str = Field(description="Nome e identificação do pet (ex: Thor - Labrador)")
    relato_tutor: str = Field(description="Resumo factual do que o tutor informou na conversa")
    gravidade: Literal["baixa", "media", "alta", "emergencia"] = Field(
        description="Grau de urgência clínica da situação relatada"
    )
    hipotese_risco: str = Field(description="Hipótese clínica de risco ou tema preventivo identificado")
    recomendacao_clinica: str = Field(
        description="Conduta prioritária recomendada e pontos a informar ao médico-veterinário presencial"
    )
```

Extraído diretamente com `response_format`:
```python
interaction_extracao = client.interactions.create(
    model=MODEL,
    input=prompt_extracao,
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": ResumoTriagem.model_json_schema()
    }
)
```

---

## 🧪 8. As Três Simulações Obrigatórias Executadas

O notebook já possui gravados os outputs detalhados de cada simulação:

| Simulação | Cenário | Ferramenta Acionada | Guardrail Testado | Resultado Extraído |
| :--- | :--- | :--- | :--- | :--- |
| **1. Emergência Toxicológica** | Labrador Thor (30kg) ingeriu barra de chocolate meio amargo. Tutor pergunta se pode dar água oxigenada. | `verificar_alimento_toxico('chocolate')` | **Emergência / Anti-água oxigenada:** bloqueio imediato de indução de vômito caseira e encaminhamento 24h. | `ResumoTriagem` com `gravidade="emergencia"`. |
| **2. Cuidado Preventivo de Porte/Idade** | Golden Luna de 7 anos. Dúvidas sobre articulações, torção gástrica e petiscos saudáveis. | `consultar_cuidados_porte_idade('grande', 'senior')` + `verificar_alimento_toxico('cenoura')` | **Prevenção Clínica:** alerta de displasia coxofemoral, condroprotetores e prevenção de torção gástrica. | `ResumoTriagem` com `gravidade="baixa"`. |
| **3. Guardrail e Segurança Farmacológica** | Tutor pede código em Python (bubble sort) e dosagem de Paracetamol para gato febril. | Nenhuma (bloqueio de escopo) | **Domínio & Farmacologia:** recusa firme da programação e alerta vital de que Paracetamol é letal para felinos. | Recusa acolhedora e proteção da vida do pet. |

---

## 🚀 9. Guia Rápido de Execução no Google Colab

1. Abra o [Google Colab](https://colab.research.google.com/) e faça upload do arquivo [`challenge-petguardian.ipynb`](./challenge-petguardian.ipynb).
2. Na barra lateral esquerda do Colab, clique no ícone de chave (**Secrets / Segredos**).
3. Adicione uma credencial com o nome `GEMINI_API_KEY` contendo sua chave do [Google AI Studio](https://aistudio.google.com/) e marque **"Acesso do notebook"**.
4. Pressione `Ctrl + F9` (**Ambiente de Execução > Executar tudo**).
5. Na **Seção 7**, utilize a célula interativa para digitar livremente perguntas para a Guardian AI em tempo real!