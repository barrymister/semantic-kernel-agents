"""
Multi-Agent Pipeline Orchestrator
-----------------------------------
Coordinates the Researcher → Analyst → Writer → Critic pipeline.
Handles the revision loop (Critic → Writer) up to MAX_REVISION_ROUNDS.

Azure AI-103 equivalent: Azure AI Agent Service orchestrator, or
AutoGen GroupChat managing agent turn order.

AutoGen pattern: GroupChat with a GroupChatManager routing messages
between agents based on role and output.
"""

import os
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.base import AgentContext
from agents.researcher import ResearcherAgent
from agents.analyst import AnalystAgent
from agents.writer import WriterAgent
from agents.critic import CriticAgent


MAX_REVISION_ROUNDS = int(os.getenv("MAX_REVISION_ROUNDS", "2"))


def run_pipeline(topic: str, rag: bool = False) -> str:
    """
    Run the full multi-agent pipeline for a given topic.

    Pipeline stages:
    1. Researcher: gather facts (with optional RAG grounding)
    2. Analyst: structure findings
    3. Writer: produce document
    4. Critic: review + approve or request revision
    5. [Loop] Writer revision if Critic requested changes

    Args:
        topic: Research topic string
        rag: If True, enable Azure AI Search RAG grounding (requires .env)

    Returns:
        Final approved document as a string
    """
    print("=" * 60)
    print(f"Multi-Agent Pipeline: {topic}")
    print(f"RAG: {'enabled' if rag else 'disabled'}")
    print("=" * 60)

    # Initialize agents
    researcher = ResearcherAgent()
    analyst = AnalystAgent()
    writer = WriterAgent()
    critic = CriticAgent()

    # Initialize shared context
    context = AgentContext(topic=topic)

    # Stage 1: Research
    context = researcher.run(context)

    # Stage 2: Analysis
    context = analyst.run(context)

    # Stage 3: Write + Critic loop
    for round_num in range(MAX_REVISION_ROUNDS + 1):
        context = writer.run(context)
        context = critic.run(context)

        if context.final_document:
            # Approved
            break

        if round_num >= MAX_REVISION_ROUNDS:
            # Max revisions reached — accept current output
            print(f"[Orchestrator] Max revision rounds ({MAX_REVISION_ROUNDS}) reached. Finalizing.")
            context.final_document = context.writer_output
            break

        print(f"[Orchestrator] Revision {round_num + 1} requested. Looping back to Writer.")

    print("=" * 60)
    print(f"Pipeline complete. Document length: {len(context.final_document or '')} chars")
    print("=" * 60)

    return context.final_document or ""


def main():
    parser = argparse.ArgumentParser(description="Run the semantic-kernel-agents pipeline")
    parser.add_argument("topic", help="Research topic")
    parser.add_argument("--rag", action="store_true", help="Enable Azure AI Search RAG grounding")
    parser.add_argument("--output", help="Write output to file instead of stdout")
    args = parser.parse_args()

    result = run_pipeline(args.topic, rag=args.rag)

    if args.output:
        Path(args.output).write_text(result)
        print(f"\nDocument written to {args.output}")
    else:
        print("\n" + "=" * 60)
        print("FINAL DOCUMENT:")
        print("=" * 60)
        print(result)


if __name__ == "__main__":
    main()
