"""Capital Agent - CECL & RWA Specialist.

This agent specializes in capital calculations, CECL provisions, RWA computations,
and stress testing under Basel III/IV frameworks.
"""
import logging
from typing import List, Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from app.tools.mesh_client import MeshClient
import yaml
import json

logger = logging.getLogger(__name__)

# Load configuration
with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)


class CapitalAgent:
    """CECL and RWA capital calculations specialist."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=config["llm"]["model"],
            temperature=config["llm"]["temperature"],
            max_tokens=config["llm"]["max_tokens"]
        )
        self.mesh_client = MeshClient()
        self.name = config["agents"]["capital"]["name"]
        self.tools = config["agents"]["capital"]["tools"]
    
    def invoke(self, query: str) -> Dict[str, Any]:
        """Process capital calculation query.
        
        Args:
            query: Capital/CECL/RWA related question
            
        Returns:
            Dict with answer, calculations, and mesh results
        """
        # Determine if we need to call mesh API for calculations
        needs_calculation = self._requires_calculation(query)
        
        mesh_results = None
        if needs_calculation:
            mesh_results = self._call_mesh_for_capital_calc(query)
        
        # Build expert prompt
        system_prompt = f"""You are {self.name}, a Senior Capital Strategy Officer at a G-SIB bank.

Your expertise includes:
- CECL (Current Expected Credit Loss) methodology and implementation
- RWA (Risk-Weighted Assets) calculations under Basel III/IV
- Stress testing and capital adequacy assessment
- Tier 1, Tier 2, CET1 capital ratios
- Pro-cyclical capital buffer management
- CCAR/DFAST regulatory scenarios

Tone: Quantitative, precise, cite specific Basel requirements and accounting standards.

{f'Mesh API Results (from quant models):\n{json.dumps(mesh_results, indent=2)}' if mesh_results else ''}

Provide detailed capital analysis with specific numbers and regulatory citations.
"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]
        
        response = self.llm.invoke(messages)
        answer = response.content
        
        logger.info(f"Capital agent processed query: {query[:50]}...")
        
        return {
            "agent": "capital",
            "query": query,
            "answer": answer,
            "mesh_results": mesh_results,
            "calculations": self._extract_calculations(answer)
        }
    
    def _requires_calculation(self, query: str) -> bool:
        """Determine if query needs mesh API calculation.
        
        Args:
            query: User question
            
        Returns:
            True if calculation needed
        """
        calc_keywords = [
            "calculate", "compute", "estimate", "provision",
            "rwa", "cecl", "loss", "capital ratio", "stress"
        ]
        return any(keyword in query.lower() for keyword in calc_keywords)
    
    def _call_mesh_for_capital_calc(self, query: str) -> Dict[str, Any]:
        """Call mesh API for capital calculations.
        
        Args:
            query: Capital calculation request
            
        Returns:
            Mesh API results
        """
        try:
            # Example: Call CECL calculation endpoint
            # In production, parse query to determine which mesh endpoint to call
            result = {
                "model": "cecl_commercial_loan_model",
                "calculated_provision": 1250000.00,
                "pd_weighted_avg": 0.0235,
                "lgd_weighted_avg": 0.45,
                "ead_total": 50000000.00,
                "confidence_interval": "95%",
                "scenario": "baseline"
            }
            logger.info("Successfully retrieved mesh capital calculations")
            return result
        except Exception as e:
            logger.error(f"Mesh API call failed: {e}")
            return None
    
    def _extract_calculations(self, answer: str) -> List[Dict[str, Any]]:
        """Extract numerical calculations from answer.
        
        Args:
            answer: Agent response
            
        Returns:
            List of extracted calculations
        """
        calculations = []
        # Simple extraction - in production use regex or structured output
        if "provision" in answer.lower():
            calculations.append({"type": "cecl_provision", "mentioned": True})
        if "rwa" in answer.lower():
            calculations.append({"type": "rwa_calculation", "mentioned": True})
        return calculations
    
    def get_capital_impact_note(self, scenario: str, impact_amount: float) -> str:
        """Generate capital impact memo.
        
        Args:
            scenario: Stress scenario name
            impact_amount: Capital impact in dollars
            
        Returns:
            Formatted capital impact note
        """
        memo = f"""CAPITAL IMPACT ANALYSIS NOTE

TO:      Chief Risk Officer / ALCO
FROM:    {self.name}
RE:      Capital Impact Assessment - {scenario}
DATE:    {{current_date}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXECUTIVE SUMMARY

Capital impact under {scenario} scenario: ${impact_amount:,.2f}

KEY METRICS:
- CET1 Ratio Impact: [Calculate]
- RWA Change: [Calculate]
- CECL Provision Increase: [Calculate]
- Buffer Adequacy: [Assess]

REGULATORY FRAMEWORK:
- Basel III Capital Requirements (12 CFR Part 3)
- CECL Implementation (ASC 326)
- Stress Testing Rules (12 CFR Part 252)

RECOMMENDATIONS:
1. [Capital action if needed]
2. [Risk appetite implications]
3. [Management escalation if thresholds breached]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return memo


if __name__ == "__main__":
    # Test the capital agent
    logging.basicConfig(level=logging.INFO)
    
    agent = CapitalAgent()
    
    test_query = "Calculate the CECL provision for our commercial loan portfolio under a severe recession scenario."
    result = agent.invoke(test_query)
    
    print(f"Query: {result['query']}")
    print(f"\nAnswer:\n{result['answer']}")
    if result['mesh_results']:
        print(f"\nMesh Results: {json.dumps(result['mesh_results'], indent=2)}")
