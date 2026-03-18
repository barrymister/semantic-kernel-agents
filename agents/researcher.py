"""
Researcher Agent
-----------------
First agent in the pipeline. Given a topic, gathers key facts,
relevant context, and source material using the search plugin.

Azure AI-103 equivalent: AI Agent with function-calling / tool-use capability.
Semantic Kernel equivalent: KernelFunction with SearchPlugin registered.
"""

import os
from agents.base import BaseAgent, AgentContext
from plugins.search_plugin import SearchPlugin


SYSTEM_PROMPT = """You are a Research Specialist. Your role is to gather accurate,
comprehensive facts about a given topic.

For each research request:
1. Identify the 5–7 most important facts or concepts
2. Note any key statistics, dates, or named entities
3. Identify areas of uncertainty or where expert opinion varies
4. Structure your findings as a numbered list with brief explanations

Be factual, not opinionated. Your output feeds directly into analysis — completeness matters more than prose quality."""


class ResearcherAgent(BaseAgent):
    """
    Researcher Agent — gathers facts and source material via search plugin.

    Semantic Kernel Plugin: SearchPlugin (registered as a kernel function).
    Tool-use pattern: Agent decides when and how to invoke the search tool.
    """

    def __init__(self, model: str = None, system_prompt: str = SYSTEM_PROMPT):
        super().__init__(
            name="Researcher",
            model=model or os.getenv("DEFAULT_MODEL", "gemma3:12b"),
            system_prompt=system_prompt,
        )
        self.search_plugin = SearchPlugin()

    def run(self, context: AgentContext) -> AgentContext:
        """
        Research the topic. Uses search plugin for grounding if available.
        Falls back to model knowledge if search is unavailable.
        """
        print(f"[{self.name}] Researching: {context.topic}")

        # Optionally ground with search results before calling the model
        search_results = self.search_plugin.search(context.topic)

        user_message = f"""Research this topic thoroughly: {context.topic}

{"Background sources found:\n" + search_results if search_results else "Use your knowledge to research this topic."}

Provide a structured list of key facts, statistics, and context."""

        # TODO: Replace with real Semantic Kernel / Ollama call
        # Example SK call:
        # kernel = build_kernel(self.model)
        # result = await kernel.invoke_prompt(user_message, system=self.system_prompt)
        # context.researcher_output = str(result)

        # Placeholder until SK integration is wired
        context.researcher_output = f"[Researcher placeholder — topic: {context.topic}]"
        print(f"[{self.name}] Research complete ({len(context.researcher_output)} chars)")
        return context
