"""
Analyst Agent
--------------
Second agent in the pipeline. Takes Researcher output and structures
it into a coherent analysis: patterns, gaps, key themes, and implications.

Azure AI-103 equivalent: Chained agent step with structured output.
AutoGen equivalent: AssistantAgent with analysis role.
"""

import os
from agents.base import BaseAgent, AgentContext


SYSTEM_PROMPT = """You are an Analytical Strategist. You receive raw research findings
and transform them into structured analysis.

Your output should include:
1. **Key Themes** — 3–5 overarching patterns in the research
2. **Critical Insights** — the most important non-obvious findings
3. **Knowledge Gaps** — what the research doesn't answer
4. **Implications** — what this means for practitioners

Write for a technical but non-specialist audience. Be direct and specific."""


class AnalystAgent(BaseAgent):
    """
    Analyst Agent — structures research findings into analytical output.
    """

    def __init__(self, model: str = None, system_prompt: str = SYSTEM_PROMPT):
        super().__init__(
            name="Analyst",
            model=model or os.getenv("DEFAULT_MODEL", "gemma3:12b"),
            system_prompt=system_prompt,
        )

    def run(self, context: AgentContext) -> AgentContext:
        """
        Analyze the researcher's output and produce structured analysis.
        """
        if not context.researcher_output:
            raise ValueError("AnalystAgent requires researcher_output in context")

        print(f"[{self.name}] Analyzing research on: {context.topic}")

        user_message = f"""Analyze these research findings about '{context.topic}':

{context.researcher_output}

Produce structured analysis with: key themes, critical insights, knowledge gaps, and implications."""

        # TODO: Replace with real SK / Ollama call
        context.analyst_output = f"[Analyst placeholder — analyzed: {context.topic}]"
        print(f"[{self.name}] Analysis complete ({len(context.analyst_output)} chars)")
        return context
