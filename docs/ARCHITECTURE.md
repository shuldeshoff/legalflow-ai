# 🏛️ Архитектура LegalFlow AI

**Дата:** 22 октября 2025  
**Версия:** 1.0  
**Автор:** Юрий Шульдешов

## 📐 Общая архитектура

```
┌──────────────────────────────────────────────────────────────┐
│                         Client Layer                          │
│  Web Browser │ Telegram App │ Mobile Browser │ API Clients   │
└─────────────────────────┬────────────────────────────────────┘
                          │
                    ┌─────▼─────┐
                    │   Nginx   │ (Reverse Proxy + SSL)
                    └─────┬─────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
  ┌─────▼─────┐    ┌─────▼─────┐    ┌─────▼─────┐
  │  Frontend │    │  Backend  │    │  Telegram │
  │  (React)  │    │ (FastAPI) │    │    Bot    │
  └───────────┘    └─────┬─────┘    └───────────┘
                         │
      ┌──────────────────┼──────────────────┐
      │                  │                  │
┌─────▼─────┐    ┌──────▼──────┐    ┌─────▼─────┐
│   MySQL   │    │    Redis    │    │  Celery   │
│  (Data)   │    │   (Cache)   │    │ (Workers) │
└───────────┘    └─────────────┘    └───────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐    ┌────▼────┐    ┌────▼──────┐
    │   LLM   │    │ChromaDB │    │  External │
    │(OpenAI) │    │(Vectors)│    │   APIs    │
    └─────────┘    └─────────┘    └───────────┘
```

## 🎯 Backend Architecture (FastAPI)

### Layered Architecture

```
app/
├── api/                    # API Layer (Controllers)
│   ├── v1/
│   │   ├── auth.py        # POST /auth/login, /auth/register
│   │   ├── clients.py     # CRUD для клиентов
│   │   ├── documents.py   # Загрузка и анализ документов
│   │   ├── chat.py        # AI чат endpoints
│   │   ├── contracts.py   # Генерация договоров
│   │   ├── crm.py         # CRM интеграция
│   │   ├── telegram.py    # Telegram webhooks
│   │   ├── payments.py    # Платежи
│   │   └── analytics.py   # Аналитика
│   └── deps.py            # Dependency injection
│
├── core/                   # Core Configuration
│   ├── config.py          # Settings (env variables)
│   ├── security.py        # JWT, passwords
│   └── database.py        # DB connection
│
├── models/                 # Data Layer (ORM)
│   ├── user.py
│   ├── client.py
│   ├── document.py
│   ├── chat.py
│   ├── contract.py
│   ├── crm.py
│   └── payment.py
│
├── schemas/                # API Schemas (Pydantic)
│   ├── user.py            # UserCreate, UserResponse
│   ├── client.py
│   ├── document.py
│   └── ...
│
├── services/               # Business Logic Layer
│   ├── auth_service.py    # Авторизация
│   ├── ai/
│   │   ├── llm_service.py        # LLM интеграция
│   │   ├── rag_service.py        # RAG pipeline
│   │   ├── document_analyzer.py  # Анализ документов
│   │   └── contract_generator.py # Генерация договоров
│   ├── integrations/
│   │   ├── amocrm_client.py
│   │   ├── bitrix24_client.py
│   │   ├── telegram_client.py
│   │   └── payment_client.py
│   └── notification_service.py
│
├── tasks/                  # Background Tasks (Celery)
│   ├── document_tasks.py  # Асинхронный анализ
│   ├── crm_tasks.py       # Синхронизация с CRM
│   └── notification_tasks.py
│
├── repositories/           # Data Access Layer
│   ├── user_repo.py       # CRUD для users
│   ├── client_repo.py
│   └── ...
│
└── utils/                  # Utilities
    ├── file_handler.py
    ├── validators.py
    └── helpers.py
```

### Request Flow

```
1. HTTP Request → Nginx → FastAPI
2. FastAPI → Route Handler (api/)
3. Route Handler → Dependency Injection (auth, db session)
4. Route Handler → Service Layer (services/)
5. Service Layer → Repository (repositories/)
6. Repository → SQLAlchemy → MySQL
7. Service Layer → External API (если нужно)
8. Response ← Format by Pydantic schema
```

### Example: Document Analysis Flow

```python
# 1. API Endpoint
@router.post("/documents/analyze")
async def analyze_document(
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    analyzer: DocumentAnalyzer = Depends(get_document_analyzer)
):
    # 2. Save file
    file_path = await save_uploaded_file(file)
    
    # 3. Create document record
    document = await document_repo.create(
        db, client_id=current_user.id, file_path=file_path
    )
    
    # 4. Queue analysis task
    task = analyze_document_task.delay(document.id)
    
    # 5. Return task ID
    return {"task_id": task.id, "document_id": document.id}

# 3. Celery Task
@celery_app.task
def analyze_document_task(document_id: int):
    # Extract text
    text = extract_text_from_pdf(document.file_path)
    
    # Analyze with LLM
    analysis = llm_service.analyze_document(text)
    
    # Save results
    document_analysis_repo.create(
        document_id=document_id,
        analysis=analysis
    )
    
# 4. LLM Service
class DocumentAnalyzer:
    async def analyze_document(self, text: str):
        prompt = f"""
        Проанализируй договор и извлеки:
        - Стороны
        - Суммы
        - Сроки
        - Риски
        
        Текст: {text}
        """
        
        response = await openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return parse_analysis(response)
```

## 🎨 Frontend Architecture (React)

### Feature-based Structure

```
src/
├── app/
│   ├── App.tsx            # Root component
│   ├── Router.tsx         # Routes configuration
│   └── providers.tsx      # Context providers
│
├── features/               # Feature modules
│   ├── auth/
│   │   ├── components/    # LoginForm, RegisterForm
│   │   ├── hooks/         # useAuth, useLogin
│   │   ├── api/           # authApi.ts
│   │   └── types/         # auth.types.ts
│   │
│   ├── chat/
│   │   ├── components/
│   │   │   ├── ChatWindow.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageInput.tsx
│   │   │   └── StreamingMessage.tsx
│   │   ├── hooks/
│   │   │   ├── useChat.ts
│   │   │   └── useStreaming.ts
│   │   └── api/
│   │       └── chatApi.ts
│   │
│   ├── documents/
│   │   ├── components/
│   │   │   ├── DocumentUpload.tsx
│   │   │   ├── DocumentList.tsx
│   │   │   ├── AnalysisResult.tsx
│   │   │   └── DocumentViewer.tsx
│   │   ├── hooks/
│   │   │   ├── useDocuments.ts
│   │   │   └── useDocumentAnalysis.ts
│   │   └── api/
│   │       └── documentsApi.ts
│   │
│   ├── contracts/
│   │   ├── components/
│   │   │   ├── TemplateSelector.tsx
│   │   │   ├── ContractForm.tsx
│   │   │   └── ContractPreview.tsx
│   │   └── hooks/
│   │       └── useContractGenerator.ts
│   │
│   └── analytics/
│       ├── components/
│       │   ├── Dashboard.tsx
│       │   ├── StatsCard.tsx
│       │   └── Charts.tsx
│       └── hooks/
│           └── useAnalytics.ts
│
├── shared/                 # Shared code
│   ├── components/        # Reusable components
│   │   ├── ui/           # shadcn/ui components
│   │   ├── Layout.tsx
│   │   ├── Sidebar.tsx
│   │   └── Header.tsx
│   ├── hooks/            # Shared hooks
│   │   ├── useApi.ts
│   │   └── useDebounce.ts
│   ├── lib/              # Utilities
│   │   ├── api-client.ts
│   │   └── utils.ts
│   └── types/            # Shared types
│       └── common.types.ts
│
├── stores/                # State management
│   ├── authStore.ts      # Zustand store
│   └── uiStore.ts
│
└── styles/
    └── globals.css
```

### State Management Strategy

```typescript
// Server State (React Query)
- API данные
- Кеширование
- Auto refetch
- Optimistic updates

// Client State (Zustand)
- UI состояние (sidebar open/closed)
- User preferences (theme, language)
- Temporary form data

// URL State (React Router)
- Filters
- Pagination
- Search params
```

### Example: Chat Component

```typescript
// features/chat/components/ChatWindow.tsx
export const ChatWindow = () => {
  const { messages, sendMessage, isLoading } = useChat()
  const { streamingContent } = useStreaming()
  
  return (
    <div className="flex flex-col h-screen">
      <MessageList messages={messages} />
      {streamingContent && (
        <StreamingMessage content={streamingContent} />
      )}
      <MessageInput onSend={sendMessage} disabled={isLoading} />
    </div>
  )
}

// features/chat/hooks/useChat.ts
export const useChat = () => {
  const queryClient = useQueryClient()
  
  // Fetch messages
  const { data: messages } = useQuery({
    queryKey: ['chat', 'messages'],
    queryFn: () => chatApi.getMessages()
  })
  
  // Send message mutation
  const { mutate: sendMessage } = useMutation({
    mutationFn: chatApi.sendMessage,
    onSuccess: () => {
      queryClient.invalidateQueries(['chat', 'messages'])
    }
  })
  
  return { messages, sendMessage }
}

// features/chat/hooks/useStreaming.ts
export const useStreaming = () => {
  const [content, setContent] = useState('')
  
  useEffect(() => {
    const eventSource = new EventSource('/api/chat/stream')
    
    eventSource.onmessage = (event) => {
      const chunk = JSON.parse(event.data)
      setContent(prev => prev + chunk.content)
    }
    
    return () => eventSource.close()
  }, [])
  
  return { streamingContent: content }
}
```

## 🤖 AI/ML Architecture

### RAG Pipeline

```
1. Ingestion (Загрузка документов в базу знаний)
┌──────────────┐
│   Document   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Text Extract │ (PyPDF2, python-docx)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Chunking   │ (Split by 500 tokens, overlap 50)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Embeddings  │ (OpenAI text-embedding-ada-002)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  ChromaDB    │ (Store vectors)
└──────────────┘

2. Retrieval (Поиск релевантных документов)
┌──────────────┐
│ User Query   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Embedding   │ (OpenAI)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Semantic   │ (ChromaDB similarity search)
│    Search    │ (Top 5 chunks)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Context    │
└──────────────┘

3. Generation (Генерация ответа)
┌──────────────┐
│   Context    │
│      +       │
│ User Query   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    Prompt    │
│  Template    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  LLM (GPT-4) │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Response   │ (with sources)
└──────────────┘
```

### LLM Integration Pattern

```python
class LLMService:
    def __init__(self):
        self.client = OpenAI()
        self.cache = Redis()
    
    async def generate_response(
        self, 
        prompt: str, 
        stream: bool = False
    ):
        # 1. Check cache
        cache_key = f"llm:{hash(prompt)}"
        if cached := await self.cache.get(cache_key):
            return cached
        
        # 2. Call LLM
        if stream:
            return self._stream_response(prompt)
        else:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            # 3. Cache result
            await self.cache.setex(
                cache_key, 3600, response.choices[0].message.content
            )
            
            return response
    
    async def _stream_response(self, prompt: str):
        stream = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        
        async for chunk in stream:
            yield chunk.choices[0].delta.content
```

## 🔗 Интеграции Architecture

### CRM Integration Pattern

```python
# Abstract base
class CRMClient(ABC):
    @abstractmethod
    async def create_lead(self, data: LeadData) -> str:
        pass
    
    @abstractmethod
    async def get_contact(self, contact_id: str) -> Contact:
        pass

# Concrete implementations
class AmoCRMClient(CRMClient):
    def __init__(self, access_token: str, domain: str):
        self.client = aiohttp.ClientSession()
        self.base_url = f"https://{domain}.amocrm.ru/api/v4"
        self.headers = {"Authorization": f"Bearer {access_token}"}
    
    async def create_lead(self, data: LeadData):
        response = await self.client.post(
            f"{self.base_url}/leads",
            json=data.dict(),
            headers=self.headers
        )
        return response.json()["id"]

class Bitrix24Client(CRMClient):
    # Similar implementation
    pass

# Factory
class CRMClientFactory:
    @staticmethod
    def create(provider: str, **kwargs) -> CRMClient:
        if provider == "amocrm":
            return AmoCRMClient(**kwargs)
        elif provider == "bitrix24":
            return Bitrix24Client(**kwargs)
        else:
            raise ValueError(f"Unknown provider: {provider}")

# Usage in service
class CRMService:
    def __init__(self, crm_repo: CRMRepository):
        self.crm_repo = crm_repo
    
    async def create_lead_from_chat(
        self, 
        client_id: int, 
        message: str
    ):
        # Get CRM integration settings
        integration = await self.crm_repo.get_by_client(client_id)
        
        # Create client
        crm_client = CRMClientFactory.create(
            provider=integration.provider,
            access_token=integration.access_token,
            domain=integration.domain
        )
        
        # Create lead
        lead_id = await crm_client.create_lead(
            LeadData(
                name=f"Чат обращение от клиента {client_id}",
                note=message,
                pipeline_id=integration.pipeline_id
            )
        )
        
        return lead_id
```

## 📊 Database Design

### Entity Relationship Diagram

```
users ──────┐
            │
            ├──< clients ──< documents ──< document_analyses
            │       │
            │       ├──< chat_messages
            │       │
            │       ├──< generated_contracts ──> contract_templates
            │       │
            │       ├──< leads ──> crm_integrations ──> users
            │       │
            │       └──< payments
            │
            └──< knowledge_base
```

### Query Optimization Examples

```sql
-- BAD: N+1 problem
SELECT * FROM clients;
foreach client:
    SELECT * FROM documents WHERE client_id = client.id;

-- GOOD: Join + eager loading
SELECT 
    clients.*, 
    documents.*
FROM clients
LEFT JOIN documents ON documents.client_id = clients.id
WHERE clients.user_id = ?;

-- GOOD: With SQLAlchemy
session.query(Client)\
    .options(joinedload(Client.documents))\
    .filter(Client.user_id == user_id)\
    .all()
```

## 🚀 Deployment Architecture

### Development
```
Docker Compose
├── nginx (5173 → frontend, 8000 → backend)
├── frontend (Vite dev server)
├── backend (uvicorn --reload)
├── mysql
├── redis
└── celery worker
```

### Production
```
Server (VPS/Cloud)
├── Nginx
│   ├── SSL (Let's Encrypt)
│   ├── Static files (React build)
│   └── Proxy API (/api → uvicorn)
│
├── Backend (multiple workers)
│   ├── uvicorn worker 1 (port 8001)
│   ├── uvicorn worker 2 (port 8002)
│   └── uvicorn worker N (port 800N)
│
├── Celery
│   ├── Worker pool (4 workers)
│   └── Beat scheduler
│
├── MySQL
│   ├── Primary (write)
│   └── Replica (read) - optional
│
└── Redis
    ├── Cache
    └── Celery broker
```

## 📈 Monitoring Architecture

```
Application Metrics (Prometheus)
├── HTTP requests (count, duration, errors)
├── LLM calls (count, duration, tokens, cost)
├── Database queries (count, duration)
├── Cache hit/miss ratio
└── Celery tasks (count, duration, failures)

Visualization (Grafana)
├── Main dashboard
│   ├── Request rate
│   ├── Error rate
│   ├── Response time (p50, p95, p99)
│   └── Active users
│
├── AI dashboard
│   ├── LLM calls per hour
│   ├── Average response time
│   ├── Token usage
│   └── Cost per day
│
└── Infrastructure dashboard
    ├── CPU/Memory usage
    ├── Disk I/O
    ├── Network traffic
    └── Database connections
```

---

**Архитектура демонстрирует:**
- ✅ Слоистую архитектуру (Layered Architecture)
- ✅ Разделение ответственности (Separation of Concerns)
- ✅ SOLID принципы
- ✅ Масштабируемость
- ✅ Testability
- ✅ Production-ready patterns

**Готово к реализации!** 🏗️

