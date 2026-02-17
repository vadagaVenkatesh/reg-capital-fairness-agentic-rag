"""FastAPI server for Regulatory Capital Fairness Agentic RAG System.

This module provides REST API endpoints to query the orchestrator and specialist agents.
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from app.agents.orchestrator import Orchestrator
from app.agents.regulatory_agent import RegulatoryAgent
from app.agents.capital_agent import CapitalAgent
from app.agents.fairness_agent import FairnessAgent
from app.agents.ops_agent import OpsAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Regulatory Capital Fairness RAG System",
    description="Agentic RAG system for bank risk management compliance",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = Orchestrator()


class QueryRequest(BaseModel):
    """Request model for query endpoint."""
    query: str = Field(..., description="User question about regulatory/capital/fairness topics")
    domain: Optional[str] = Field(None, description="Optional: specific domain (regulatory, capital, fairness, ops)")


class QueryResponse(BaseModel):
    """Response model for query endpoint."""
    query: str
    domain: str
    answer: str
    context: Dict[str, Any] = {}


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Regulatory Capital Fairness RAG System",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "orchestrator": "operational",
        "agents": {
            "regulatory": "operational",
            "capital": "operational",
            "fairness": "operational",
            "ops": "operational"
        }
    }


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Process query through orchestrator.
    
    The orchestrator will automatically classify the query and route it to the
    appropriate specialist agent (Regulatory, Capital, Fairness, or Ops).
    """
    try:
        logger.info(f"Processing query: {request.query}")
        result = orchestrator.invoke(request.query)
        return QueryResponse(**result)
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query/regulatory", response_model=QueryResponse)
async def query_regulatory(request: QueryRequest):
    """Direct query to regulatory agent (SR 11-7, Basel, model risk)."""
    try:
        agent = RegulatoryAgent()
        result = agent.invoke(request.query)
        return QueryResponse(
            query=request.query,
            domain="regulatory",
            answer=result["answer"],
            context=result.get("context", {})
        )
    except Exception as e:
        logger.error(f"Error in regulatory agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query/capital", response_model=QueryResponse)
async def query_capital(request: QueryRequest):
    """Direct query to capital agent (CECL, RWA, capital calculations)."""
    try:
        agent = CapitalAgent()
        result = agent.invoke(request.query)
        return QueryResponse(
            query=request.query,
            domain="capital",
            answer=result["answer"],
            context=result.get("context", {})
        )
    except Exception as e:
        logger.error(f"Error in capital agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query/fairness", response_model=QueryResponse)
async def query_fairness(request: QueryRequest):
    """Direct query to fairness agent (ECOA, disparate impact analysis)."""
    try:
        agent = FairnessAgent()
        result = agent.invoke(request.query)
        return QueryResponse(
            query=request.query,
            domain="fairness",
            answer=result["answer"],
            context=result.get("context", {})
        )
    except Exception as e:
        logger.error(f"Error in fairness agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query/ops", response_model=QueryResponse)
async def query_ops(request: QueryRequest):
    """Direct query to ops agent (data quality, model drift monitoring)."""
    try:
        agent = OpsAgent()
        result = agent.invoke(request.query)
        return QueryResponse(
            query=request.query,
            domain="ops",
            answer=result["answer"],
            context=result.get("context", {})
        )
    except Exception as e:
        logger.error(f"Error in ops agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
