# 🚀 Руководство по установке и запуску LegalFlow AI

## Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- Redis 7+

## Вариант 1: Docker Compose (рекомендуется)

### 1. Клонирование репозитория

```bash
git clone https://github.com/shuldeshoff/legalflow-ai.git
cd legalflow-ai
```

### 2. Настройка переменных окружения

Создайте `.env` файл в корне проекта:

```bash
# Backend
DATABASE_HOST=mysql
DATABASE_PORT=3306
DATABASE_USER=legalflow
DATABASE_PASSWORD=legalflow_password
DATABASE_NAME=legalflow_db

REDIS_HOST=redis
REDIS_PORT=6379

SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI/LLM
OPENAI_API_KEY=your-openai-api-key
YANDEX_GPT_API_KEY=your-yandex-api-key
YANDEX_FOLDER_ID=your-yandex-folder-id

# Integrations
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
YOOKASSA_SHOP_ID=your-yookassa-shop-id
YOOKASSA_SECRET_KEY=your-yookassa-secret-key

# Frontend
VITE_API_URL=http://localhost:8000/api/v1
```

### 3. Запуск всех сервисов

```bash
docker-compose up -d
```

Это запустит:
- **Backend** (FastAPI): http://localhost:8000
- **Frontend** (React): http://localhost:5173
- **MySQL**: localhost:3306
- **Redis**: localhost:6379

### 4. Применение миграций

```bash
docker-compose exec backend alembic upgrade head
```

### 5. Создание первого пользователя

```bash
# Через API
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@legalflow.ai",
    "password": "SecurePassword123!"
  }'
```

### 6. Доступ к приложению

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Swagger UI**: http://localhost:8000/redoc

## Вариант 2: Локальная разработка

### Backend

```bash
cd backend

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Настроить .env файл
cp .env.example .env
# Отредактируйте .env

# Применить миграции
alembic upgrade head

# Запустить сервер
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend

# Установить зависимости
npm install

# Создать .env файл
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env

# Запустить dev-сервер
npm run dev
```

## Структура проекта

```
legalflow-ai/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   │   └── v1/
│   │   │       ├── auth.py
│   │   │       ├── llm.py
│   │   │       ├── documents.py
│   │   │       ├── knowledge.py
│   │   │       ├── integrations.py
│   │   │       └── payments.py
│   │   ├── core/              # Конфигурация
│   │   ├── models/            # SQLAlchemy модели
│   │   ├── schemas/           # Pydantic схемы
│   │   └── services/          # Бизнес-логика
│   │       ├── llm/           # LLM провайдеры
│   │       ├── vector_store.py
│   │       ├── rag_service.py
│   │       ├── document_processor.py
│   │       ├── document_analyzer.py
│   │       ├── telegram_bot.py
│   │       └── payment_service.py
│   ├── alembic/               # Миграции БД
│   └── requirements.txt
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── pages/             # Страницы
│   │   ├── services/          # API клиенты
│   │   ├── stores/            # Zustand stores
│   │   └── hooks/             # React hooks
│   └── package.json
├── docs/                       # Документация
├── docker-compose.yml
└── README.md
```

## API Endpoints

### Аутентификация
- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Вход
- `GET /api/v1/auth/me` - Текущий пользователь

### LLM
- `POST /api/v1/llm/chat` - Chat с AI
- `POST /api/v1/llm/chat/stream` - Streaming chat
- `GET /api/v1/llm/models` - Список моделей

### Документы
- `POST /api/v1/documents/upload` - Загрузка документа
- `POST /api/v1/documents/{id}/analyze` - AI-анализ
- `GET /api/v1/documents/` - Список документов
- `GET /api/v1/documents/{id}` - Детали документа
- `DELETE /api/v1/documents/{id}` - Удаление

### База знаний
- `POST /api/v1/knowledge/` - Создать запись
- `GET /api/v1/knowledge/` - Список записей
- `POST /api/v1/knowledge/search` - Поиск
- `POST /api/v1/knowledge/rag` - RAG запрос
- `GET /api/v1/knowledge/stats/summary` - Статистика

### Интеграции
- `POST /api/v1/integrations/` - Создать интеграцию
- `GET /api/v1/integrations/` - Список интеграций
- `POST /api/v1/integrations/webhook/{id}` - Webhook

### Платежи
- `POST /api/v1/payments/create` - Создать платеж
- `GET /api/v1/payments/` - Список платежей
- `POST /api/v1/payments/webhook/yookassa` - Webhook YooKassa

## Конфигурация AI моделей

### OpenAI
```env
OPENAI_API_KEY=sk-...
```

Доступные модели:
- gpt-4-turbo-preview
- gpt-4
- gpt-3.5-turbo

### Yandex GPT
```env
YANDEX_GPT_API_KEY=your-api-key
YANDEX_FOLDER_ID=your-folder-id
```

Доступные модели:
- yandexgpt
- yandexgpt-lite

## Конфигурация интеграций

### Telegram Bot
```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
```

### YooKassa (Платежи)
```env
YOOKASSA_SHOP_ID=123456
YOOKASSA_SECRET_KEY=live_...
```

## Тестирование

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm test
```

## Мониторинг

### Логи Docker
```bash
# Все сервисы
docker-compose logs -f

# Только backend
docker-compose logs -f backend

# Только frontend
docker-compose logs -f frontend
```

### Health Check
```bash
curl http://localhost:8000/health
```

## Troubleshooting

### База данных не подключается
```bash
# Проверить статус MySQL
docker-compose ps mysql

# Перезапустить MySQL
docker-compose restart mysql

# Проверить логи
docker-compose logs mysql
```

### Frontend не подключается к Backend
- Проверьте CORS настройки в `backend/app/core/config.py`
- Убедитесь что `VITE_API_URL` правильно настроен

### Ошибки миграций
```bash
# Откатить миграции
docker-compose exec backend alembic downgrade -1

# Применить заново
docker-compose exec backend alembic upgrade head
```

## Продакшн деплой

### 1. Обновите переменные окружения

```env
DEBUG=False
SECRET_KEY=<generate-strong-key>
DATABASE_PASSWORD=<strong-password>
```

### 2. Используйте production docker-compose

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 3. Настройте reverse proxy (Nginx)

```nginx
server {
    listen 80;
    server_name legalflow.ai;

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
    }
}
```

### 4. SSL сертификаты

```bash
certbot --nginx -d legalflow.ai
```

## Поддержка

- **GitHub**: https://github.com/shuldeshoff/legalflow-ai
- **Issues**: https://github.com/shuldeshoff/legalflow-ai/issues
- **Telegram**: [@shuldeshoff](https://t.me/shuldeshoff)

## Лицензия

MIT License - см. LICENSE файл

---

**Автор**: Юрий Шульдешов  
**GitHub**: [@shuldeshoff](https://github.com/shuldeshoff)  
**Telegram**: [@shuldeshoff](https://t.me/shuldeshoff)

