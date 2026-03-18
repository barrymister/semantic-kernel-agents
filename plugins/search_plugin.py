"""
Search Plugin — Semantic Kernel Native Plugin
----------------------------------------------
Provides web/document search capability to the Researcher agent.

Semantic Kernel equivalent: A KernelFunction decorated with @kernel_function.
Azure AI-103 equivalent: Plugin registered with an AI Agent for tool-use.

Two modes:
- Local: searches a local document store (no external API needed)
- Azure AI Search: queries an Azure AI Search index (RAG grounding)
"""

import os
from typing import Optional


class SearchPlugin:
    """
    Search plugin for the Researcher agent.

    Registers as a Semantic Kernel native plugin.
    Falls back to returning empty string if no search backend is configured.
    """

    def __init__(self):
        self.azure_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT", "")
        self.azure_key = os.getenv("AZURE_SEARCH_KEY", "")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX", "research-docs")
        self._mode = self._detect_mode()

    def _detect_mode(self) -> str:
        if self.azure_endpoint and self.azure_key:
            return "azure"
        return "none"

    def search(self, query: str, top_k: int = 5) -> str:
        """
        Search for relevant documents given a query.

        Semantic Kernel: decorated with @kernel_function for agent tool-use.

        Args:
            query: Search query string
            top_k: Number of results to return

        Returns:
            Formatted search results as a string, or empty string if unavailable
        """
        if self._mode == "azure":
            return self._azure_search(query, top_k)
        return ""

    def _azure_search(self, query: str, top_k: int) -> str:
        """
        Query Azure AI Search index.
        Azure AI-103: Azure AI Search as a RAG grounding source.

        TODO: Implement with azure-search-documents SDK
        Example:
            from azure.search.documents import SearchClient
            from azure.core.credentials import AzureKeyCredential
            client = SearchClient(self.azure_endpoint, self.index_name,
                                  AzureKeyCredential(self.azure_key))
            results = client.search(query, top=top_k)
            return "\n".join([r["content"] for r in results])
        """
        return f"[Azure AI Search placeholder — index: {self.index_name}, query: {query}]"
