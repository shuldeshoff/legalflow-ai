# LegalFlow AI

> AI-powered legal automation platform with LLM integration, RAG, and document analysis

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue.svg)](https://www.typescriptlang.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Overview

Full-featured legal automation platform demonstrating modern full-stack development with AI/ML integration. Built with Python FastAPI backend, React frontend, and comprehensive LLM capabilities for document analysis, contract generation, and intelligent client communication.

## Key Features

- **AI Legal Assistant** - RAG-powered chatbot for legal consultations
- **Document Analysis** - Automated contract analysis with risk detection
- **Contract Generator** - Template-based document generation with LLM
- **CRM Integration** - AmoCRM/Bitrix24 connectors
- **Telegram Bot** - Automated client communication
- **Payment Integration** - YooKassa support
- **Knowledge Base** - Semantic search with vector embeddings

## Tech Stack

**Backend**
- FastAPI 0.110 (async/await)
- SQLAlchemy 2.0 (async ORM)
- MySQL 8.0
- Redis (caching)
- LangChain + OpenAI/YandexGPT
- ChromaDB (vector storage)

**Frontend**
- React 18 + TypeScript
- Vite
- TanStack Query
- Zustand
- Tailwind CSS

**Infrastructure**
- Docker + Docker Compose
- Alembic (migrations)
- pytest (testing)
- Nginx

## Architecture

```
┌─────────────────┐
│  React Frontend │
└────────┬────────┘
         │
    ┌────▼────┐
    │ FastAPI │
    └────┬────┘
         │
    ┌────┼─────┬──────┐
    │    │     │      │
┌───▼┐ ┌─▼──┐ ┌▼───┐ ┌▼─────┐
│MySQL│ │Redis│ │LLM│ │CRM   │
└─────┘ └────┘ └───┘ └──────┘
```

## Quick Start

### Requirements
- Python 3.11+
- Node.js 20+
- MySQL 8.0
- Redis 7+

### Installation

```bash
# Clone repository
git clone https://github.com/shuldeshoff/legalflow-ai.git
cd legalflow-ai

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run with Docker
docker-compose up -d

# Or manually:

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Access
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## API Examples

### Document Analysis
```python
POST /api/v1/documents/analyze
{
  "file": "contract.pdf",
  "type": "contract"
}

Response:
{
  "summary": "Service agreement...",
  "key_points": ["Payment terms", "Delivery date"],
  "risks": ["Missing penalty clause"],
  "recommendations": "Add termination conditions"
}
```

### AI Chat
```python
POST /api/v1/llm/chat
{
  "messages": [{"role": "user", "content": "How to terminate a lease?"}],
  "model": "gpt-3.5-turbo"
}

Response (streaming):
{
  "content": "To terminate a lease agreement...",
  "sources": ["Knowledge base"],
  "model": "gpt-3.5-turbo"
}
```

### RAG Query
```python
POST /api/v1/knowledge/rag
{
  "query": "What are client rights?",
  "limit": 3
}

Response:
{
  "answer": "Based on available knowledge...",
  "sources": [{"title": "Civil Code", "score": 0.89}],
  "model": "gpt-3.5-turbo"
}
```

## Testing

```bash
# Run tests
cd backend
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html

# Results
13/13 tests passing
Coverage: 51%
```

## Project Structure

```
legalflow-ai/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Configuration
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   └── services/         # Business logic
│   ├── tests/                # Test suite
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
├── docs/                     # Documentation
└── docker-compose.yml
```

## Key Technical Capabilities

**Backend Development**
- FastAPI with async/await patterns
- SQLAlchemy 2.0 async ORM
- Pydantic validation
- JWT authentication
- File processing (PDF, DOCX)
- Background tasks
- Unit & integration tests

**AI/ML Integration**
- LLM integration (OpenAI, YandexGPT)
- RAG (Retrieval Augmented Generation)
- LangChain orchestration
- Vector database (ChromaDB)
- Semantic search
- Streaming responses
- Prompt engineering

**Frontend Development**
- React 18 with TypeScript
- State management (Zustand + React Query)
- Real-time updates
- Responsive design
- Form validation

**Database & Performance**
- MySQL schema design
- Complex queries & JOINs
- Indexes & optimization
- Migrations (Alembic)
- Connection pooling
- Redis caching

**Integrations**
- REST API clients
- OAuth 2.0
- Webhook handling
- CRM systems
- Telegram Bot API
- Payment systems
- Error handling & retry logic

**DevOps**
- Docker containerization
- Docker Compose orchestration
- Nginx configuration
- Environment management
- Structured logging

## Performance Metrics

- API response time: < 200ms (p95)
- LLM response time: 2-5s (streaming)
- Database queries: < 50ms (indexed)
- Test execution: < 3s
- Code coverage: 51%

## Security

- JWT tokens with refresh mechanism
- SQL injection protection (ORM)
- Password hashing (bcrypt)
- Environment variables for secrets
- CORS configuration
- Input validation

## Documentation

- API Documentation: `/docs` (Swagger UI)
- Alternative docs: `/redoc` (ReDoc)
- Architecture: `docs/ARCHITECTURE.md`
- API Reference: `docs/API.md`
- Testing Guide: `docs/TESTING.md`

## Deployment

```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# Or manual:
# 1. Set up server (Ubuntu 22.04+)
# 2. Install Docker
# 3. Configure environment
# 4. Run containers
# 5. Set up Nginx + SSL
```

## License

MIT License

## Author

**Yuri Shuldeshov**

Full-stack developer specializing in Python, AI/ML, and legal tech automation

- GitHub: [@shuldeshoff](https://github.com/shuldeshoff)
- Telegram: [@shuldeshoff](https://t.me/shuldeshoff)
- Repository: [legalflow-ai](https://github.com/shuldeshoff/legalflow-ai)

---

**Technologies:** Python · FastAPI · React · TypeScript · MySQL · Redis · OpenAI GPT-4 · LangChain · Docker
