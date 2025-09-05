# Pomodoro Timer API

## 📋 О проекте

API для управления техникой Pomodoro. Позволяет создавать задачи, запускать таймеры, ставить на паузу, пропускать этапы и отслеживать прогресс

## 🚀 Возможности

- ✅ Создание и управление задачами
- ✅ Запуск/пауза/сброс таймеров Pomodoro
- ✅ Настройка длительности работы и перерывов
- ✅ Отслеживание прогресса выполнения задач
- ✅ Уведомления по email о регистрации
- ✅ Аутентификация и авторизация пользователей, через Google + Yandex
- ✅ Работа с Redis для хранения состояния таймеров и задач
- ✅ Обработка задач с Celery и RabbitMQ

## 🛠️ Технологии

- **FastAPI** - веб-фреймворк
- **PostgreSQL** - база данных
- **Redis** - кэширование и хранение состояния таймеров и задач
- **Celery** - асинхронные задачи
- **RabbitMQ** - брокер сообщений
- **SQLAlchemy** - ORM
- **Pydantic** - валидация данных
- **JWT** - аутентификация
- **Docker** - контейнеризация

## 📦 Установка и запуск

### Предварительные требования

- Docker и Docker Compose
- Python 3.8+

### 1. Клонирование репозитория

```bash
git clone https://github.com/Birobizhan/pomodoro.git
```

### 2. Настройка окружения

Измените файл .prod.env в корневой папке по примеру который там уже есть:

```.prod.env
DB_URL=postgresql+asyncpg://postgres:example@db:5432/exampledb
DB_PASSWORD=example
DB_NAME=exampledb
DB_USER=postgres
JWT_SECRET_KEY=examplesecretkey
JWT_ENCODE_ALGORITHM=HS256
GOOGLE_SECRET_KEY=examplesecretkey
GOOGLE_CLIENT_ID=exampleclientid
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google
YANDEX_REDIRECT_URI=http://localhost:8000/auth/yandex
YANDEX_CLIENT_ID=exampleclientid
YANDEX_SECRET_KEY=examplesecretkey
DB_TEST_URL=postgresql+asyncpg://postgres:example@db:5432/exampledbtest
SMTP_PASSWORD=examplepassword
from_email=example@example.com
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
POSTGRES_PASSWORD=example
POSTGRES_USER=postgres
POSTGRES_DB=exampledb
DB_TEST_PORT=5432
EXISTS_GOOGLE_USER_EMAIL=example@example.com
```

### 3. Запуск с Docker

```bash
docker-compose up -d --build
```
Может потребоваться дополнительное обновление базы данных до последней миграции:
```bash
docker-compose exec -it app bash
poetry run alembic upgrade head
```

Приложение будет доступно по адресу: http://localhost:8000


## 📚 API Документация

После запуска приложения доступны:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Аутентификация

API использует JWT токены для аутентификации. Добавьте токен в заголовок запроса:

```http
Authorization: Bearer ваш_jwt_токен
```

## API Endpoints

### Аутентификация
- `POST /auth/login` - вход в систему
- `GET /auth/login/google` - вход в систему через google аккаунт
- `GET /auth/google` - Авторизация в системе через google
- `GET /auth/login/yandex` - вход в систему через yandex аккаунт
- `GET /auth/login` - Авторизация в системе через yandex

### Задачи (Tasks)
- `GET /tasks/all` - список задач пользователя
- `POST /tasks/` - создание новой задачи
- `GET /tasks/{task_id}` - получение задачи по ID
- `PATCH /tasks/{task_id}` - обновление задачи
- `DELETE /tasks/{task_id}` - удаление задачи

### Таймер (Timer)
- `GET /timer/{task_id}` - получение задачи по id
- `GET /timer/start/{task_id}` - запуск таймера
- `POST /timer/pause/{task_id}` - пауза таймера
- `POST /timer/reset/{task_id}` - снятие с паузы
- `GET /timer/status/{task_id}` - статус таймера
- `POST /timer/end/{task_id}` - завершение задачи
- `POST /timer/skip/{task_id}` - пропуск текущего этапа

### Пользователь (User)
- `POST /user` - создание пользователя
- `GET /user/settings` - настройки таймера
- `PATCH /user/settings` - обновление настроек

## 🎯 Примеры использования

### Запуск таймера

```bash
curl -X GET "http://localhost:8000/timer/start/1" \
  -H "Authorization: Bearer ваш_токен"
```

### Получение статуса таймера

```bash
curl -X GET "http://localhost:8000/timer/status/1" \
  -H "Authorization: Bearer ваш_токен"
```


## ⚙️ Настройки по умолчанию

- **Рабочий интервал**: 25 минут
- **Короткий перерыв**: 5 минут
- **Количество помидоров**: настраивается для каждой задачи

## Диагностика проблем

### Частые проблемы:

1. **Ошибки подключения к БД**:
   - Проверьте настройки PostgreSQL в .env файле
   - Убедитесь, что БД запущена

2. **Проблемы с Redis**:
   - Проверьте доступность Redis сервера
   - Убедитесь в правильности настроек

3. **Ошибки Celery**:
   - Проверьте подключение к RabbitMQ
   - Убедитесь, что worker запущен

### Логи:

```bash
# Просмотр логов приложения
docker-compose logs app

# Просмотр логов Celery
docker-compose logs celery

# Просмотр логов БД
docker-compose logs db
# Отедльный файл с логами:
middleware.log
```

## Автор:

Федоров Дмитрий – [fedorovd2005@gmail.com](mailto:fedorovd2005@gmail.com)
