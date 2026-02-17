"""Agents package for Regulatory Capital Fairness Agentic RAG System.

This package contains specialized agents for different domains:
- Orchestrator: Routes queries to appropriate specialist agents
- RegulatoryAgent: SR 11-7, Basel, model risk management
- CapitalAgent: CECL, RWA, capital calculations (placeholder)
- FairnessAgent: Fair lending, ECOA compliance (placeholder)
- OpsAgent: Data quality, model drift monitoring (placeholder)
"""

from app.agents.orchestrator import Orchestrator
from app.agents.regulatory_agent import RegulatoryAgent

__all__ = [
    "Orchestrator",
    "RegulatoryAgent",
]

__version__ = "0.1.0"
