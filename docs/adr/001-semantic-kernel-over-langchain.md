# ADR 001: Use Semantic Kernel Over LangChain

**Status:** Accepted
**Date:** 2026-03-18

## Context

This project is a portfolio piece targeting Microsoft AI-103 certification and job applications at AI-focused companies (Scale AI, Anduril). The core choice is which agentic AI framework to build on:

- **LangChain** — the most widely used Python framework for LLM applications
- **Semantic Kernel (SK)** — Microsoft's open-source framework, used by Azure AI Foundry and Azure AI Agent Service
- **AutoGen** — Microsoft's multi-agent conversation framework

## Decision

Use **Semantic Kernel** as the primary framework with **AutoGen** for multi-agent orchestration. LangChain is not used.

## Reasoning

**Cert alignment:**
- Microsoft AI-103 tests SK plugin development, SK agent patterns, and Azure AI Agent Service
- SK is the native framework for Azure AI Foundry and Azure AI App Service
- LangChain knowledge has zero exam relevance for AI-103

**Portfolio alignment:**
- Hiring at Scale AI, Anduril, and Palantir focuses on production agentic AI systems
- Azure AI Agent Service (SK-native) is increasingly the enterprise deployment target
- SK + AutoGen is the Microsoft-endorsed stack for multi-agent systems

**Technical fit:**
- SK's plugin interface maps cleanly to function-calling patterns tested in AI-103
- AutoGen's GroupChat is a natural fit for Researcher/Analyst/Writer/Critic turn management
- SK supports Ollama as a `ChatCompletionService` — no Azure OpenAI cost during development

**Provider abstraction:**
- SK's `IChatCompletionService` interface supports Ollama (local), Azure OpenAI, and Anthropic
- Swap providers by changing one config value — the agent code doesn't change
- This directly maps to Azure AI Foundry's model catalog swap pattern tested on exam

## Consequences

**Good:**
- Direct cert exam alignment — every pattern in this codebase appears on the AI-103 exam
- Ollama + SK = zero cost local development, identical API to Azure OpenAI
- SK plugin pattern is reusable across enterprise Azure AI workloads

**Bad:**
- Smaller community and fewer Stack Overflow answers than LangChain
- SK 1.x Python SDK is newer and has fewer examples than the C# SDK
- AutoGen API changed significantly between 0.2 and 0.4 — pinned to 0.2.x for stability

## Alternatives considered

**LangChain:** Rejected — no AI-103 exam relevance, different agent patterns, already overcrowded in portfolios.

**Pure AutoGen (no SK):** Rejected — AutoGen handles orchestration well but SK provides the plugin/function-calling pattern that AI-103 tests directly.

**Bare Ollama + httpx:** Rejected — bypasses the framework patterns the cert tests; code would be harder to explain in interviews.
