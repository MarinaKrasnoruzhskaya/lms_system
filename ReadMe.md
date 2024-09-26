# LMS-система

- Реализована платформа для онлайн-обучения, в которой каждый желающий может размещать свои полезные материалы или
  курсы.
- Реализована работа над SPA веб-приложением. Результат проекта - бэкенд-сервер, который возвращает клиенту
  JSON-структуры.

## Инструкции по установке

1. Клонировать репозиторий
   ```sh
   git clone https://github.com/MarinaKrasnoruzhskaya/lms_system
   ```
2. Перейти в директорию 
   ```sh
   cd lms_system
   ```
3. Установить виртуальное окружение
   ```sh
   python -m venv env
   ```
4. Активировать виртуальное окружение
   ```sh
   env\Scripts\activate
   ```
5. Установить зависимости
   ```sh
   pip install -r requirements.txt
   ```
6. Заполнить файл ```.env.sample``` и переименовать его, дав имя ```.env```
7. Создать БД ```lms_system```
   ```
   psql -U postgres
   create database lms_system;  
   \q
   ```
8. Применить миграции
    ```sh
   python manage.py migrate
    ```
9. Заполнить БД
    ```sh
   python manage.py fill
   ```
10. Запустить Celery worker
   ```sh
   celery -A config worker -l INFO
   ```
11. Запустить планировщик Celery beat
   ```sh
   celery -A config beat -l info -S django
   ```    

## Руководство по использованию

1. Для запуска проекта в терминале IDE выполните команду:

  ```sh
   python manage.py runserver
   ```

## Пользователи проекта:

1. Superuser: {"email": "admin@lms.com", "password": "admin"}
2. Moderator: {"email": "moderator@lms.com", "password": "moderator"}
3. Users: {"email": "user_1@lms.com", "password": "123456"}, {"email": "user_2@lms.com", "password": "123456"}, 
{"email": "owner_course@lms.com","password": "owner"}


## Построен с:

1. Python 3.12
2. env
3. Django 5.0.6
4. Python-dotenv 1.0.1
5. Psycopg2-bynary 2.9.9
6. docutils 0.21.2
7. djangorestframework 3.15.2
8. django-filter 24.3

## Лицензия:

Проект распространяется под [лицензией MIT](LICENSE).
<p align="right">(<a href="#readme-top">Наверх</a>)</p>

