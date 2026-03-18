# semantic-kernel-agents

Multi-agent AI system using Microsoft Semantic Kernel and AutoGen. Four specialized agents — Researcher, Analyst, Writer, and Critic — collaborate to produce structured research documents from a single topic prompt.

Runs 100% locally via Ollama. No Azure costs required. Optional Azure AI Search F0 free tier for RAG document grounding.

---

## What it does

```
User prompt: "Research topic X"
        │
        ▼
  Researcher Agent
  (gathers facts, sources, key points via search plugin)
        │
        ▼
  Analyst Agent
  (structures findings, identifies patterns, gaps)
        │
        ▼
  Writer Agent
  (produces formatted document: summary, sections, citations)
        │
        ▼
  Critic Agent
  (reviews for accuracy, completeness, tone — requests revision if needed)
        │
        ▼
  Final document output (markdown)
```

Multi-turn: Critic can send output back to Writer for revision before finalizing.

---

## Azure AI-103 cert alignment

This project covers all exam domains of the Microsoft AI-103: Azure AI App & Agent Developer Associate:

| This project | Azure AI-103 concept | Exam domain |
|---|---|---|
| `agents/researcher.py` | AI Agent with tool-use | Domain 1: Agentic AI fundamentals |
| `plugins/search_plugin.py` | Semantic Kernel Plugin | Domain 1: SK plugin development |
| `orchestrator/pipeline.py` | Multi-agent orchestration | Domain 2: Agent coordination |
| `agents/critic.py` | Agent evaluation + feedback loop | Domain 2: Agent quality patterns |
| `config/agents.yaml` | Agent persona + system prompt design | Domain 3: Prompt engineering |
| Ollama integration | Azure AI Foundry model swap | Domain 4: Model deployment |
| AutoGen GroupChat | AutoGen multi-agent framework | Domain 2: AutoGen patterns |
| Optional RAG path | Azure AI Search grounding | Domain 3: RAG patterns |

---

## Quick start

### Local (Ollama — $0)

**Prerequisites:** Python 3.11, Ollama running locally with `gemma3:12b` or `mistral-small3.2` pulled.

```bash
git clone https://github.com/barrymister/semantic-kernel-agents.git
cd semantic-kernel-agents

pip install -r requirements.txt

cp .env.example .env
# Edit .env: set OLLAMA_BASE_URL (default: http://localhost:11434)

# Run the multi-agent pipeline
python -m orchestrator.pipeline "The impact of containerization on ML deployment workflows"
```

### Optional: Azure AI Search RAG

```bash
# Edit .env: set AZURE_SEARCH_ENDPOINT + AZURE_SEARCH_KEY (free F0 tier)
# Then run with RAG grounding enabled:
python -m orchestrator.pipeline "Your topic" --rag
```

---

## Project structure

```
semantic-kernel-agents/
├── agents/
│   ├── base.py             # BaseAgent abstract class
│   ├── researcher.py       # Gathers facts via search plugin
│   ├── analyst.py          # Structures findings into analysis
│   ├── writer.py           # Produces final formatted document
│   └── critic.py           # Reviews output, requests revision if needed
├── plugins/
│   └── search_plugin.py    # Semantic Kernel native plugin (web/local search)
├── orchestrator/
│   └── pipeline.py         # Multi-agent turn management + AutoGen GroupChat
├── config/
│   └── agents.yaml         # Agent personas, model assignments, system prompts
├── docs/adr/
│   └── 001-semantic-kernel-over-langchain.md
├── requirements.txt
├── .env.example
└── CONTRIBUTING.md
```

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama inference endpoint |
| `DEFAULT_MODEL` | `gemma3:12b` | Model for all agents (override per-agent in agents.yaml) |
| `ANTHROPIC_API_KEY` | *(empty)* | Optional — swap Ollama for Claude API |
| `AZURE_SEARCH_ENDPOINT` | *(empty)* | Azure AI Search endpoint (RAG, optional) |
| `AZURE_SEARCH_KEY` | *(empty)* | Azure AI Search API key (RAG, optional) |
| `AZURE_SEARCH_INDEX` | `research-docs` | Index name for RAG grounding |
| `MAX_REVISION_ROUNDS` | `2` | Max Critic→Writer revision cycles before finalizing |

---

## Agentic AI patterns demonstrated

| Pattern | Implementation |
|---|---|
| Tool-use agents | Researcher uses `search_plugin` — a Semantic Kernel native plugin |
| Multi-agent orchestration | AutoGen GroupChat manages agent turn order + message routing |
| Feedback loops | Critic agent triggers Writer revision via structured message |
| Prompt engineering | System prompts in `config/agents.yaml` — externalized, swappable |
| Provider abstraction | Ollama or Azure OpenAI — same SK `ChatCompletionService` interface |
| RAG grounding | Azure AI Search plugin (optional) retrieves docs before Researcher runs |
| State management | Shared `AgentContext` passed through pipeline for cross-agent memory |

---

## Infrastructure

Development: Local Ollama inference (appfactory: gemma3:12b, mistral-small3.2)
Optional cloud: Azure AI Search F0 free tier (50MB, 3 indexes, no compute cost)

---

## License

MIT — use freely, attribution appreciated.
