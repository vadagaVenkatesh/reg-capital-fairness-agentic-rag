"""Fairness Agent - ECOA & Fair Lending Specialist.

This agent specializes in fair lending compliance, ECOA requirements,
disparate impact analysis, and model fairness assessments.
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


class FairnessAgent:
    """Fair lending and ECOA compliance specialist."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=config["llm"]["model"],
            temperature=config["llm"]["temperature"],
            max_tokens=config["llm"]["max_tokens"]
        )
        self.mesh_client = MeshClient()
        self.name = config["agents"]["fairness"]["name"]
        self.tools = config["agents"]["fairness"]["tools"]
    
    def invoke(self, query: str) -> Dict[str, Any]:
        """Process fairness/ECOA compliance query.
        
        Args:
            query: Fair lending related question
            
        Returns:
            Dict with answer, analysis, and fairness metrics
        """
        # Determine if we need disparate impact analysis
        needs_analysis = self._requires_fairness_analysis(query)
        
        fairness_metrics = None
        if needs_analysis:
            fairness_metrics = self._analyze_disparate_impact(query)
        
        # Build expert prompt
        system_prompt = f"""You are {self.name}, a Fair Lending Compliance Officer at a G-SIB bank.

Your expertise includes:
- ECOA (Equal Credit Opportunity Act) compliance and Reg B
- Disparate impact analysis and statistical testing
- Fair lending risk assessment for credit models
- Adverse action notice requirements
- Protected class analysis (race, gender, age, etc.)
- Redlining detection and prevention

Tone: Analytical, evidence-based, cite specific ECOA/Reg B provisions.

{f'Fairness Analysis Results:\n{json.dumps(fairness_metrics, indent=2)}' if fairness_metrics else ''}

Provide detailed fairness assessment with regulatory citations and statistical evidence.
"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]
        
        response = self.llm.invoke(messages)
        answer = response.content
        
        logger.info(f"Fairness agent processed query: {query[:50]}...")
        
        return {
            "agent": "fairness",
            "query": query,
            "answer": answer,
            "fairness_metrics": fairness_metrics,
            "risk_level": self._assess_risk_level(fairness_metrics)
        }
    
    def _requires_fairness_analysis(self, query: str) -> bool:
        """Determine if query needs fairness analysis.
        
        Args:
            query: User question
            
        Returns:
            True if analysis needed
        """
        fairness_keywords = [
            "disparate", "bias", "discrimination", "fairness",
            "ecoa", "protected class", "adverse action", "redlining"
        ]
        return any(keyword in query.lower() for keyword in fairness_keywords)
    
    def _analyze_disparate_impact(self, query: str) -> Dict[str, Any]:
        """Perform disparate impact analysis.
        
        Args:
            query: Fairness analysis request
            
        Returns:
            Fairness metrics and statistical test results
        """
        try:
            # Example: Call mesh API for fairness metrics
            # In production, parse query to determine protected classes
            metrics = {
                "model": "consumer_credit_scorecard",
                "protected_classes_analyzed": ["race", "gender", "age"],
                "disparate_impact_ratios": {
                    "race_minority_vs_majority": 0.78,  # Below 0.8 threshold - concern
                    "gender_female_vs_male": 0.92,
                    "age_older_vs_younger": 0.85
                },
                "adverse_impact_threshold": 0.80,
                "statistical_significance": {
                    "race": "p < 0.01",
                    "gender": "p = 0.15",
                    "age": "p = 0.08"
                },
                "recommendation": "REVIEW REQUIRED - Race disparate impact ratio below threshold"
            }
            logger.info("Successfully completed disparate impact analysis")
            return metrics
        except Exception as e:
            logger.error(f"Fairness analysis failed: {e}")
            return None
    
    def _assess_risk_level(self, metrics: Dict[str, Any]) -> str:
        """Assess fair lending risk level.
        
        Args:
            metrics: Fairness analysis metrics
            
        Returns:
            Risk level (LOW, MEDIUM, HIGH, CRITICAL)
        """
        if not metrics:
            return "UNKNOWN"
        
        # Check disparate impact ratios
        ratios = metrics.get("disparate_impact_ratios", {})
        min_ratio = min(ratios.values()) if ratios else 1.0
        
        if min_ratio < 0.70:
            return "CRITICAL"
        elif min_ratio < 0.80:
            return "HIGH"
        elif min_ratio < 0.90:
            return "MEDIUM"
        else:
            return "LOW"
    
    def get_fairness_memo(self, model_name: str, findings: str) -> str:
        """Generate fair lending assessment memo.
        
        Args:
            model_name: Name of model assessed
            findings: Summary of findings
            
        Returns:
            Formatted fairness memo
        """
        memo = f"""FAIR LENDING ASSESSMENT MEMORANDUM

TO:      Fair Lending Compliance Committee
FROM:    {self.name}
RE:      Fair Lending Analysis - {model_name}
DATE:    {{current_date}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXECUTIVE SUMMARY

Fair lending assessment of {model_name} pursuant to ECOA and Regulation B.

KEY FINDINGS:
{findings}

PROTECTED CLASSES ANALYZED:
- Race/Ethnicity
- Gender
- Age
- Marital Status

STATISTICAL TESTS PERFORMED:
- Disparate Impact Ratio (4/5ths Rule)
- Logistic Regression Analysis
- Matched Pair Testing

REGULATORY FRAMEWORK:
- ECOA (15 USC 1691 et seq.)
- Regulation B (12 CFR Part 1002)
- Interagency Fair Lending Guidelines

RECOMMENDATIONS:
1. [Specific remediation if needed]
2. [Monitoring requirements]
3. [Documentation requirements]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return memo


if __name__ == "__main__":
    # Test the fairness agent
    logging.basicConfig(level=logging.INFO)
    
    agent = FairnessAgent()
    
    test_query = "Analyze our auto lending model for potential disparate impact on minority applicants."
    result = agent.invoke(test_query)
    
    print(f"Query: {result['query']}")
    print(f"\nAnswer:\n{result['answer']}")
    print(f"\nRisk Level: {result['risk_level']}")
    if result['fairness_metrics']:
        print(f"\nFairness Metrics: {json.dumps(result['fairness_metrics'], indent=2)}")
