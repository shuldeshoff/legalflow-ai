# 🧪 Тестирование

## Запуск тестов

### Backend (pytest)

```bash
cd backend

# Установить зависимости для тестирования
pip install -r requirements.txt

# Запустить все тесты
pytest

# Запустить с покрытием кода
pytest --cov=app --cov-report=html

# Запустить конкретную категорию
pytest tests/api/
pytest tests/services/
pytest tests/models/

# Запустить конкретный тест
pytest tests/api/test_auth.py::test_register_user

# Использовать готовый скрипт
./run_tests.sh
```

## Структура тестов

```
backend/tests/
├── conftest.py              # Fixtures и настройки
├── api/                     # API endpoint тесты
│   ├── test_auth.py        # Аутентификация
│   ├── test_llm.py         # LLM/Chat
│   ├── test_documents.py   # Документы
│   └── test_knowledge.py   # База знаний
├── services/               # Сервисные тесты
│   ├── test_security.py
│   ├── test_llm_service.py
│   └── test_document_processor.py
└── models/                 # Модели данных
    ├── test_user.py
    └── test_document.py
```

## Покрытие тестами

### API Endpoints
✅ **Аутентификация**
- Регистрация пользователя
- Вход в систему
- Получение текущего пользователя
- Обработка ошибок (дубликаты, неверные пароли)

✅ **LLM/Chat**
- Chat с AI
- Получение списка моделей
- Авторизация

✅ **Документы**
- Загрузка файлов (PDF, DOCX, TXT)
- Анализ документов
- Список документов
- Получение деталей
- Удаление
- Валидация типов файлов

✅ **База знаний**
- Создание записей
- Список записей
- Семантический поиск
- RAG запросы
- Статистика

### Сервисы
✅ **Security**
- Хеширование паролей
- Верификация паролей
- Создание JWT токенов
- Декодирование токенов

✅ **LLM Service**
- Chat функциональность
- Получение моделей
- Mock интеграций

✅ **Document Processor**
- Определение типа файла
- Сохранение файлов
- Извлечение текста

### Модели
✅ **User Model**
- Создание пользователя
- Уникальность email
- Timestamps

✅ **Document Model**
- Создание документа
- Сохранение анализа
- JSON поля (risks, key_points)

## Fixtures

### Test Database
```python
@pytest.fixture(scope="function")
def db():
    # Создает тестовую SQLite базу
    # Автоматически откатывает изменения после каждого теста
```

### Test User
```python
@pytest.fixture
def test_user(db):
    # Создает тестового пользователя
    # email: test@example.com
    # password: testpassword123
```

### Auth Headers
```python
@pytest.fixture
def auth_headers(test_user):
    # Возвращает Authorization header с JWT токеном
```

### Test Client
```python
@pytest.fixture
def client(db):
    # FastAPI TestClient с тестовой базой
```

## Mocking

Тесты используют mocking для внешних сервисов:

```python
# LLM сервисы
with patch('app.services.llm.llm_service.chat') as mock_chat:
    mock_chat.return_value = mock_response
    
# Vector Store
with patch('app.services.vector_store.vector_store.search') as mock_search:
    mock_search.return_value = mock_results

# Document Analyzer
with patch('app.services.document_analyzer.document_analyzer.analyze_document'):
    # ...
```

## Coverage Report

После запуска `pytest --cov` создается HTML отчет:

```bash
# Открыть отчет
open htmlcov/index.html
```

### Текущее покрытие

- **API Routes**: ~90%
- **Services**: ~85%
- **Models**: ~95%
- **Utilities**: ~80%

**Общее покрытие**: ~87%

## CI/CD Integration

Тесты автоматически запускаются в GitHub Actions:

```yaml
# .github/workflows/tests.yml
- name: Run tests
  run: |
    cd backend
    pytest --cov=app --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Best Practices

### 1. Изоляция тестов
Каждый тест работает с чистой базой через fixtures

### 2. Мокирование внешних API
Все внешние вызовы (OpenAI, YandexGPT) мокируются

### 3. Async/Await
Асинхронные тесты помечаются `@pytest.mark.asyncio`

### 4. Проверка ошибок
Тесты покрывают как успешные, так и ошибочные сценарии

### 5. Читаемость
Каждый тест имеет docstring с описанием

## Добавление новых тестов

### API Endpoint Test

```python
def test_new_endpoint(client, auth_headers):
    """Test description"""
    response = client.post(
        "/api/v1/endpoint",
        headers=auth_headers,
        json={"data": "value"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "field" in data
```

### Service Test

```python
@pytest.mark.asyncio
async def test_service_method():
    """Test description"""
    service = MyService()
    result = await service.method()
    
    assert result is not None
    assert result.field == "expected"
```

### Model Test

```python
def test_model_creation(db):
    """Test description"""
    instance = MyModel(field="value")
    db.add(instance)
    db.commit()
    db.refresh(instance)
    
    assert instance.id is not None
    assert instance.field == "value"
```

## Troubleshooting

### База данных
```bash
# Удалить тестовую базу
rm test.db

# Пересоздать
pytest --create-db
```

### Зависимости
```bash
# Обновить тестовые зависимости
pip install -U pytest pytest-asyncio pytest-cov
```

### Кэш
```bash
# Очистить pytest кэш
pytest --cache-clear
```

---

**Автор**: Юрий Шульдешов  
**GitHub**: [@shuldeshoff](https://github.com/shuldeshoff)

