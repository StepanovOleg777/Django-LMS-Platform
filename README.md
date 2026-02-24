# 📚 Django LMS Platform
Система управления обучением (LMS) на Django с Django REST Framework.

## 🚀 Возможности
🔐 JWT-авторизация с регистрацией пользователей

👥 Группы пользователей (модераторы, обычные пользователи)

📊 Управление курсами и уроками с изображениями

💳 Система платежей с фильтрацией

🔒 Права доступа на уровне объектов

🌍 Русская локализация интерфейса

📱 REST API для всех сущностей

## 🏗️ Технологии
Python 3.10+

Django 5.2

Django REST Framework

JWT-авторизация (Simple JWT)

SQLite (для разработки)

Pillow (работа с изображениями)

Django Filter (фильтрация API)

## ⚙️ Установка
## 1. Клонирование и настройка
bash
git clone <repository-url>
cd Django-LMS-Platform
python -m venv venv

### Активация venv
 Windows:
venv\Scripts\activate
 Linux/Mac:
source venv/bin/activate

### Установка зависимостей
pip install -r requirements.txt
## 2. Настройка базы данных

### Применение миграций
python manage.py migrate

### Создание суперпользователя
python manage.py createsuperuser

### Создание групп (модераторы)
python manage.py create_groups
## 3. Запуск сервера

python manage.py runserver

## 🔐 Аутентификация
Регистрация пользователя
http
POST /api/register/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123",
    "first_name": "Иван",
    "last_name": "Иванов"
}
Получение JWT токена
http
POST /api/token/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
Ответ:

json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbG...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
Использование токена
Добавить в заголовки:

text
Authorization: Bearer <access_token>

## 🛠️ Администрирование
### Админка
Доступ: http://127.0.0.1:8000/admin

### Управление: пользователи, группы, курсы, уроки, платежи

### Создание групп

python manage.py create_groups

## 🔧 Разработка
### Запуск тестов
python manage.py test
## Проверка кода

### Проверка Django
python manage.py check

### Миграции
python manage.py makemigrations
python manage.py migrate

### Статика
python manage.py collectstatic
Переменные окружения (опционально)
Создать файл .env:

env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

## 🚀 Деплой

### Автоматический деплой через GitHub Actions

При каждом пуше в ветку `feature/work_1`:
1. Автоматически запускаются тесты
2. После успешных тестов код деплоится на сервер
3. Обновляются зависимости
4. Применяются миграции
5. Перезапускаются Gunicorn и Celery

### Ручной деплой
ssh stepanov@89.169.133.198
cd /home/stepanov/Django-LMS-Platform
git pull origin feature/work_1
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input
sudo systemctl restart gunicorn
sudo systemctl restart celery
sudo systemctl restart celery-beat


## 🐳 Запуск через Docker

### Предварительные требования
- Установленные Docker и Docker Compose

## Запуск

### Клонируй репозиторий
git clone https://github.com/StepanovOleg777/Django-LMS-Platform.git
cd Django-LMS-Platform

### Создай .env файл (скопируй из .env.example)
cp .env.example .env

### Отредактируй .env, укажи свои данные

### Запусти контейнеры
docker-compose up -d --build

### Приложение доступно по адресу: http://localhost

## Полезные команды

### Просмотр логов
docker-compose logs -f

### Просмотр запущенных контейнеров
docker-compose ps

### Перезапуск контейнеров
docker-compose restart

## 🔄 CI/CD Pipeline
Проект использует GitHub Actions для автоматического тестирования и деплоя.

### Что происходит при каждом пуше в ветку feature/work_1:
✅ Запускаются тесты

✅ Проверяется стиль кода (flake8)

✅ Собираются Docker образы

🚀 Автоматический деплой на сервер 89.169.133.198

### Настроенные GitHub Secrets:
SERVER_HOST - IP сервера

SERVER_USER - пользователь для SSH

SSH_PRIVATE_KEY - приватный ключ для подключения

## 🌐 Деплой на сервер
### Автоматический деплой
Достаточно запушить изменения в ветку feature/work_1 - GitHub Actions сделает всё автоматически.

### Ручной деплой (если нужно)
ssh stepanov@89.169.133.198
cd /home/stepanov/Django-LMS-Platform
git pull origin feature/work_1
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input
sudo systemctl restart gunicorn
sudo systemctl restart celery
sudo systemctl restart celery-beat

# 📊 Проверка работы
### Локально
Главная: http://localhost

Админка: http://localhost/admin

Swagger: http://localhost/swagger

API курсов: http://localhost/api/courses/

### На сервере
Главная: http://89.169.133.198

Админка: http://89.169.133.198/admin

Swagger: http://89.169.133.198/swagger

## 📄 Лицензия
Проект создан для учебных целей

## 👨‍💻 Автор
Платформа: Django LMS

Версия: 1.0

Дата: 2026