# Exercises — semantic-kernel-agents

Hands-on exercises mapped to Microsoft AI-103: Azure AI App & Agent Developer Associate exam domains.

These exercises reference real code in the repo. Work through them while reading the source files.

---

## Exercise 1 — Agent Design and Single vs Multi-Turn

**Cert domain:** Design AI agents (~25%)

Open `agents/researcher.py`.

**Questions to answer:**

1. The Researcher agent has a `SYSTEM_PROMPT` constant at the top of the file. In **Azure AI Agent Service**, what is the equivalent of a system prompt — what parameter do you set when creating an agent? Name the API call.

2. Is the Researcher a **single-turn** or **multi-turn** agent? A single-turn agent handles one request and returns. A multi-turn agent maintains conversation history across multiple calls. Look at `ResearcherAgent.run()` — does it keep any conversation history? What would need to change to make it multi-turn?

3. The Researcher's `SYSTEM_PROMPT` instructs it to "Identify the 5–7 most important facts." In Azure AI Agent Service, the system prompt is called the agent's `instructions`. Write an `instructions` string (2–4 sentences) for an Azure AI Agent that would be equivalent to this Researcher agent.

4. In Azure AI-103, **agent grounding** is a key concept. What is the difference between:
   - Grounding via **Azure AI Search** (RAG)
   - Grounding via **Bing search** (tool-use)
   - Grounding via **file upload** (document context)
   Which type does `SearchPlugin.search()` use when `backend = "azure"`?

---

## Exercise 2 — Implement AI Agents: Data Flow Trace

**Cert domain:** Implement AI agents (~30%)

Open `orchestrator/pipeline.py` and `agents/analyst.py`.

**Questions to answer:**

1. Trace the data flow from `researcher.run(context)` to `analyst.run(context)`. What Python object carries data between agents? What attribute does the Analyst read from the Researcher's output? What would happen if the Researcher produced an empty string?

2. The `AgentContext` dataclass (in `agents/base.py`) is the shared state object. In **Azure AI Agent Service**, what is the equivalent of a shared state object between agents? What is a **Thread** in Azure AI Agent Service and how does it relate to AgentContext?

3. The Analyst agent's `run()` method raises `ValueError` if `context.researcher_output` is None. In a production Azure AI workflow, what is the more robust way to handle this — what Azure AI service feature would you use to validate agent outputs before passing them downstream?

4. The `MAX_REVISION_ROUNDS` variable limits how many times the Critic can send the pipeline back to the Writer. In AutoGen's `GroupChat`, what is the equivalent setting? What happens in AutoGen if max rounds are reached with no consensus?

---

## Exercise 3 — AI Applications: Plugins and Tool Use

**Cert domain:** Build AI applications (~25%)

Open `plugins/search_plugin.py`.

**Questions to answer:**

1. A **Semantic Kernel plugin** is a class that exposes functions for the kernel to call. In the real SK SDK, functions are decorated with `@kernel_function`. What does this decorator do — how does SK discover and invoke plugin functions? (This is tested on AI-103.)

2. How does a Semantic Kernel plugin differ from a plain Python function call? Specifically: who decides *when* to call the plugin — the developer's code or the LLM? Name the SK feature that enables the LLM to autonomously decide when to call a plugin function.

3. In **Azure AI Foundry** (the new platform replacing parts of Azure AI Studio), what is the equivalent of a Semantic Kernel plugin? Name the Azure AI Foundry concept that maps to "a function the agent can call."

4. The `SearchPlugin._detect_mode()` method checks for `AZURE_SEARCH_ENDPOINT` and `AZURE_SEARCH_KEY`. In a production Azure deployment, storing API keys in environment variables is acceptable but not ideal. What Azure service provides managed identity authentication so the app never handles the key? What is this feature called in Azure AI Search?

---

## Exercise 4 — Responsible AI: Critic and Content Safety

**Cert domain:** Responsible AI (~20%)

Open `agents/critic.py`.

**Questions to answer:**

1. The Critic agent reviews documents for: accuracy, completeness, clarity, and factual errors. In **Azure Content Safety**, what categories does the service detect? (Name the four main harm categories.) How does this differ from what the Critic agent checks?

2. The Critic responds with `APPROVED` or `REVISION_NEEDED`. In Azure AI Agent Service, what is the equivalent of a quality gate in an agentic workflow? Name the **evaluation** feature in Azure AI Foundry that can assess agent outputs against defined criteria.

3. The Critic's `temperature` is set to `0.2` in `config/agents.yaml`. Why does a quality-checking agent want a very low temperature? What happens to consistency and reliability as temperature increases toward 1.0?

4. The `APPROVAL_SIGNAL = "APPROVED"` constant is how the orchestrator detects the Critic's decision — it checks if this string appears in the review output. This is a brittle pattern. In a production system, name two more robust alternatives:
   - One using **structured output** (JSON schema enforcement)
   - One using **Azure AI Evaluation** metrics

---

## Exercise 5 — Multi-Agent Orchestration: SK vs AutoGen

**Cert domain:** Design AI agents (~25%) | Implement AI agents (~30%)

**No code to open — answer from memory, then verify with the tech stack reference doc.**

**Questions to answer:**

1. **Semantic Kernel Agent Framework** and **AutoGen** both support multi-agent systems. Explain the key difference in how they handle agent coordination:
   - SK Agent Framework: orchestration is ___-driven (developer writes the routing logic)
   - AutoGen GroupChat: orchestration is ___-driven (an LLM decides who speaks next)
   Which model does `orchestrator/pipeline.py` follow?

2. In AutoGen, a `UserProxyAgent` can represent a human in the loop. What is the equivalent in this project — which agent plays the "approval gate" role that a human would play in a fully manual workflow?

3. The AI-103 exam tests **Microsoft Foundry** (the new platform, 2026). What is the relationship between:
   - Microsoft Foundry
   - Azure AI Studio
   - Azure AI Agent Service
   - Semantic Kernel
   Which one is the orchestration SDK? Which one is the cloud platform? Which one is being retired/replaced?

4. The AI-103 exam scenario: "You are building a customer service bot that can research a customer's issue, draft a response, and get human approval before sending. Which Azure AI components would you use and how would they connect?" Write a 3–4 sentence answer describing the architecture using Azure AI Agent Service, Semantic Kernel, and Azure AI Search.
