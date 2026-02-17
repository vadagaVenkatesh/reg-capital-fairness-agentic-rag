"""Ops Agent - Data Quality & Model Drift Specialist.

This agent specializes in operational resilience, data quality monitoring,
model drift detection, and ongoing performance surveillance.
"""
import logging
from typing import List, Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import yaml

logger = logging.getLogger(__name__)

with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)


class OpsAgent:
    """Operational resilience and model monitoring specialist."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=config["llm"]["model"],
            temperature=config["llm"]["temperature"],
            max_tokens=config["llm"]["max_tokens"]
        )
        self.name = config["agents"]["ops"]["name"]
        self.tools = config["agents"]["ops"]["tools"]
    
    def invoke(self, query: str) -> Dict[str, Any]:
        """Process operational resilience query."""
        system_prompt = f"""You are {self.name}, an Operational Risk Officer specializing in model operations.

Your expertise includes:
- Model drift detection and remediation
- Data quality assessment (completeness, accuracy, timeliness)
- Performance degradation analysis
- Operational resilience per SR 11-7 Appendix B
- Automated monitoring and alerting

Tone: Operational, data-driven, action-oriented.

Provide specific recommendations for operational improvements.
"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]
        
        response = self.llm.invoke(messages)
        logger.info(f"Ops agent processed query: {query[:50]}...")
        
        return {
            "agent": "ops",
            "query": query,
            "answer": response.content,
            "monitoring_recommendations": self._generate_monitoring_plan()
        }
    
    def _generate_monitoring_plan(self) -> List[str]:
        """Generate operational monitoring recommendations."""
        return [
            "Monitor model performance metrics daily",
            "Track data quality scores (>95% completeness target)",
            "Alert on drift detection (PSI > 0.25)",
            "Review model logs for anomalies"
        ]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = OpsAgent()
    result = agent.invoke("How should we monitor for model drift in our credit risk models?")
    print(f"Answer: {result['answer']}")
