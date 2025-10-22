# Тестирование LegalFlow AI

## 📊 Обзор

Проект содержит комплексный набор тестов для демонстрации профессионального подхода к тестированию.

### ✅ Результаты тестирования

```
======================== 13 passed, 1 warning =========================
```

**Coverage: 51%** - отличное покрытие для демонстрационного проекта

---

## 🧪 Типы тестов

### 1. Security Tests (`tests/services/test_security.py`)
Тестирование функций безопасности:
- ✅ Хеширование паролей (bcrypt)
- ✅ Проверка паролей
- ✅ Создание JWT access токенов
- ✅ Создание JWT refresh токенов
- ✅ Декодирование токенов
- ✅ Обработка невалидных токенов

### 2. Model Tests (`tests/models/`)
Тестирование моделей данных:
- ✅ `test_user.py` - создание пользователей, уникальность email
- ✅ `test_document.py` - создание документов, типы документов

### 3. Service Tests (`tests/services/`)
Тестирование бизнес-логики:
- ✅ `test_llm_service.py` - LLM сервис, получение списка моделей
- ✅ `test_document_processor.py` - определение типа файлов, извлечение текста

---

## 🚀 Запуск тестов

### Запуск всех тестов
```bash
cd backend
python -m pytest tests/ -v
```

### С coverage отчетом
```bash
python -m pytest tests/ --cov=app --cov-report=html
```

### Запуск конкретного теста
```bash
python -m pytest tests/services/test_security.py::test_password_hashing -v
```

---

## 📈 Coverage Report

После запуска тестов с coverage, отчет доступен в:
```
backend/htmlcov/index.html
```

Откройте в браузере:
```bash
open htmlcov/index.html
```

---

## 🏗️ Структура тестов

```
tests/
├── conftest.py                    # Pytest fixtures
├── README.md                      # Эта документация
├── models/                        # Тесты моделей
│   ├── test_user.py
│   └── test_document.py
└── services/                      # Тесты сервисов
    ├── test_security.py
    ├── test_llm_service.py
    └── test_document_processor.py
```

---

## 🔧 Fixtures

Основные fixtures в `conftest.py`:

- `db_engine` - тестовая база данных (SQLite)
- `db` - сессия базы данных
- `test_user` - тестовый пользователь
- `auth_headers` - заголовки аутентификации с JWT

---

## 🎯 Что демонстрирует этот test suite

### Профессиональные практики:
1. ✅ **Unit тесты** - изолированное тестирование функций
2. ✅ **Integration тесты** - тестирование моделей с БД
3. ✅ **Fixtures** - переиспользуемые тестовые данные
4. ✅ **Mocking** - изоляция внешних зависимостей
5. ✅ **Coverage** - отслеживание покрытия кода
6. ✅ **Изоляция** - каждый тест независим
7. ✅ **Документация** - понятная структура и описание

### Технологии:
- `pytest` - современный тестовый фреймворк
- `pytest-cov` - coverage reporting
- `pytest-asyncio` - поддержка async тестов
- `faker` - генерация тестовых данных
- SQLite для тестовой БД

---

## 📝 Примеры

### Пример unit теста
```python
def test_password_hashing():
    """Test password hashing"""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
```

### Пример теста с БД
```python
def test_create_user(db):
    """Test user model creation"""
    user = User(
        email="test@example.com",
        full_name="Test User",
        is_active=True
    )
    user.password_hash = get_password_hash("password")
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    assert user.id is not None
    assert user.email == "test@example.com"
```

---

## 🐛 Troubleshooting

### Проблема: ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Проблема: Database locked
Удалите тестовую БД:
```bash
rm test.db
```

### Проблема: Permission denied
Используйте `--user` flag:
```bash
pip install --user pytest
```

---

## 📚 Дополнительные ресурсы

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Real Python Testing Guide](https://realpython.com/pytest-python-testing/)

---

## 🎓 Для работодателя

Этот test suite демонстрирует:

✅ Понимание важности тестирования  
✅ Знание современных инструментов (pytest, coverage)  
✅ Умение писать изолированные, читаемые тесты  
✅ Опыт работы с fixtures и mocking  
✅ Профессиональный подход к качеству кода  

**51% coverage** - отличный показатель для демонстрационного проекта, покрывающий критические компоненты:
- Security (97%)
- Core Config (98%)
- Models (100%)
- Schemas (100%)

---

**Автор**: Юрий Шульдешов ([@shuldeshoff](https://t.me/shuldeshoff))  
**Проект**: LegalFlow AI  
**GitHub**: https://github.com/shuldeshoff/legalflow-ai
