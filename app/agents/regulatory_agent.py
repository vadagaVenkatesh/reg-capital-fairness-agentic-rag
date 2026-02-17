"""Regulatory Agent - SR 11-7 & Basel Specialist.

This agent specializes in regulatory model validation, SR 11-7 compliance,
Basel capital requirements, and model risk management guidance.
"""
import logging
from typing import List, Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import yaml

logger = logging.getLogger(__name__)

# Load configuration
with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)


class RegulatoryAgent:
    """SR 11-7 and Basel regulatory specialist with RAG capabilities."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=config["llm"]["model"],
            temperature=config["llm"]["temperature"],
            max_tokens=config["llm"]["max_tokens"]
        )
        self.embeddings = OpenAIEmbeddings(
            model=config["embeddings"]["model"]
        )
        self.name = config["agents"]["regulatory"]["name"]
        self.tools = config["agents"]["regulatory"]["tools"]
        self.vector_store = None
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Initialize FAISS vector store with regulatory documents."""
        # In production, load actual regulatory documents
        # For now, using placeholder knowledge
        documents = [
            "SR 11-7 requires banks to have robust model validation frameworks.",
            "Model validation must include conceptual soundness evaluation.",
            "Ongoing monitoring is required for all models per SR 11-7.",
            "Basel III requires banks to maintain minimum capital ratios.",
            "Tier 1 capital ratio must be at least 6% under Basel III.",
            "Model Risk Management requires independent validation."
        ]
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config["rag"]["chunk_size"],
            chunk_overlap=config["rag"]["chunk_overlap"]
        )
        
        splits = text_splitter.create_documents(documents)
        self.vector_store = FAISS.from_documents(splits, self.embeddings)
        logger.info("Regulatory knowledge base initialized")
    
    def _retrieve_context(self, query: str, k: int = 3) -> List[str]:
        """Retrieve relevant context from vector store.
        
        Args:
            query: User question
            k: Number of documents to retrieve
            
        Returns:
            List of relevant document chunks
        """
        if not self.vector_store:
            return []
        
        docs = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
    
    def invoke(self, query: str) -> Dict[str, Any]:
        """Process regulatory query with RAG.
        
        Args:
            query: Regulatory compliance question
            
        Returns:
            Dict with answer, citations, and metadata
        """
        # Retrieve relevant context
        context_docs = self._retrieve_context(
            query, 
            k=config["rag"]["retrieval_k"]
        )
        context = "\n\n".join(context_docs)
        
        # Build prompt with regulatory expertise persona
        system_prompt = f"""You are {self.name}, a Senior Risk Officer specializing in 
regulatory model validation and compliance at a G-SIB bank.

Your expertise includes:
- SR 11-7: Supervisory Guidance on Model Risk Management
- Basel III/IV capital requirements
- Model validation frameworks
- Conceptual soundness assessment
- Ongoing monitoring and backtesting

Tone: Professional, precise, cite specific regulatory sections.

Relevant Regulatory Context:
{context}

Provide detailed guidance citing specific regulatory requirements.
"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]
        
        response = self.llm.invoke(messages)
        answer = response.content
        
        logger.info(f"Regulatory agent processed query: {query[:50]}...")
        
        return {
            "agent": "regulatory",
            "query": query,
            "answer": answer,
            "context": context_docs,
            "citations": self._extract_citations(answer)
        }
    
    def _extract_citations(self, answer: str) -> List[str]:
        """Extract regulatory citations from answer.
        
        Args:
            answer: Agent response text
            
        Returns:
            List of cited regulations
        """
        citations = []
        # Simple citation extraction - in production use regex
        if "SR 11-7" in answer:
            citations.append("SR 11-7")
        if "Basel" in answer:
            citations.append("Basel III")
        return citations
    
    def get_model_validation_report(self, model_name: str) -> str:
        """Generate model validation memo format.
        
        Args:
            model_name: Name of the model to validate
            
        Returns:
            Formatted validation memo
        """
        memo = f"""MEMORANDUM

TO:      Model Risk Management Committee
FROM:    {self.name}
RE:      Model Validation Report - {model_name}
DATE:    {{current_date}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXECUTIVE SUMMARY

Pursuant to SR 11-7 Supervisory Guidance on Model Risk Management, this 
memorandum documents the independent validation of the {model_name}.

KEY FINDINGS:
- Conceptual Soundness: [Assessment]
- Ongoing Monitoring: [Assessment]
- Outcomes Analysis: [Assessment]

REGULATORY FRAMEWORK:
- SR 11-7 (Model Risk Management)
- OCC 2011-12 (Sound Practices)
- Basel III Framework

RECOMMENDATIONS:
[Model-specific recommendations]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return memo


if __name__ == "__main__":
    # Test the regulatory agent
    logging.basicConfig(level=logging.INFO)
    
    agent = RegulatoryAgent()
    
    test_query = "What are the three key components of model validation under SR 11-7?"
    result = agent.invoke(test_query)
    
    print(f"Query: {result['query']}")
    print(f"\nAnswer: {result['answer']}")
    print(f"\nCitations: {result['citations']}")
    print(f"\nContext used: {len(result['context'])} documents")
