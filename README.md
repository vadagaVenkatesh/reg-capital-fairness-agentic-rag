# Regulatory Capital & Fairness Agentic RAG System

**Capital Governance Pivot Agent**: An AI-powered regulatory co-pilot for bank risk management

## Overview

This repository implements a **Compliance-as-Code Operating System** for banks. The system acts as a "Regulatory Co-Pilot" focusing on **Governance, Capital Strategy, and Fairness Reasoning** by calling the consumer-risk-model-mesh as a tool.

### Key Capabilities
- SR 11-7 Model Validation
- Basel III Capital Analysis
- CECL Accounting
- Fair Lending Compliance (ECOA)
- Operational Resilience

## Architecture

Agentic RAG + Quantitative Mesh architecture with 5 specialized agents:
1. **Orchestrator** - Routes queries to specialists
2. **Regulatory Agent** - SR 11-7 & Basel specialist
3. **Capital Agent** - CECL & RWA specialist  
4. **Fairness Agent** - ECOA/Reg B specialist
5. **Ops Agent** - Resilience watchdog

## Project Structure Created

- pyproject.toml ✅
- config/settings.yaml ✅  
- .gitignore ✅

## Quick Start

```bash
git clone https://github.com/vadagaVenkatesh/reg-capital-fairness-agentic-rag.git
cd reg-capital-fairness-agentic-rag
pip install -e .[dev]
```

## Integration

Connects to [consumer-risk-model-mesh](https://github.com/vadagaVenkatesh/consumer-risk-model-mesh) for quantitative calculations.

## API Usage

### Start the FastAPI Server

```bash
python -m app.main
# Server runs on http://localhost:8000
```

### Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Query via Orchestrator (Auto-routing)
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the SR 11-7 requirements for model validation?"
  }'
```

#### Direct Agent Queries

**Regulatory Agent:**
```bash
curl -X POST http://localhost:8000/query/regulatory \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain Basel III capital adequacy requirements"
  }'
```

**Capital Agent:**
```bash
curl -X POST http://localhost:8000/query/capital \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Calculate CECL provisions under stressed scenario"
  }'
```

**Fairness Agent:**
```bash
curl -X POST http://localhost:8000/query/fairness \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Check this lending model for disparate impact"
  }'
```

**Ops Agent:**
```bash
curl -X POST http://localhost:8000/query/ops \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the data quality for our credit risk models?"
  }'
```

### Docker Deployment

```bash
docker-compose up
# Access API at http://localhost:8000
# Vector DB at http://localhost:6333
```


## Author

**VDG Venkatesh** - [@vadagaVenkatesh](https://github.com/vadagaVenkatesh)
