# Operations Guide — semantic-kernel-agents

How to run the multi-agent pipeline, configure agents, add new agents, and wire real Semantic Kernel calls.

---

## What this project does

A multi-agent research pipeline: four specialized AI agents collaborate to produce a structured document on any topic.

```
Topic → Researcher → Analyst → Writer ←→ Critic (revision loop) → Final document
```

Each agent has a distinct role and system prompt. The Critic can request revisions, sending the pipeline back to the Writer up to `MAX_REVISION_ROUNDS` times.

**Azure AI-103 mapping:** This is a working implementation of the multi-agent orchestration patterns tested on the AI-103 exam. The Orchestrator (`orchestrator/pipeline.py`) maps to **Azure AI Agent Service** orchestration. Each agent maps to an **Azure AI Agent** with a role-specific system prompt.

---

## Prerequisites

- Python 3.11
- Ollama running locally with at least one model pulled:
  ```bash
  ollama pull gemma3:12b       # used by Researcher, Analyst, Critic
  ollama pull mistral-small3.2  # used by Writer (config/agents.yaml)
  ```
- (Optional) Azure AI Search credentials for RAG grounding — see below

```bash
pip install -r requirements.txt
```

---

## Run the pipeline

```bash
python -m orchestrator.pipeline "quantum computing"
```

This runs the full Researcher → Analyst → Writer → Critic pipeline and prints the final document to stdout.

**Options:**

```bash
# Save output to a file
python -m orchestrator.pipeline "machine learning" --output output.md

# Enable Azure AI Search RAG grounding (requires .env credentials)
python -m orchestrator.pipeline "transformer architectures" --rag

# Run with a different topic
python -m orchestrator.pipeline "self-hosted AI infrastructure"
```

**Current state:** The agent LLM calls are stubbed out (see the `TODO` comments in each agent file). The pipeline runs and produces placeholder output. To get real output, wire the Ollama or Semantic Kernel calls — see "Wire real LLM calls" below.

---

## Read `config/agents.yaml`

This file controls every agent's behavior. Edit it without touching Python code.

```yaml
default_model: gemma3:12b
max_revision_rounds: 2          # how many times Critic can request revision

agents:
  researcher:
    model: gemma3:12b           # which Ollama model this agent uses
    temperature: 0.3            # lower = more factual, consistent
  writer:
    model: mistral-small3.2     # use a prose-quality model for writing
    temperature: 0.7            # higher = more varied, creative
  critic:
    temperature: 0.2            # very low = strict, consistent review
    approval_threshold: 0.75    # minimum quality score (0–1)

plugins:
  search:
    backend: none               # options: none, azure
    top_k: 5                    # number of search results to return
```

**Azure AI-103 mapping:** This YAML maps directly to an agent definition in Azure AI Agent Service. The `system_prompt_override` field is equivalent to setting the `instructions` parameter when creating an Azure AI Agent.

---

## Add a new agent

1. Create `agents/summarizer.py` following the pattern in `agents/analyst.py`:
   ```python
   from agents.base import BaseAgent, AgentContext

   class SummarizerAgent(BaseAgent):
       def __init__(self, model=None, system_prompt=SYSTEM_PROMPT):
           super().__init__(name="Summarizer", model=model or "gemma3:12b",
                            system_prompt=system_prompt)

       def run(self, context: AgentContext) -> AgentContext:
           # Add your logic here
           context.summary_output = "[Summarizer output]"
           return context
   ```

2. Register it in `orchestrator/pipeline.py`:
   ```python
   from agents.summarizer import SummarizerAgent
   summarizer = SummarizerAgent()
   # Add to the pipeline sequence after critic approves
   context = summarizer.run(context)
   ```

3. Add configuration to `config/agents.yaml`:
   ```yaml
   agents:
     summarizer:
       model: gemma3:12b
       temperature: 0.4
   ```

---

## Wire real LLM calls (Ollama)

Each agent file has a `TODO` comment showing exactly where to add the real call. Here's how to wire Ollama for the Researcher agent (`agents/researcher.py`):

Replace this:
```python
# TODO: Replace with real Semantic Kernel / Ollama call
context.researcher_output = f"[Researcher placeholder — topic: {context.topic}]"
```

With this (direct Ollama HTTP call — no SDK needed):
```python
import httpx, os

async def _call_ollama(model: str, system: str, user: str) -> str:
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            f"{os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')}/api/chat",
            json={
                "model": model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ]
            }
        )
        return response.json()["message"]["content"]

# In run():
import asyncio
context.researcher_output = asyncio.run(
    _call_ollama(self.model, self.system_prompt, user_message)
)
```

Repeat the same pattern for each agent file.

---

## Wire real Semantic Kernel calls (optional)

To use the official Semantic Kernel SDK instead of direct Ollama:

```python
import semantic_kernel as sk
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion

kernel = sk.Kernel()
kernel.add_service(OllamaChatCompletion(
    ai_model_id=self.model,
    host=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
))

result = await kernel.invoke_prompt(
    user_message,
    kernel_arguments=sk.KernelArguments(settings={"system": self.system_prompt})
)
context.researcher_output = str(result)
```

**Azure AI-103 exam note:** SK's `kernel.invoke_prompt()` is the equivalent of calling an Azure OpenAI chat completion through the Semantic Kernel abstraction layer. The same code works with Azure OpenAI, OpenAI, or Ollama by swapping the service registration.

---

## Optional: Azure AI Search RAG grounding

The `plugins/search_plugin.py` supports Azure AI Search as a document grounding source.

Setup (free tier — no cost):
1. Create an Azure AI Search resource (F0 tier: free, 50MB storage, 3 indexes)
2. Create an index named `research-docs`
3. Add to `.env`:
   ```
   AZURE_SEARCH_ENDPOINT=https://your-service.search.windows.net
   AZURE_SEARCH_KEY=your-key
   AZURE_SEARCH_INDEX=research-docs
   ```
4. Implement `_azure_search()` in `plugins/search_plugin.py` (the TODO is marked)
5. Run with `--rag` flag

**Azure AI-103 exam note:** Azure AI Search as a RAG grounding source is a core AI-103 topic. The F0 tier is sufficient to demonstrate the pattern without cost.

---

## Understand the revision loop

The orchestrator in `orchestrator/pipeline.py` runs this loop:

```python
for round_num in range(MAX_REVISION_ROUNDS + 1):
    context = writer.run(context)    # Writer produces/revises document
    context = critic.run(context)    # Critic reviews

    if context.final_document:
        break                        # Approved — exit loop

    if round_num >= MAX_REVISION_ROUNDS:
        context.final_document = context.writer_output   # Accept anyway
        break
```

When the Critic sets `context.critic_feedback`, the Writer receives it on the next loop iteration and incorporates the feedback. This is the **multi-turn state management** pattern tested on AI-103.

**Azure AI Agent Service equivalent:** An orchestrator calling `agent.run()` in a turn loop, with the agent's `thread` maintaining state across turns.
