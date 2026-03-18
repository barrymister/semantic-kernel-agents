"""
BaseAgent — abstract base class for all agents in the pipeline.

Each agent:
- Has a name and role description
- Receives an AgentContext (shared state across agents)
- Returns an updated AgentContext with its output appended

Azure AI-103 equivalent: Azure AI Agent Service agent definition.
Semantic Kernel equivalent: IChatCompletionService-backed agent with system prompt.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AgentContext:
    """
    Shared state passed between agents in the pipeline.
    Accumulates outputs from each stage.

    Azure equivalent: Agent session state / conversation history.
    """
    topic: str
    researcher_output: Optional[str] = None
    analyst_output: Optional[str] = None
    writer_output: Optional[str] = None
    critic_feedback: Optional[str] = None
    final_document: Optional[str] = None
    revision_count: int = 0
    metadata: dict = field(default_factory=dict)


class BaseAgent(ABC):
    """
    Abstract base class for all pipeline agents.

    Subclasses implement `run()` to process the context and return an updated version.
    """

    def __init__(self, name: str, model: str, system_prompt: str):
        self.name = name
        self.model = model
        self.system_prompt = system_prompt

    @abstractmethod
    def run(self, context: AgentContext) -> AgentContext:
        """
        Execute this agent's task against the shared context.

        Args:
            context: Shared pipeline state from previous agents

        Returns:
            Updated context with this agent's output set
        """
        ...

    def _format_user_message(self, context: AgentContext) -> str:
        """Build the user message for this agent from context. Override in subclasses."""
        return f"Topic: {context.topic}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, model={self.model!r})"
