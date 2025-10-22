# 🎯 Руководство по деплою в продакшн

## Подготовка к деплою

### 1. Сервер

Минимальные требования:
- **OS**: Ubuntu 20.04+ / Debian 11+
- **CPU**: 2 cores
- **RAM**: 4 GB
- **Disk**: 50 GB SSD
- **Docker**: 20.10+
- **Docker Compose**: 2.0+

### 2. Домен и SSL

```bash
# Установка Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Получение SSL сертификата
sudo certbot --nginx -d legalflow.ai -d www.legalflow.ai
```

### 3. Настройка окружения

Создайте `.env` файл:

```bash
# Сгенерируйте секретный ключ
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Создайте .env
cat > .env << EOF
DEBUG=False
SECRET_KEY=<ваш-секретный-ключ>

DATABASE_USER=legalflow
DATABASE_PASSWORD=<сильный-пароль>
DATABASE_NAME=legalflow_db
MYSQL_ROOT_PASSWORD=<сильный-пароль>

OPENAI_API_KEY=<ваш-ключ>
YANDEX_GPT_API_KEY=<ваш-ключ>
YANDEX_FOLDER_ID=<ваш-folder>

TELEGRAM_BOT_TOKEN=<ваш-токен>
YOOKASSA_SHOP_ID=<ваш-shop-id>
YOOKASSA_SECRET_KEY=<ваш-ключ>

VITE_API_URL=https://legalflow.ai/api/v1
EOF
```

## Production Docker Compose

Создайте `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    restart: always
    environment:
      - DEBUG=False
      - DATABASE_HOST=mysql
      - REDIS_HOST=redis
    env_file:
      - .env
    volumes:
      - uploads:/app/uploads
      - chroma_data:/app/chroma_data
    depends_on:
      - mysql
      - redis
    networks:
      - legalflow_network
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        - VITE_API_URL=${VITE_API_URL}
    restart: always
    networks:
      - legalflow_network

  mysql:
    image: mysql:8.0
    restart: always
    env_file:
      - .env
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - legalflow_network
    command: --default-authentication-plugin=mysql_native_password

  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis_data:/data
    networks:
      - legalflow_network

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - /etc/letsencrypt:/etc/letsencrypt
    depends_on:
      - backend
      - frontend
    networks:
      - legalflow_network

volumes:
  mysql_data:
  redis_data:
  uploads:
  chroma_data:

networks:
  legalflow_network:
    driver: bridge
```

## Nginx конфигурация

Создайте `nginx/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:80;
    }

    # HTTP -> HTTPS redirect
    server {
        listen 80;
        server_name legalflow.ai www.legalflow.ai;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS
    server {
        listen 443 ssl http2;
        server_name legalflow.ai www.legalflow.ai;

        ssl_certificate /etc/letsencrypt/live/legalflow.ai/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/legalflow.ai/privkey.pem;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        client_max_body_size 100M;

        # Backend API
        location /api {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

## Production Frontend Dockerfile

Создайте `frontend/Dockerfile`:

```dockerfile
# Build stage
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci --production=false

COPY . .
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Деплой процесс

### 1. Клонирование на сервер

```bash
# SSH на сервер
ssh user@your-server.com

# Клонирование репозитория
git clone https://github.com/shuldeshoff/legalflow-ai.git
cd legalflow-ai
```

### 2. Настройка переменных окружения

```bash
# Скопируйте example и заполните
cp .env.example .env
nano .env
```

### 3. Запуск в продакшн

```bash
# Build и запуск
docker-compose -f docker-compose.prod.yml up -d --build

# Применение миграций
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Проверка логов
docker-compose -f docker-compose.prod.yml logs -f
```

### 4. Создание первого пользователя

```bash
curl -X POST https://legalflow.ai/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@legalflow.ai",
    "password": "SecurePassword123!"
  }'
```

## Обновление приложения

```bash
# Pull последних изменений
git pull origin main

# Перезапуск сервисов
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build

# Применение новых миграций
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

## Backup

### База данных

```bash
# Backup
docker-compose -f docker-compose.prod.yml exec mysql mysqldump \
  -u legalflow -p legalflow_db > backup_$(date +%Y%m%d).sql

# Restore
docker-compose -f docker-compose.prod.yml exec -T mysql mysql \
  -u legalflow -p legalflow_db < backup_20251022.sql
```

### Файлы

```bash
# Backup uploads и vector DB
tar -czf backup_files_$(date +%Y%m%d).tar.gz \
  $(docker volume inspect legalflow_uploads -f '{{.Mountpoint}}') \
  $(docker volume inspect legalflow_chroma_data -f '{{.Mountpoint}}')
```

## Мониторинг

### Health Checks

```bash
# Backend health
curl https://legalflow.ai/health

# Проверка всех сервисов
docker-compose -f docker-compose.prod.yml ps
```

### Логирование

```bash
# Все логи
docker-compose -f docker-compose.prod.yml logs -f

# Только backend
docker-compose -f docker-compose.prod.yml logs -f backend

# Последние 100 строк
docker-compose -f docker-compose.prod.yml logs --tail=100 backend
```

## Безопасность

### Firewall

```bash
# UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Fail2Ban

```bash
# Установка
sudo apt-get install fail2ban

# Конфигурация для SSH
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Обновления системы

```bash
# Автоматические обновления безопасности
sudo apt-get install unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

## Troubleshooting

### Проблемы с контейнерами

```bash
# Перезапуск всех сервисов
docker-compose -f docker-compose.prod.yml restart

# Пересборка с нуля
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build
```

### Проблемы с SSL

```bash
# Обновление сертификатов
sudo certbot renew

# Проверка статуса
sudo certbot certificates
```

### Проблемы с базой данных

```bash
# Вход в MySQL
docker-compose -f docker-compose.prod.yml exec mysql mysql -u legalflow -p

# Проверка таблиц
SHOW TABLES;
```

## Производительность

### Масштабирование Backend

В `docker-compose.prod.yml`:

```yaml
backend:
  deploy:
    replicas: 3
```

### Кэширование Redis

Настроено автоматически для:
- LLM ответов
- Данных сессий

### Оптимизация MySQL

```sql
-- Индексы для основных запросов
CREATE INDEX idx_documents_status ON documents(analysis_status);
CREATE INDEX idx_documents_user ON documents(uploaded_by);
CREATE INDEX idx_knowledge_category ON knowledge_base(category);
```

---

**Поддержка**: [@shuldeshoff](https://t.me/shuldeshoff)

