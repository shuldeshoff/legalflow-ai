# 📚 API Документация LegalFlow AI

## Базовая информация

- **Base URL**: `http://localhost:8000/api/v1`
- **Аутентификация**: JWT Bearer Token
- **Content-Type**: `application/json`

## Аутентификация

### Регистрация пользователя

```http
POST /api/v1/auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2025-10-22T12:00:00"
}
```

### Вход

```http
POST /api/v1/auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Получить текущего пользователя

```http
GET /api/v1/auth/me
Authorization: Bearer {token}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2025-10-22T12:00:00"
}
```

## LLM / AI Консультант

### Chat с AI

```http
POST /api/v1/llm/chat
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "messages": [
    {
      "role": "system",
      "content": "Ты профессиональный юридический консультант"
    },
    {
      "role": "user",
      "content": "Какие документы нужны для регистрации ООО?"
    }
  ],
  "model": "gpt-3.5-turbo",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

**Response:** `200 OK`
```json
{
  "content": "Для регистрации ООО необходимы следующие документы...",
  "model": "gpt-3.5-turbo",
  "usage": {
    "prompt_tokens": 45,
    "completion_tokens": 120,
    "total_tokens": 165
  }
}
```

### Streaming Chat

```http
POST /api/v1/llm/chat/stream
Authorization: Bearer {token}
```

**Request Body:** (аналогично `/chat`)

**Response:** `200 OK` (Server-Sent Events)
```
data: {"content": "Для", "done": false}
data: {"content": " регистрации", "done": false}
data: {"content": " ООО", "done": false}
...
data: {"done": true}
```

### Список доступных моделей

```http
GET /api/v1/llm/models
Authorization: Bearer {token}
```

**Response:** `200 OK`
```json
{
  "models": [
    {
      "id": "gpt-4-turbo-preview",
      "name": "GPT-4 Turbo",
      "provider": "openai"
    },
    {
      "id": "gpt-3.5-turbo",
      "name": "GPT-3.5 Turbo",
      "provider": "openai"
    },
    {
      "id": "yandexgpt",
      "name": "YandexGPT",
      "provider": "yandex"
    }
  ]
}
```

## Документы

### Загрузка документа

```http
POST /api/v1/documents/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**Request:**
- `file`: File (PDF, DOCX, TXT)
- `client_id`: Integer (optional)

**Response:** `201 Created`
```json
{
  "id": 1,
  "title": "contract.pdf",
  "file_path": "/uploads/abc123_contract.pdf",
  "file_type": "pdf",
  "file_size": 245678,
  "uploaded_at": "2025-10-22T12:00:00",
  "analysis_status": "pending"
}
```

### Анализ документа

```http
POST /api/v1/documents/{id}/analyze
Authorization: Bearer {token}
```

**Query Parameters:**
- `analyze_risks` (boolean, default: true)
- `analyze_key_points` (boolean, default: true)
- `generate_summary` (boolean, default: true)

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "contract.pdf",
  "analysis_status": "completed",
  "analysis_summary": "Договор купли-продажи недвижимости...",
  "key_points": [
    "Стоимость объекта: 5 000 000 руб.",
    "Срок передачи: 30 дней",
    "Штрафные санкции: 0.1% за день просрочки"
  ],
  "risks": [
    {
      "type": "Юридический риск",
      "description": "Не указан порядок разрешения споров",
      "severity": "medium",
      "recommendation": "Добавить арбитражную оговорку"
    }
  ],
  "recommendations": "Рекомендуется уточнить...",
  "analyzed_at": "2025-10-22T12:05:00"
}
```

### Список документов

```http
GET /api/v1/documents/
Authorization: Bearer {token}
```

**Query Parameters:**
- `skip` (integer, default: 0)
- `limit` (integer, default: 20)
- `client_id` (integer, optional)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "contract.pdf",
    "file_type": "pdf",
    "file_size": 245678,
    "uploaded_at": "2025-10-22T12:00:00",
    "analysis_status": "completed"
  }
]
```

### Детали документа

```http
GET /api/v1/documents/{id}
Authorization: Bearer {token}
```

**Response:** `200 OK` (см. ответ `/analyze`)

### Удаление документа

```http
DELETE /api/v1/documents/{id}
Authorization: Bearer {token}
```

**Response:** `204 No Content`

## База знаний

### Создание записи (Admin)

```http
POST /api/v1/knowledge/
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "title": "Гражданский кодекс РФ - Статья 123",
  "content": "Полный текст статьи...",
  "category": "гражданское_право",
  "source": "ГК РФ"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "title": "Гражданский кодекс РФ - Статья 123",
  "content": "Полный текст статьи...",
  "category": "гражданское_право",
  "source": "ГК РФ",
  "embedding_id": "abc123def456",
  "created_at": "2025-10-22T12:00:00",
  "updated_at": "2025-10-22T12:00:00"
}
```

### Список записей

```http
GET /api/v1/knowledge/
Authorization: Bearer {token}
```

**Query Parameters:**
- `skip` (integer, default: 0)
- `limit` (integer, default: 20)
- `category` (string, optional)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "Гражданский кодекс РФ - Статья 123",
    "content": "Полный текст статьи...",
    "category": "гражданское_право",
    "source": "ГК РФ",
    "created_at": "2025-10-22T12:00:00"
  }
]
```

### Семантический поиск

```http
POST /api/v1/knowledge/search
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "query": "ответственность директора ООО",
  "limit": 5,
  "category": "корпоративное_право"
}
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "ФЗ об ООО - Статья 44",
    "content": "Директор несет ответственность...",
    "category": "корпоративное_право",
    "score": 0.92
  }
]
```

### RAG запрос

```http
POST /api/v1/knowledge/rag
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "query": "Какая ответственность у директора ООО?",
  "limit": 3,
  "category": "корпоративное_право"
}
```

**Response:** `200 OK`
```json
{
  "answer": "Директор ООО несет ответственность перед обществом...",
  "sources": [
    {
      "id": "doc123",
      "title": "ФЗ об ООО - Статья 44",
      "score": 0.92,
      "category": "корпоративное_право"
    }
  ],
  "model": "gpt-3.5-turbo",
  "usage": {
    "prompt_tokens": 450,
    "completion_tokens": 180,
    "total_tokens": 630
  }
}
```

### Статистика базы знаний

```http
GET /api/v1/knowledge/stats/summary
Authorization: Bearer {token}
```

**Response:** `200 OK`
```json
{
  "total_documents": 156,
  "categories": {
    "гражданское_право": 45,
    "корпоративное_право": 32,
    "трудовое_право": 28
  },
  "vector_store": {
    "total_documents": 156,
    "collection_name": "legal_knowledge"
  }
}
```

## Интеграции

### Создание интеграции (Admin)

```http
POST /api/v1/integrations/
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "name": "AmoCRM Integration",
  "type": "crm",
  "is_active": true,
  "config": {
    "api_url": "https://example.amocrm.ru",
    "access_token": "token123"
  }
}
```

**Response:** `201 Created`

### Webhook handler

```http
POST /api/v1/integrations/webhook/{integration_id}
```

**Request Body:** (любой JSON)

**Response:** `200 OK`
```json
{
  "status": "success",
  "message": "Webhook received",
  "integration_id": 1
}
```

## Платежи

### Создание платежа

```http
POST /api/v1/payments/create
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "amount": 100000,
  "currency": "RUB",
  "description": "Консультация юриста",
  "client_id": 5,
  "return_url": "https://legalflow.ai/payment/success"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "user_id": 1,
  "amount": 100000,
  "currency": "RUB",
  "status": "pending",
  "payment_system": "yookassa",
  "payment_id": "2a8b4c6d-1234-5678",
  "payment_url": "https://yookassa.ru/checkout/...",
  "description": "Консультация юриста",
  "created_at": "2025-10-22T12:00:00"
}
```

### Проверка статуса платежа

```http
POST /api/v1/payments/{id}/check
Authorization: Bearer {token}
```

**Response:** `200 OK`
```json
{
  "payment_id": 1,
  "status": "succeeded",
  "amount": 100000,
  "currency": "RUB",
  "payment_url": "https://yookassa.ru/checkout/..."
}
```

## Коды ошибок

| Код | Описание |
|-----|----------|
| 200 | OK - Успешный запрос |
| 201 | Created - Ресурс создан |
| 204 | No Content - Успешно, нет контента |
| 400 | Bad Request - Неверный запрос |
| 401 | Unauthorized - Не авторизован |
| 403 | Forbidden - Доступ запрещен |
| 404 | Not Found - Не найдено |
| 422 | Unprocessable Entity - Ошибка валидации |
| 500 | Internal Server Error - Внутренняя ошибка |

## Rate Limiting

- 100 запросов/минуту для аутентифицированных пользователей
- 10 запросов/минуту для неаутентифицированных

---

**Интерактивная документация**: http://localhost:8000/docs

