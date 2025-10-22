# 🚀 Git Setup Commands

## Первоначальная настройка и push

```bash
# 1. Инициализировать git репозиторий
cd /Users/sul/LLM
git init

# 2. Добавить все файлы
git add .

# 3. Создать первый коммит
git commit -m "Initial commit: LegalFlow AI - AI-powered legal automation platform

- Project documentation (README, plan, architecture, tech stack)
- Python FastAPI + React + MySQL stack
- AI/ML modules (LLM, RAG, document analysis)
- CRM, messenger, and payment integrations
- Full-stack demo project for portfolio"

# 4. Добавить remote origin
git remote add origin https://github.com/shuldeshoff/legalflow-ai.git

# 5. Переименовать ветку в main
git branch -M main

# 6. Push в GitHub
git push -u origin main
```

## Дальнейшая работа

```bash
# Проверить статус
git status

# Добавить изменения
git add .

# Коммит
git commit -m "Update: описание изменений"

# Push
git push origin main
```

## Git игнорирование

Создать `.gitignore`:
```bash
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
*.egg-info/

# Node
node_modules/
npm-debug.log*
.env.local

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.production

# Logs
*.log

# Database
*.sqlite
*.db

# Build
dist/
build/
.next/
```

## Полезные команды

```bash
# Просмотр истории
git log --oneline --graph

# Просмотр изменений
git diff

# Создать новую ветку для фичи
git checkout -b feature/название-фичи

# Вернуться на main
git checkout main

# Слить фичу
git merge feature/название-фичи

# Создать тег (версия)
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## GitHub настройки

### Описание репозитория (About)
```
AI-powered legal automation platform | Python FastAPI + React + MySQL | LLM integration, RAG, document analysis, CRM connectors
```

### Website
```
https://github.com/shuldeshoff/legalflow-ai
```

### Topics (теги)
```
ai
artificial-intelligence
llm
fastapi
python
react
typescript
mysql
langchain
openai
gpt-4
rag
nlp
legal-tech
legaltech
crm-integration
telegram-bot
document-analysis
fullstack
asyncio
sqlalchemy
automation
```

## Рекомендации

1. **Commit Messages:** Используйте Conventional Commits
   - `feat:` - новая функция
   - `fix:` - исправление бага
   - `docs:` - обновление документации
   - `refactor:` - рефакторинг кода
   - `test:` - добавление тестов

2. **Branching Strategy:**
   - `main` - production ready код
   - `develop` - разработка (опционально)
   - `feature/*` - новые фичи
   - `bugfix/*` - исправления

3. **README Updates:** Всегда обновлять README при добавлении новых фич

4. **Changelog:** Вести CHANGELOG.md для истории изменений

