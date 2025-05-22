# Платформа для обмена вещами (Barter System)

Веб-приложение на Django для организации обмена вещами между пользователями.

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
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env в корневой директории:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

5. Примените миграции:
```bash
python manage.py migrate
```

6. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

7. Запустите сервер разработки:
```bash
python manage.py runserver
```

## Использование

1. Откройте http://localhost:8000 в браузере
2. Зарегистрируйтесь или войдите в систему
3. Создайте объявление о товаре для обмена
4. Просматривайте другие объявления и отправляйте предложения обмена

## API Endpoints

- `/api/ads/` - CRUD операции с объявлениями
- `/api/proposals/` - Управление предложениями обмена
- `/api/users/` - Управление пользователями

## Тестирование

Запуск тестов:
```bash
pytest
```

## Лицензия

MIT 