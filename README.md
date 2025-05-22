# Бартерная система

Система для обмена вещами между пользователями.

## Требования

- Python 3.8+
- PostgreSQL 13+
- Docker и Docker Compose (опционально)

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd barter-system
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env в корневой директории проекта:
```
DEBUG=True
SECRET_KEY=your-secret-key
POSTGRES_DB=barter_local
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

5. Создайте базу данных PostgreSQL:
```bash
createdb barter_local
```

6. Примените миграции:
```bash
python manage.py migrate
```

7. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

8. Запустите сервер разработки:
```bash
python manage.py runserver
```

## Запуск с Docker

### Локальное окружение
```bash
docker-compose -f docker-compose.local.yml up --build
```

### Разработка
```bash
docker-compose -f docker-compose.dev.yml up --build
```

### Продакшн
```bash
docker-compose -f docker-compose.prod.yml up --build
```

## API Документация

После запуска сервера, API документация доступна по следующим URL:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- JSON схема: http://localhost:8000/swagger.json

## Тестирование

Для запуска тестов используйте:
```bash
pytest
```

## Основные функции

- Создание и управление объявлениями
- Категоризация объявлений
- Система обмена вещами
- Поиск и фильтрация объявлений
- REST API для интеграции
- Swagger документация API

## Функциональность

- Создание, редактирование и удаление объявлений
- Поиск и фильтрация объявлений
- Система предложений обмена
- REST API для работы с данными
- Современный веб-интерфейс

## Технический стек

- Python 3.8+
- Django 4.2
- Django REST Framework
- SQLite (для разработки) / PostgreSQL (для продакшена)
- Bootstrap 5
- Crispy Forms

## Использование

1. Откройте http://localhost:8000 в браузере
2. Зарегистрируйтесь или войдите в систему
3. Создайте объявление о товаре для обмена
4. Просматривайте другие объявления и отправляйте предложения обмена

## API Endpoints

- `/api/ads/` - CRUD операции с объявлениями
- `/api/proposals/` - Управление предложениями обмена
- `/api/users/` - Управление пользователями

## Лицензия

MIT 