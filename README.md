# Книгарня — інтернет-магазин книг

Курсовий проєкт з дисципліни «Веб-технології та веб-дизайн».
Тема (варіант 14): інформаційна система мережі магазинів із продажу книг
(друкованих та електронних).

## Стек технологій
- Python 3.14
- Django 5.2 LTS
- Django REST Framework
- SQLite
- HTML / CSS

## Запуск проєкту локально

1. Створити та активувати віртуальне середовище:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Встановити залежності:
   ```
   pip install -r requirements.txt
   ```
3. Застосувати міграції:
   ```
   python manage.py migrate
   ```
4. Наповнити базу тестовими книгами:
   ```
   python manage.py seed_books
   ```
5. Створити адміністратора:
   ```
   python manage.py createsuperuser
   ```
6. Запустити сервер:
   ```
   python manage.py runserver
   ```
7. Відкрити http://127.0.0.1:8000/

## Структура проєкту
- `config/` — налаштування та головні маршрути
- `accounts/` — користувачі, реєстрація, підтвердження email, профіль
- `catalog/` — категорії та книги, каталог, пошук
- `cart/` — кошик на основі сесії (працює для гостей)
- `orders/` — замовлення, історія, завантаження е-книг
- `api/` — REST API (DRF)
- `templates/`, `static/` — шаблони та стилі

## Тести
```
python manage.py test
```

## API
- `GET /api/books/` — список книг (параметри: `?search=`, `?type=`)
- `POST /api/books/` — додати книгу
- `GET /api/books/<id>/` — одна книга
- `DELETE /api/books/<id>/` — видалити книгу
- `GET /api/categories/` — категорії
