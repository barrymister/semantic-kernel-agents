"""
Critic Agent
-------------
Fourth agent in the pipeline. Reviews the Writer's output for accuracy,
completeness, and quality. Returns either APPROVED or REVISION_NEEDED with feedback.

Azure AI-103 equivalent: Evaluation agent / quality gate in an agentic workflow.
AutoGen equivalent: UserProxyAgent with review function, or AssistantAgent as judge.
"""

import os
from agents.base import BaseAgent, AgentContext


SYSTEM_PROMPT = """You are a Quality Control Reviewer. You evaluate research documents
for accuracy, completeness, and clarity.

Review checklist:
1. Does it accurately reflect the source research?
2. Are key themes and insights present?
3. Is the structure clear and navigable?
4. Is the writing clear for the target audience?
5. Are there factual errors or unsupported claims?

Respond with one of:
- APPROVED: (brief reason why it meets quality bar)
- REVISION_NEEDED: (specific, actionable feedback — what to fix and how)

Be direct. If it's good enough, approve it. Don't request cosmetic changes."""


APPROVAL_SIGNAL = "APPROVED"


class CriticAgent(BaseAgent):
    """
    Critic Agent — reviews document quality and triggers revision if needed.

    Returns context with either final_document set (approved) or
    critic_feedback set (revision needed).
    """

    def __init__(self, model: str = None, system_prompt: str = SYSTEM_PROMPT):
        super().__init__(
            name="Critic",
            model=model or os.getenv("DEFAULT_MODEL", "gemma3:12b"),
            system_prompt=system_prompt,
        )

    def run(self, context: AgentContext) -> AgentContext:
        """
        Review the writer's document. Set final_document if approved,
        set critic_feedback if revision is needed.
        """
        if not context.writer_output:
            raise ValueError("CriticAgent requires writer_output in context")

        print(f"[{self.name}] Reviewing document (revision #{context.revision_count})")

        user_message = f"""Review this document about '{context.topic}':

{context.writer_output}

Is it APPROVED or does it need REVISION_NEEDED?"""

        # TODO: Replace with real SK / Ollama call
        # Placeholder: approve after 1 revision or on first pass
        review_result = APPROVAL_SIGNAL  # Placeholder

        if APPROVAL_SIGNAL in review_result:
            context.final_document = context.writer_output
            context.critic_feedback = None
            print(f"[{self.name}] APPROVED after {context.revision_count} revision(s)")
        else:
            context.critic_feedback = review_result
            context.revision_count += 1
            print(f"[{self.name}] REVISION_NEEDED (round {context.revision_count})")

        return context

    @property
    def approved(self) -> bool:
        """Convenience check — use after run() to decide whether to loop back."""
        return True  # TODO: track last review result
