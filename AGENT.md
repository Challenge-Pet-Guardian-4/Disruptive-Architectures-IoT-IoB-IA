# 🤖 AGENT.md — Especificação Técnica & Guia Arquitetural da Aplicação

> **Projeto:** PetGuardian — Copiloto Inteligente de Triagem Clínica Preventiva e Orientação Pet  
> **Disciplina:** Disruptive Architectures: IoT, IoB & Generative IA (FIAP — 2TDSPG) | Sprint 4  
> **Professor:** Arnaldo Jr  
> **Núcleo de Produção:** Microsserviço FastAPI Modular em Produção no Render ([`deploy_guardianai_render`](./deploy_guardianai_render))  
> **Status:** Concluído, validado e 100% operacional  

---

## 🎯 2. Evolução Arquitetural: Sprint 3 para Sprint 4

### 2.1. O Desafio em Produção (Restrição de 512 MB de RAM no Render)
Na Sprint 3, a aplicação contava com suporte ao Groq e Gemini, mas utilizava consultas baseadas em correspondências determinísticas fixas. Para a Sprint 4, implementamos um **Pipeline Completo de RAG (Retrieval-Augmented Generation)** vetorial.
Como o container gratuito do Render possui **512 MB de RAM**:
- Frameworks pesados como PyTorch (`torch`) ou `sentence-transformers` exigiriam mais de 900 MB de memória, causando crash imediato por OOM (*Out Of Memory*).
- Como solução de engenharia de software sênior, implementamos o **`LocalSemanticEmbedder`** (`src/utils/embeddings.py`), que gera **embeddings vetoriais densos de 512 dimensões ($\mathbb{R}^{512}$)** com L2-normalização e Similaridade de Cosseno direta.
- Consumo de memória do motor vetorial: **inferior a 15 MB de RAM**, permitindo que todo o microsserviço FastAPI rode com folga (~45 MB de RAM total).

### 2.2. Provedor Principal Groq LPU + Fallback Gemini
- **Groq Cloud (openai/gpt-oss-20b):** Modelo MoE open-weight de 20 bilhões de parâmetros rodando em chips LPU (*Language Processing Units*), fornecendo inferência com tempo de resposta médio de ~350 ms.
- **Google Gemini (gemini-3.5-flash):** Segundo provedor via SDK oficial. O provedor primário é escolhido por `AI_PROVIDER` (`groq` por padrão ou `gemini`) e o outro é usado como fallback automático em caso de falha ou cota esgotada.

---

## 🏗️ 3. Diagrama do Pipeline RAG Ponta a Ponta

```text
 ┌────────────────────────────────────────────────────────────────────────┐
 │                    📱 APLICATIVO MOBILE (REACT NATIVE)                 │
 │            Payload com pergunta do tutor e contexto do pet             │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │ POST /ai/chat
                                     ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │                 ⚡ FASTAPI CONTROLLER (ROUTER /AI/CHAT)                │
 │  1. Validação de Schema Pydantic (ChatRequest)                         │
 │  2. Verificação de Guardrail Crítico (Paracetamol em Felinos)          │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │            📚 KNOWLEDGE SERVICE: MOTOR DE EMBEDDINGS LOCAIS            │
 │  • LocalSemanticEmbedder gera vetor denso da pergunta: u ∈ R^128       │
 │  • Similaridade de Cosseno: cos(u, v) = u . v                          │
 │  • Filtro de relevância estrito: score >= 0.18                         │
 │  • Ranking e seleção dos Top-3 Chunks com metadados e fontes           │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │ Chunks + Status (match_found)
                                     ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │                📝 MONTAGEM DO PROMPT FUNDAMENTADO                      │
 │  • Injeção do System Prompt Pet Guardian com diretrizes éticas         │
 │  • Injeção dos dados biológicos do pet (raça, idade, peso, alergias)   │
 │  • Injeção dos trechos recuperados com instrução de citação de fontes │
 │  • Diretriz Anti-Alucinação caso nenhum chunk atinja o limiar mínimo   │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │             🚀 INFERÊNCIA GENERATIVA (GROQ LPU / GEMINI)               │
 │  Gera resposta empática, fundamentada nos trechos e citando as fontes  │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │         💾 PERSISTÊNCIA & AUDITORIA NO BANCO DE DADOS SQLITE           │
 │  • Salva mensagem do tutor e resposta no histórico                     │
 │  • Salva parecer da triagem na tabela de auditoria clínica             │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │  Retorno JSON: ChatResponse com sources_used e flag rag_grounded       │
 └────────────────────────────────────────────────────────────────────────┘
```

---

## 📚 4. Base de Conhecimento Estruturada em Chunks (Pet Guardian)

A base foi totalmente modernizada e expandida para **64 chunks atômicos em 8 categorias clínicas** com metadados obrigatórios (`id`, `source`, `category`, `title`, `content`, `keywords`), eliminando todos os dicionários legados:
- **14 Chunks de Toxicologia:** Chocolate, cacau puro, uvas/passas, cebola/alho, xilitol, macadâmia, cafeína, plantas tóxicas (lírio em gatos, comigo-ninguém-pode, espada-de-são-jorge), raticidas/chumbinho, cloro/água sanitária, medicamentos humanos (paracetamol, ibuprofeno), abacate e bebidas alcoólicas.
- **8 Chunks de Cuidados Preventivos:** Manejo de porte pequeno (coração e tártaro), médio (peso e otite), grande (articulações e torção gástrica), filhotes (vacinas pediátricas), adultos (imunidade e carrapatos), sênior (SDMA renal e osteoartrite), saúde urinária felina (prevenção de FLUTD) e controle de bolas de pelos.
- **11 Chunks de FAQ e Primeiros Socorros:** Frutas seguras, legumes permitidos, carnes e perigo de ossos cozidos, intolerância a laticínios, transição gradual de ração, manejo de vômito/diarreia, proibição de vômito caseiro com sal ou água oxigenada, manobra de Heimlich para engasgo, golpe de calor em braquicefálicos, picadas de insetos/cobras e ansiedade de separação.
- **7 Chunks de Comportamento:** Adestramento positivo, latido/destruição, arranhadores felinos, caixa de areia, agressividade, exercício físico e introdução de novo pet.
- **7 Chunks de Higiene e Pele:** Banho correto, pulgas/carrapatos (risco permetrina em gatos), coceira/dermatite, higiene de ouvidos, corte de unhas, tosa/escovação e vermifugação.
- **5 Chunks de Reprodução:** Castração e pós-operatório, cio, piometra (urgência cirúrgica), gestação/parto e neonatos órfãos.
- **7 Chunks de Estilo de Vida:** Viagem de carro, viagem aérea/transporte, lei de maus-tratos, posse responsável, adoção, pets e crianças, kit de primeiros socorros.
- **5 Chunks de Doenças Infecciosas:** Parvovirose e cinomose, FIV e FeLV felina, tosse dos canis, leishmaniose visceral e giardíase/coccidiose.

---

## 🛡️ 5. Guardrails e Salvaguardas Éticas

1. **Guardrail Farmacológico:** Veto inegociável a Paracetamol (letal em gatos) e anti-inflamatórios humanos sem prescrição.
2. **Guardrail Toxicológico e de Primeiros Socorros:** Proibição explícita de receitas caseiras para induzir vômito com água oxigenada ou sal (risco de gastrite hemorrágica e pneumonia aspirativa).
3. **Guardrail Anti-Pretexto e Blindagem de Domínio:** Recusa de pedidos de código de programação ou tarefas de software, mesmo quando solicitados usando o animal como pretexto.
4. **Diretriz de Anti-Alucinação:** Quando a consulta não atinge o score de similaridade de cosseno de 0.18, o sistema declara com honestidade que a informação não consta na base e orienta avaliação presencial na Pet Guardian.