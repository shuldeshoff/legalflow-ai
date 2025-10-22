# 🛠️ Технологический стек LegalFlow AI

**Дата:** 22 октября 2025  
**Проект:** LegalFlow AI  
**Автор:** Юрий Шульдешов

## Обзор

Проект построен на современном Python + React стеке с фокусом на AI/ML интеграции и масштабируемость.

## Backend Stack (Python)

### Core Framework
```python
FastAPI 0.110.0
- Async/await из коробки
- Автоматическая валидация (Pydantic)
- OpenAPI/Swagger документация
- Dependency Injection
- WebSocket поддержка
- Высокая производительность

Uvicorn 0.27.0
- ASGI сервер
- HTTP/2 поддержка
- WebSocket
- Graceful shutdown
```

### Database
```python
# ORM
SQLAlchemy 2.0.25
- Async support
- Декларативный синтаксис
- Relationship management
- Query optimization

# Миграции
Alembic 1.13.1
- Автогенерация миграций
- Версионирование схемы
- Rollback support

# Driver
PyMySQL 1.1.0
- Pure Python MySQL client
- Async support
```

### Кеширование и очереди
```python
# Redis
redis 5.0.1
- Кеширование ответов
- Session storage
- Rate limiting
- Pub/Sub для real-time

# Task Queue
Celery 5.3.6
- Background tasks
- Scheduled tasks
- Retry logic
- Result backend
```

### AI/ML/NLP Stack
```python
# LLM Integration
openai 1.12.0
- GPT-4 API
- Streaming responses
- Function calling
- Vision API (опционально)

# LLM Framework
langchain 0.1.6
- Chain abstractions
- Prompt templates
- Memory management
- Agent framework

# Vector Database
chromadb 0.4.22
- Embeddings storage
- Semantic search
- Collection management
- Persistent storage

# Alternative: Pinecone
pinecone-client 3.0.2
- Managed vector DB
- Serverless option
- High performance

# NLP
spacy 3.7.2
- Named Entity Recognition
- Part-of-speech tagging
- Dependency parsing
- Russian language support

# Text Processing
nltk 3.8.1
- Tokenization
- Stemming
- Text preprocessing
```

### Document Processing
```python
# PDF
PyPDF2 3.0.1
- PDF text extraction
- Metadata reading
- Page manipulation

# Alternative: pdfplumber
pdfplumber 0.11.0
- Better table extraction
- Layout analysis

# Word Documents
python-docx 1.1.0
- DOCX reading/writing
- Styling support
- Tables and images

# File Upload
python-multipart 0.0.6
- Multipart form data
- File handling
```

### Интеграции
```python
# HTTP Client
aiohttp 3.9.3
- Async HTTP requests
- Session management
- Timeout handling
- Connection pooling

# Telegram Bot
aiogram 3.4.1
- Modern async bot framework
- FSM (Finite State Machine)
- Filters and handlers
- Webhook support

# Alternative: python-telegram-bot
python-telegram-bot 20.7
- Более зрелая библиотека
```

### Авторизация и безопасность
```python
# JWT
python-jose[cryptography] 3.3.0
- JWT encoding/decoding
- Token validation
- Cryptographic signing

# Password hashing
passlib[bcrypt] 1.7.4
- Bcrypt hashing
- Password verification
- Multiple algorithms

# CORS
fastapi-cors
- Cross-origin requests
- Credentials support
```

### Валидация и сериализация
```python
# Validation
pydantic 2.6.1
- Data validation
- Type checking
- JSON schema generation
- Settings management

pydantic-settings 2.1.0
- Environment variables
- .env file support
- Settings validation
```

### Логирование и мониторинг
```python
# Structured Logging
structlog 24.1.0
- JSON logging
- Context binding
- Log levels
- Performance logging

# Monitoring
prometheus-client 0.19.0
- Metrics collection
- Histogram/Counter/Gauge
- HTTP middleware
```

### Тестирование
```python
# Test Framework
pytest 8.0.0
- Fixture support
- Parametrize tests
- Plugins ecosystem

pytest-asyncio 0.23.4
- Async test support
- Event loop management

pytest-cov 4.1.0
- Coverage reporting
- HTML reports

# HTTP Testing
httpx 0.26.0
- Async HTTP client
- TestClient for FastAPI

# Mocking
pytest-mock 3.12.0
- Easy mocking
- Spy functionality
```

## Frontend Stack (React)

### Core
```typescript
React 18.2.0
- Hooks API
- Concurrent rendering
- Suspense
- Server Components ready

TypeScript 5.3.3
- Static typing
- Type inference
- Strict mode
- Declaration files
```

### Build Tool
```typescript
Vite 5.0.12
- Lightning fast HMR
- Optimized builds
- Plugin ecosystem
- ESM native
```

### Routing
```typescript
React Router 6.21.3
- Client-side routing
- Nested routes
- Lazy loading
- Search params
```

### State Management
```typescript
// Server State
@tanstack/react-query 5.17.19
- Data fetching
- Caching
- Auto refetch
- Optimistic updates
- Infinite queries

// Client State
zustand 4.4.7
- Minimal boilerplate
- TypeScript support
- Devtools
- Persist middleware
```

### HTTP Client
```typescript
axios 1.6.5
- Promise based
- Interceptors
- Request/response transform
- Cancel requests
- TypeScript support
```

### UI Components
```typescript
// Styling
tailwindcss 3.4.1
- Utility-first CSS
- JIT compiler
- Dark mode support
- Custom theming

// Component Library
shadcn/ui latest
- Radix UI primitives
- Fully customizable
- Accessible
- TypeScript first

// Icons
lucide-react 0.307.0
- Modern icon set
- Tree-shakeable
- Consistent design
```

### Forms
```typescript
react-hook-form 7.49.3
- Performance optimized
- Validation
- TypeScript support
- Easy integration

zod 3.22.4
- Schema validation
- Type inference
- Custom validators
```

### Rich Text
```typescript
react-markdown 9.0.1
- Markdown rendering
- Syntax highlighting
- Custom components

remark-gfm 4.0.0
- GitHub Flavored Markdown
- Tables, strikethrough
- Task lists
```

### Charts
```typescript
recharts 2.10.3
- Declarative charts
- Responsive
- Animation
- Customizable
```

### Date/Time
```typescript
date-fns 3.2.0
- Modern date utility
- Tree-shakeable
- Immutable
- i18n support
```

## Database Schema (MySQL 8.0)

### Основные таблицы
```sql
-- Пользователи
users
  id (PK)
  email (UNIQUE)
  password_hash
  full_name
  role (enum: admin, lawyer, client)
  created_at
  updated_at

-- Клиенты
clients
  id (PK)
  user_id (FK → users)
  phone
  telegram_id
  crm_id
  status
  created_at

-- Документы
documents
  id (PK)
  client_id (FK → clients)
  type (enum: contract, claim, complaint)
  file_path
  original_name
  mime_type
  size
  uploaded_by (FK → users)
  created_at

-- Анализ документов
document_analyses
  id (PK)
  document_id (FK → documents)
  parties (JSON)
  amounts (JSON)
  dates (JSON)
  risks (JSON)
  summary (TEXT)
  confidence
  analyzed_at

-- Шаблоны договоров
contract_templates
  id (PK)
  name
  category
  template_path
  variables (JSON)
  created_by (FK → users)
  created_at

-- Сгенерированные договоры
generated_contracts
  id (PK)
  template_id (FK → contract_templates)
  client_id (FK → clients)
  data (JSON)
  file_path
  created_by (FK → users)
  created_at

-- База знаний
knowledge_base
  id (PK)
  title
  content (TEXT)
  category
  source
  embedding_id
  created_at
  updated_at

-- Чат сообщения
chat_messages
  id (PK)
  session_id
  client_id (FK → clients)
  role (enum: user, assistant)
  content (TEXT)
  tokens
  sources (JSON)
  created_at

-- CRM интеграции
crm_integrations
  id (PK)
  provider (enum: amocrm, bitrix24)
  access_token
  refresh_token
  domain
  user_id (FK → users)
  created_at

-- Лиды
leads
  id (PK)
  client_id (FK → clients)
  source
  status
  crm_id
  amount
  created_at
  updated_at

-- Платежи
payments
  id (PK)
  client_id (FK → clients)
  amount
  currency
  status (enum: pending, success, failed)
  provider
  transaction_id
  created_at
```

### Индексы
```sql
-- Performance optimization
CREATE INDEX idx_clients_user_id ON clients(user_id);
CREATE INDEX idx_clients_telegram_id ON clients(telegram_id);
CREATE INDEX idx_documents_client_id ON documents(client_id);
CREATE INDEX idx_documents_created_at ON documents(created_at);
CREATE INDEX idx_chat_session_id ON chat_messages(session_id);
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_payments_status ON payments(status);
```

## DevOps Stack

### Контейнеризация
```yaml
Docker 24.0+
- Multi-stage builds
- Layer caching
- Health checks
- Volume management

Docker Compose 2.20+
- Service orchestration
- Network isolation
- Environment management
```

### Reverse Proxy
```nginx
Nginx 1.25
- Load balancing
- SSL termination
- Static file serving
- Gzip compression
- Rate limiting
```

### Мониторинг
```yaml
Prometheus 2.48
- Metrics collection
- Time series DB
- PromQL queries
- Alerting rules

Grafana 10.2
- Visualization
- Custom dashboards
- Alert management
- Data exploration
```

### CI/CD
```yaml
GitHub Actions
- Automated testing
- Docker builds
- Deployment automation
- Security scanning
```

## Development Tools

### Code Quality
```yaml
# Python
black 24.1.0         # Formatting
flake8 7.0.0         # Linting
mypy 1.8.0           # Type checking
isort 5.13.2         # Import sorting

# TypeScript
eslint 8.56.0        # Linting
prettier 3.2.4       # Formatting
```

### Git Hooks
```yaml
pre-commit 3.6.0
- Code formatting
- Linting
- Type checking
- Test running
```

## Сервисы третьих сторон

### AI/ML
```yaml
OpenAI API
- GPT-4 для чата
- text-embedding-ada-002 для embeddings
- ~$0.03/1K tokens (GPT-4)

YandexGPT
- Альтернатива OpenAI
- Русский язык
- ~₽0.16/1K tokens
```

### CRM
```yaml
AmoCRM API
- OAuth 2.0
- REST API
- Webhooks
- Rate limits: 7 req/sec

Bitrix24 API
- OAuth 2.0
- REST API
- Webhooks
```

### Мессенджеры
```yaml
Telegram Bot API
- Long polling / Webhooks
- File uploads до 50MB
- Inline keyboards
- Free

WhatsApp Business API
- Cloud API / On-premises
- Templates required
- Paid (~$0.005/message)
```

### Платежи
```yaml
ЮKassa
- REST API
- Webhook уведомления
- Комиссия ~2.8%
- Быстрая интеграция

CloudPayments
- REST API
- Рекуррентные платежи
- Комиссия ~2.8%
```

## Архитектурные паттерны

### Backend
```
Repository Pattern
- Абстракция доступа к данным
- Легкое тестирование
- Смена БД без изменения бизнес-логики

Service Layer
- Бизнес-логика отдельно от API
- Переиспользование кода
- Легкое тестирование

Dependency Injection
- FastAPI Depends
- Слабая связанность
- Легкое mock'ирование в тестах
```

### Frontend
```
Feature-based structure
- Все файлы фичи в одной папке
- Легко находить код
- Масштабируемость

Custom Hooks
- Переиспользование логики
- Чистые компоненты
- Легкое тестирование

Component Composition
- Маленькие компоненты
- Переиспользование
- Читаемость
```

## Performance Optimization

### Backend
```python
# Кеширование
- Redis для частых запросов (TTL 5-60 мин)
- LLM ответов (exact match)
- Embeddings результатов

# Database
- Connection pooling (min=5, max=20)
- Lazy loading relationships
- Pagination везде (limit 20-100)
- Индексы на FK и частых WHERE

# Async
- Все IO операции async
- Concurrent requests где возможно
- Background tasks через Celery
```

### Frontend
```typescript
// Code splitting
- React.lazy для больших компонентов
- Route-based splitting
- Component lazy loading

// Caching
- React Query staleTime (5 мин)
- LocalStorage для settings
- IndexedDB для больших данных

// Optimization
- Debounce поисковых запросов (300ms)
- Виртуализация длинных списков
- Image optimization (WebP)
```

## Security Best Practices

```yaml
Authentication:
  - JWT с refresh tokens
  - Token expiration (15 мин access, 7 дней refresh)
  - Secure cookie для refresh token
  - Password hashing (bcrypt, cost=12)

Authorization:
  - Role-based access control (RBAC)
  - Resource-level permissions
  - API key для внешних интеграций

Data Protection:
  - HTTPS обязательно
  - SQL injection защита (ORM)
  - XSS protection (CSP headers)
  - Rate limiting (10-100 req/min)
  - Input validation (Pydantic)

Secrets:
  - Environment variables
  - Never commit to git
  - Rotation политика
```

## Scalability Strategy

### Horizontal Scaling
```
Backend:
  - Stateless API (JWT токены)
  - Load balancer (Nginx/HAProxy)
  - Multiple uvicorn workers

Database:
  - Read replicas для аналитики
  - Connection pooling
  - Query optimization

Celery:
  - Multiple workers
  - Task routing по очередям
  - Result backend в Redis
```

### Vertical Scaling
```
Resources:
  - CPU: 4+ cores для LLM операций
  - RAM: 8GB+ для векторных операций
  - SSD: быстрый доступ к БД
```

## Cost Optimization

### Development
```
Local:
  - MySQL: Docker (free)
  - Redis: Docker (free)
  - OpenAI: $20/month для тестов

Development server:
  - VPS: $10-20/month (Hetzner, Contabo)
  - Domain: $10/year
```

### Production
```
Small scale (100 users):
  - VPS: $40/month (4GB RAM, 2 CPU)
  - MySQL: Same VPS
  - OpenAI: $50-100/month
  - Total: ~$100/month

Medium scale (1000 users):
  - VPS: $80/month (8GB RAM, 4 CPU)
  - Managed MySQL: $30/month
  - OpenAI: $200-500/month
  - CDN: $20/month
  - Total: ~$350/month
```

## Альтернативные технологии

### Если заказчик предпочитает другое
```python
# Backend альтернативы
Django + DRF      # Если нужен админ-панель из коробки
Flask             # Если нужна простота
Tornado           # Если нужны WebSocket

# Database альтернативы
PostgreSQL        # Если нужен PostGIS или лучший full-text search
MongoDB           # Если документо-ориентированная модель

# Frontend альтернативы
Vue 3 + Nuxt      # Если команда предпочитает Vue
Next.js           # Если нужен SSR
Svelte + SvelteKit # Если нужна легковесность
```

## Выводы

Этот стек обеспечивает:
- ✅ Modern Python best practices (async, type hints)
- ✅ Production-ready AI интеграции
- ✅ Масштабируемость (горизонтальная и вертикальная)
- ✅ Отличный Developer Experience
- ✅ Type safety (TypeScript + Pydantic + mypy)
- ✅ Comprehensive testing capabilities
- ✅ Cost effective (оптимизация расходов)

**Стек демонстрирует все требуемые навыки для вакансии!** ✨
