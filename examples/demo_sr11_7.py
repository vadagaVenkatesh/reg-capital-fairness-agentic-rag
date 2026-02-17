#!/usr/bin/env python3
"""Demo: SR 11-7 Model Validation Workflow

This script demonstrates the Regulatory Capital Fairness Agentic RAG System
for answering SR 11-7 regulatory questions and generating validation memos.
"""
import os
import logging
from app.agents import Orchestrator, RegulatoryAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def demo_orchestrator():
    """Demo orchestrator routing to different agents."""
    print("=" * 80)
    print("DEMO 1: Orchestrator Domain Routing")
    print("=" * 80)
    
    orchestrator = Orchestrator()
    
    queries = [
        "What are the key requirements for SR 11-7 model validation?",
        "How should we calculate CECL provisions for commercial loans?",
        "Can you analyze this lending model for disparate impact?",
        "What metrics should we track for model drift detection?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        result = orchestrator.invoke(query)
        print(f"Domain: {result['domain']}")
        print(f"Answer: {result['answer'][:150]}...")
        print("-" * 80)


def demo_regulatory_agent():
    """Demo regulatory agent with RAG capabilities."""
    print("\n" + "=" * 80)
    print("DEMO 2: Regulatory Agent with RAG")
    print("=" * 80)
    
    agent = RegulatoryAgent()
    
    # Example 1: General SR 11-7 question
    query1 = "What are the three components of effective model validation per SR 11-7?"
    print(f"\nQuery: {query1}")
    result1 = agent.invoke(query1)
    print(f"\nAnswer:\n{result1['answer']}")
    print(f"\nCitations: {', '.join(result1['citations'])}")
    print(f"Context documents used: {len(result1['context'])}")
    
    # Example 2: Basel capital requirements
    query2 = "What are the minimum capital ratios under Basel III?"
    print(f"\n{'-'*80}")
    print(f"Query: {query2}")
    result2 = agent.invoke(query2)
    print(f"\nAnswer:\n{result2['answer']}")
    print(f"\nCitations: {', '.join(result2['citations'])}")


def demo_validation_memo():
    """Demo generating a model validation memo."""
    print("\n" + "=" * 80)
    print("DEMO 3: Model Validation Memo Generation")
    print("=" * 80)
    
    agent = RegulatoryAgent()
    memo = agent.get_model_validation_report("Credit Risk Scorecard v2.1")
    print(memo)


def main():
    """Run all demos."""
    print("\n" + "#" * 80)
    print("#" + " " * 78 + "#")
    print("#  Regulatory Capital & Fairness Agentic RAG System - Demo".ljust(79) + "#")
    print("#  SR 11-7 Model Validation & Compliance Workflow".ljust(79) + "#")
    print("#" + " " * 78 + "#")
    print("#" * 80 + "\n")
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY environment variable not set!")
        print("\nERROR: Please set your OPENAI_API_KEY environment variable:")
        print("export OPENAI_API_KEY='your-api-key-here'\n")
        return
    
    try:
        # Run demos
        demo_orchestrator()
        demo_regulatory_agent()
        demo_validation_memo()
        
        print("\n" + "#" * 80)
        print("#  Demo completed successfully!".ljust(79) + "#")
        print("#" * 80 + "\n")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"\nERROR: {e}")
        print("\nMake sure you have:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Installed all dependencies: pip install -e .")
        print("3. Proper network connectivity\n")


if __name__ == "__main__":
    main()
