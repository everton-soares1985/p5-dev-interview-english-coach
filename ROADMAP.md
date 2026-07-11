# P5 — Dev Interview English Coach
## Escopo Completo & Roadmap de Implementação

> **Documento de continuidade** — escrito pelo Claude Sonnet para garantir que qualquer
> agente (Gemini, Claude, etc.) possa dar sequência ao projeto sem perda de contexto.
> **Data:** 10/07/2026 | **Status:** Phase 2 concluída, Phase 3 em execução.

---

## Estado Atual (Fase 2 — CONCLUÍDA ✅)

### O que funciona hoje
```
python src/main.py --video inputs/entrevista.mkv       ← análise de vídeo real
python src/main.py --transcript examples/fake.txt      ← análise de texto
python src/main.py --dry-run ...                       ← preview sem gravar
pytest tests/ -v                                       ← 20/20 testes passando
```

### Stack validada
- **Modelo:** `gemini-2.5-flash` (multimodal, free tier Google AI Studio)
- **SDK:** `google-genai` (novo SDK — NÃO usar `google-generativeai` que está deprecated)
- **CLI:** argparse + rich
- **Testes:** pytest + pytest-mock (sem chamadas reais de API nos testes)
- **Python:** 3.12.2 | **.venv:** `C:\PROGRAMACAO\PORTFOLIO_PUBLIC\.venv`

### Arquivos de saída atuais (7 relatórios .md por análise)
```
transcript.md
english_feedback.md
corrected_answers.md
improved_interview_answers.md
vocabulary_to_study.md
grammar_patterns.md
next_practice_plan.md
```

### Segurança Git (NUNCA violar)
```
.env                          ← gitignored
inputs/                       ← gitignored
outputs/                      ← gitignored
```

---

## PHASE 3 — GitHub + Visual Polish (PRÓXIMA)

### 3.1 — Melhorar prompts para output visual rico

**Problema identificado:** O Gemini gera texto corrido sem estrutura visual.
**Solução:** Reescrever os dois prompts em `src/prompts/` para forçar saída formatada.

Padrões a exigir em cada arquivo:

```
english_feedback.md  → tabela de dimensões + score ⭐ visual + A2/B1 badge
corrected_answers.md → blocos ❌ Original / ✅ Corrected / 📌 Rule
vocabulary_to_study.md → tabela Markdown obrigatória (Word | Meaning | Example | Level)
grammar_patterns.md  → seções por tipo de erro, antes/depois
next_practice_plan.md → ### Day 1 / Day 2 ... + checklist - [ ]
transcript.md        → **Interviewer:** / **Candidate:** em bold, separadores ---
```

### 3.2 — Score numérico de fluência (0-10)

Adicionar nova seção ao response do Gemini:

```
## FLUENCY_SCORE
Overall: 5.5/10
Clarity: 6/10
Grammar: 4/10
Vocabulary: 5/10
Fluency: 6/10
Confidence: 6/10
```

**Arquivos a modificar:**
- `src/prompts/video_review_prompt.txt` — adicionar instrução de score
- `src/prompts/transcript_review_prompt.txt` — idem
- `src/writer.py` — adicionar `"FLUENCY_SCORE"` em `SECTION_KEYS`
- `tests/test_writer.py` — atualizar fixtures para incluir a nova seção

### 3.3 — examples/fake_output/ (para GitHub demo)

Criar 8 arquivos .md fictícios com visual rico. 
**Candidato fictício:** "Alex Chen, Backend Engineer, entrevista para vaga Python Dev".
Nenhuma referência ao Everton, Wellfound real, ou dados privados.

### 3.4 — README.md (em inglês, para portfólio)

```markdown
# P5 — Dev Interview English Coach
[badges: Python, Gemini AI, License MIT, Tests 20/20]

> AI-powered English coach for technical interviews.
> Upload your OBS recording → get 7 structured Markdown reports.

## Features | Demo Output | Installation | Usage | Privacy | Roadmap
```

Seção Privacy (obrigatória):
> ⚠️ Privacy: Your interview recordings and generated reports are processed locally
> and never committed to this repository. inputs/ and outputs/ are gitignored by default.

### 3.5 — GitHub

```
Repo name: p5-dev-interview-english-coach
Visibility: Public
Conta: mesma conta Lane B (PORTFOLIO_PUBLIC)
Branch: main
```

Checklist antes do push:
- .env NÃO está no repo
- outputs/ NÃO está no repo  
- inputs/ NÃO está no repo
- Nenhum dado real no repo
- examples/ usa APENAS dados fictícios
- .gitignore verificado

---

## PHASE 4 — Funcionalidades Pessoais (SESSÃO FUTURA)

### 4.1 — Modo --compare (PRIORIDADE ALTA — uso pessoal)

```bash
python src/main.py --compare outputs/sessao_01/ outputs/sessao_02/
```

Output: `outputs/compare_[timestamp]/evolution_report.md`

```markdown
## 📈 Evolution Report
Session 1: 2026-07-10 | Score: 4.5/10
Session 2: 2026-07-17 | Score: 6.0/10
Delta: +1.5 points (+33% improvement)

## What improved | What still needs work | Consistency patterns
```

Novos arquivos:
- `src/comparator.py`
- `src/prompts/compare_prompt.txt`
- `tests/test_comparator.py`

**Depende do FLUENCY_SCORE (3.2) estar implementado.**

### 4.2 — Histórico de Sessões

Arquivo local gitignored `session_history.json`:
```json
{
  "sessions": [
    {
      "date": "2026-07-10",
      "source": "video",
      "file": "Entrevista.mkv",
      "output_dir": "outputs/minha_entrevista_wellfound",
      "overall_score": 5.5,
      "scores": { "clarity": 6.0, "grammar": 4.0, "vocabulary": 5.0 }
    }
  ]
}
```

`python src/main.py --history` → tabela Rich com histórico e evolução.

Novos arquivos:
- `src/history.py`
- `tests/test_history.py`

### 4.3 — PDF Export

```bash
python src/main.py --video ... --export-pdf
```

Fluxo: `.md` → HTML → `fpdf2` → `.pdf`
Biblioteca recomendada: `fpdf2>=2.7.0` (sem dependência de GTK no Windows)

Novos arquivos:
- `src/exporter.py`
- `src/templates/report_template.html`

### 4.4 — Antigravity Workflow Integration

Criar skill `.agent/skills/p5-coach/SKILL.md` no workspace:
- Pergunta caminho do vídeo ao usuário
- Roda `python src/main.py --video <path>` via run_command
- Mostra resumo dos outputs gerados
- Opcionalmente roda `--compare` com sessão anterior

---

## Decisões Arquiteturais (NÃO mudar sem revisão)

| Decisão | Motivo |
|:---|:---|
| `google.genai` SDK | Oficial e mantido; `google.generativeai` está deprecated |
| `gemini-2.5-flash` | Free tier, suporta vídeo multimodal, rápido |
| Saída em `.md` | Portável, legível, versionável, sem dependências |
| Parsing por `## SECTION_NAME` | Simples e robusto; falha com placeholder |
| Testes com mock | 1s por run, sem consumir API real |
| `outputs/` gitignored | Privacidade absoluta dos dados reais |
| Limite: 1 GB hard, 300 MB warn | Cobre entrevistas reais de 13-30 min |
| Suporte: .mp4 .mov .mkv .webm .avi | .mkv é o formato padrão do OBS |

---

## Estrutura Final do Projeto

```
p5-dev-interview-english-coach/
├── .env                          ← GITIGNORED — GEMINI_API_KEY
├── .env.example                  ← template público
├── .gitignore
├── requirements.txt
├── SPEC.md
├── ROADMAP.md
├── README.md                     ← [A CRIAR — Phase 3]
│
├── src/
│   ├── __init__.py
│   ├── main.py                   ← CLI (argparse + rich)
│   ├── gemini_client.py          ← Files API + generate_content
│   ├── analyzer.py               ← orquestra análises
│   ├── writer.py                 ← parser + writer .md
│   ├── comparator.py             ← [Phase 4.1]
│   ├── history.py                ← [Phase 4.2]
│   ├── exporter.py               ← [Phase 4.3]
│   └── prompts/
│       ├── video_review_prompt.txt
│       ├── transcript_review_prompt.txt
│       └── compare_prompt.txt    ← [Phase 4.1]
│
├── tests/
│   ├── __init__.py
│   ├── test_writer.py            ← 9 testes ✅
│   ├── test_transcript_mode.py   ← 4 testes ✅
│   ├── test_video_mode.py        ← 7 testes ✅
│   ├── test_comparator.py        ← [Phase 4.1]
│   └── test_history.py           ← [Phase 4.2]
│
├── examples/
│   ├── fake_interview_transcript.txt
│   └── fake_output/              ← [Phase 3.3]
│       ├── transcript.md
│       ├── english_feedback.md
│       ├── corrected_answers.md
│       ├── improved_interview_answers.md
│       ├── vocabulary_to_study.md
│       ├── grammar_patterns.md
│       ├── next_practice_plan.md
│       └── fluency_score.md
│
├── docs/
│   └── screenshot.png            ← [Phase 3]
│
├── inputs/                       ← GITIGNORED
└── outputs/                      ← GITIGNORED
```

---

## Dependências

```
# requirements.txt atual
google-genai>=0.3.0
python-dotenv>=1.0.0
rich>=13.7.0
pytest>=8.0.0
pytest-mock>=3.14.0

# Adições futuras
fpdf2>=2.7.0          ← Phase 4.3 (PDF export)
```

---

## Próximos passos imediatos (Phase 3 — hoje)

```
[ ] Passo 1: Reescrever prompts (visual rico + fluency score)
[ ] Passo 2: Atualizar writer.py + testes para FLUENCY_SCORE
[ ] Passo 3: Criar examples/fake_output/ com 8 .md fictícios e visual rico
[ ] Passo 4: Criar README.md em inglês (portfólio)
[ ] Passo 5: Verificar .gitignore, rodar pytest (20/20)
[ ] Passo 6: git init → git remote add → git push
```
