# Contributing

## Development approach

This project uses AI-assisted development. Architecture, design decisions, and agent persona definitions are human-authored. Implementation scaffolding leverages Claude Code for velocity.

Architecture Decision Records (`docs/adr/`) document the reasoning behind key choices — those are the signal for understanding how the system was designed.

## Adding a new agent

1. Create `agents/<name>.py` inheriting from `BaseAgent`
2. Implement `run(context: AgentContext) -> AgentContext`
3. Write a docstring explaining the Azure AI-103 / Semantic Kernel equivalent
4. Register the agent in `orchestrator/pipeline.py`
5. Add configuration block to `config/agents.yaml`

## Adding a new plugin

1. Create `plugins/<name>_plugin.py`
2. Implement a `search()` or equivalent method
3. Add `@kernel_function` decorator when wiring into Semantic Kernel
4. Update `config/agents.yaml` plugin section

## Wiring the real SK calls

The `# TODO: Replace with real SK / Ollama call` comments in each agent mark where the placeholder strings need to be replaced with actual Semantic Kernel + Ollama / Claude API calls. See the SK docs for `ChatCompletionService` with Ollama.

## Cost discipline

- Development runs on local Ollama — zero cost
- Azure AI Search F0 free tier: 50MB, 3 indexes — sufficient for demos
- Never leave Azure AI Search running at paid tier — delete resource group when done
