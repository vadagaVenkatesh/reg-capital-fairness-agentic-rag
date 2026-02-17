"""Orchestrator Agent - LangGraph Supervisor for Regulatory Capital Fairness System.

This module implements the supervisor/orchestrator node that routes queries to
appropriate specialist agents based on the domain classification.
"""
import logging
from typing import Annotated, Literal, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import tools_condition
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import yaml

logger = logging.getLogger(__name__)

# Load configuration
with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)


class AgentState(TypedDict):
    """State schema for the agentic workflow."""
    messages: Annotated[list, "The conversation messages"]
    next: str
    query: str
    domain: str
    context: dict
    answer: str


class Orchestrator:
    """Orchestrator/Supervisor agent that routes to specialist agents."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=config["llm"]["model"],
            temperature=config["llm"]["temperature"],
            max_tokens=config["llm"]["max_tokens"]
        )
        self.agents = config["agents"]
        self.graph = self._build_graph()
    
    def _classify_domain(self, state: AgentState) -> AgentState:
        """Classify query into one of the specialist domains."""
        query = state["query"]
        
        system_prompt = f"""You are a domain classifier for a bank risk management system.
        
        Available domains:
        - REGULATORY: SR 11-7, Basel, model risk management, regulatory guidance
        - CAPITAL: CECL, RWA, capital calculations, stress testing
        - FAIRNESS: Fair lending, ECOA, disparate impact analysis
        - OPS: Data quality, model drift, operational resilience
        
        Classify the following query into ONE domain. Respond with only the domain name.
        
        Query: {query}
        """
        
        messages = [SystemMessage(content=system_prompt)]
        response = self.llm.invoke(messages)
        domain = response.content.strip().upper()
        
        # Validate domain
        valid_domains = ["REGULATORY", "CAPITAL", "FAIRNESS", "OPS"]
        if domain not in valid_domains:
            domain = "REGULATORY"  # Default fallback
        
        state["domain"] = domain
        state["next"] = domain.lower()
        logger.info(f"Query classified as domain: {domain}")
        
        return state
    
    def _route_to_agent(self, state: AgentState) -> str:
        """Route to the appropriate specialist agent based on domain."""
        domain = state.get("domain", "REGULATORY").lower()
        logger.info(f"Routing to {domain} agent")
        return domain
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("orchestrator", self._classify_domain)
        workflow.add_node("regulatory", self._call_regulatory_agent)
        workflow.add_node("capital", self._call_capital_agent)
        workflow.add_node("fairness", self._call_fairness_agent)
        workflow.add_node("ops", self._call_ops_agent)
        
        # Define edges
        workflow.set_entry_point("orchestrator")
        
        workflow.add_conditional_edges(
            "orchestrator",
            self._route_to_agent,
            {
                "regulatory": "regulatory",
                "capital": "capital",
                "fairness": "fairness",
                "ops": "ops"
            }
        )
        
        # All agents end the workflow
        workflow.add_edge("regulatory", END)
        workflow.add_edge("capital", END)
        workflow.add_edge("fairness", END)
        workflow.add_edge("ops", END)
        
        return workflow.compile()
    
    def _call_regulatory_agent(self, state: AgentState) -> AgentState:
        """Placeholder for regulatory agent call."""
        state["answer"] = f"Regulatory agent processing: {state['query']}"
        logger.info("Regulatory agent executed")
        return state
    
    def _call_capital_agent(self, state: AgentState) -> AgentState:
        """Placeholder for capital agent call."""
        state["answer"] = f"Capital agent processing: {state['query']}"
        logger.info("Capital agent executed")
        return state
    
    def _call_fairness_agent(self, state: AgentState) -> AgentState:
        """Placeholder for fairness agent call."""
        state["answer"] = f"Fairness agent processing: {state['query']}"
        logger.info("Fairness agent executed")
        return state
    
    def _call_ops_agent(self, state: AgentState) -> AgentState:
        """Placeholder for ops agent call."""
        state["answer"] = f"Ops agent processing: {state['query']}"
        logger.info("Ops agent executed")
        return state
    
    def invoke(self, query: str) -> dict:
        """Execute the orchestrator workflow.
        
        Args:
            query: User question about regulatory/capital/fairness topics
            
        Returns:
            dict with answer and metadata
        """
        initial_state = AgentState(
            messages=[],
            next="",
            query=query,
            domain="",
            context={},
            answer=""
        )
        
        result = self.graph.invoke(initial_state)
        
        return {
            "query": query,
            "domain": result["domain"],
            "answer": result["answer"],
            "context": result.get("context", {})
        }


if __name__ == "__main__":
    # Test the orchestrator
    logging.basicConfig(level=logging.INFO)
    
    orchestrator = Orchestrator()
    
    test_queries = [
        "What are the requirements for SR 11-7 model validation?",
        "How do we calculate CECL provisions under stress?",
        "Can you check this lending model for disparate impact?",
        "What's the data quality for our credit risk models?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*80}")
        print(f"Query: {query}")
        result = orchestrator.invoke(query)
        print(f"Domain: {result['domain']}")
        print(f"Answer: {result['answer']}")
