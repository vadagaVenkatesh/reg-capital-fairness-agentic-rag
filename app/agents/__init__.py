"""Agents package for Regulatory Capital Fairness Agentic RAG System.

This package contains specialized agents for different domains:
- Orchestrator: Routes queries to appropriate specialist agents
- RegulatoryAgent: SR 11-7, Basel, model risk management
- CapitalAgent: CECL, RWA, capital calculations
- FairnessAgent: Fair lending, ECOA compliance
- OpsAgent: Data quality, model drift monitoring
"""

from app.agents.orchestrator import Orchestrator
from app.agents.regulatory_agent import RegulatoryAgent
from app.agents.capital_agent import CapitalAgent
from app.agents.fairness_agent import FairnessAgent
from app.agents.ops_agent import OpsAgent

__all__ = [
    "Orchestrator",
    "RegulatoryAgent",
    "CapitalAgent",
    "FairnessAgent",
    "OpsAgent",
]

__version__ = "0.1.0"
