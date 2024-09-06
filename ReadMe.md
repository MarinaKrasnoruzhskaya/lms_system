# LMS-система

- Реализована платформа для онлайн-обучения, в которой каждый желающий может размещать свои полезные материалы или
  курсы.
- Реализована работа над SPA веб-приложением. Результат проекта - бэкенд-сервер, который возвращает клиенту
  JSON-структуры.

Инструкции по установке
------------

1. Клонировать репозиторий
   ```sh
   git clone https://github.com/MarinaKrasnoruzhskaya/lms_system
   ```
2. Перейти в директорию django_shop
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
   pip install -r requirements.tx
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

Руководство по использованию
---------------

1. Для запуска проекта в терминале IDE выполните команду:

  ```sh
   python manage.py runserver
   ```


Построен с:
---------------

1. Python 3.12
2. env
3. Django 5.0.6
4. Python-dotenv 1.0.1
5. Psycopg2-bynary 2.9.9
6. docutils 0.21.2
7. djangorestframework 3.15.2
8. django-filter 24.3

Контакты
---------------
Марина Красноружская - krasnoruzhskayamarina@yandex.ru

Ссылка на
проект: [https://github.com/MarinaKrasnoruzhskaya/django_shop](https://github.com/MarinaKrasnoruzhskaya/django_shop)

<p align="right">(<a href="#readme-top">Наверх</a>)</p>

