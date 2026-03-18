"""
Writer Agent
-------------
Third agent in the pipeline. Takes Analyst output and produces a
well-structured, readable document: title, executive summary, sections, conclusion.

Azure AI-103 equivalent: Content generation agent with structured output format.
AutoGen equivalent: AssistantAgent with writer persona.
"""

import os
from agents.base import BaseAgent, AgentContext


SYSTEM_PROMPT = """You are a Technical Writer. You transform analysis into clear,
well-structured documents that technical practitioners can act on.

Document format:
# [Title]

## Executive Summary
(2–3 sentences: what this is about and why it matters)

## Key Findings
(3–5 bullet points from the analysis)

## Detailed Analysis
(Organized prose covering themes and insights)

## Implications for Practice
(Concrete takeaways)

## Conclusion
(Brief close)

Write clearly. Avoid jargon unless necessary. Aim for 400–600 words."""


class WriterAgent(BaseAgent):
    """
    Writer Agent — produces the final formatted document from analysis.
    Can receive revision requests from the Critic agent.
    """

    def __init__(self, model: str = None, system_prompt: str = SYSTEM_PROMPT):
        super().__init__(
            name="Writer",
            model=model or os.getenv("DEFAULT_MODEL", "gemma3:12b"),
            system_prompt=system_prompt,
        )

    def run(self, context: AgentContext) -> AgentContext:
        """
        Write the document. If critic_feedback is set, incorporate revisions.
        """
        if not context.analyst_output:
            raise ValueError("WriterAgent requires analyst_output in context")

        is_revision = context.critic_feedback is not None
        print(f"[{self.name}] {'Revising' if is_revision else 'Writing'} document on: {context.topic}")

        if is_revision:
            user_message = f"""Revise the document based on critic feedback.

Original document:
{context.writer_output}

Critic feedback:
{context.critic_feedback}

Produce an improved version addressing all feedback points."""
        else:
            user_message = f"""Write a structured document about '{context.topic}' based on this analysis:

{context.analyst_output}

Follow the document format from your instructions."""

        # TODO: Replace with real SK / Ollama call
        context.writer_output = f"[Writer placeholder — {'revision' if is_revision else 'draft'} for: {context.topic}]"
        print(f"[{self.name}] Document {'revised' if is_revision else 'written'} ({len(context.writer_output)} chars)")
        return context
