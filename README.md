<div align="center">

# 📚 FastAPI Pet Project

**A RESTful API for managing books and authors with JWT authentication**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://sqlalchemy.org)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Alembic](https://img.shields.io/badge/Alembic-migrations-6BA539?style=for-the-badge)](https://alembic.sqlalchemy.org)

---

🇬🇧 [English](#english) &nbsp;|&nbsp; 🇺🇦 [Українська](#ukrainian)

</div>

---

<a name="english"></a>
## 🇬🇧 English

### About

A pet project built with **FastAPI** and **async SQLAlchemy 2.0**. Implements a books/authors catalog with file uploads, JWT cookie authentication, and role-based access control.

### Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL + asyncpg |
| ORM | SQLAlchemy 2.0 (async) |
| Migrations | Alembic |
| Auth | AuthX (JWT in HTTP-only cookies) |
| Validation | Pydantic v2 |
| Password hashing | bcrypt |
| Containerization | Docker + Docker Compose |

### Architecture

```
Request → Router → Service → Repository → SQLAlchemy → PostgreSQL
```

- **`api/v1/routers/`** — HTTP endpoints, thin handlers
- **`services/`** — business logic
- **`repository/`** — database queries, all extend `CrudBase`
- **`models/`** — SQLAlchemy ORM models
- **`schemas/`** — Pydantic v2 request/response schemas

### Getting Started

#### With Docker (recommended)

```bash
git clone https://github.com/evilsenpa1/FastAPIpet.git
cd your-repo
cp .env.example .env   # fill in the values
docker-compose up --build
```

API will be available at: `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

#### Local setup

```bash
pip install -r requirements.txt
cp .env.example .env        # fill in the values
alembic upgrade head        # apply migrations
python main.py              # starts on port 8000 with reload
```

### Environment Variables

Copy `.env.example` to `.env` and fill in:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost            # use "db" for Docker
DB_PORT=5432
DB_NAME=your_db_name

SECRET_KEY=your_secret_key  # generate with: openssl rand -hex 32

SUPERUSER_USERNAME=admin
SUPERUSER_EMAIL=admin@example.com
SUPERUSER_PASSWORD=your_admin_password

PROD=false                  # set to true in production (enables Secure cookie flag)
```

### API Endpoints

#### Auth — `/api/v1/auth`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/register` | — | Register new user |
| `POST` | `/login` | — | Login, sets JWT cookies |
| `POST` | `/refresh` | refresh token | Refresh access token |

#### Books — `/api/v1/books`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/get_all_books` | — | Get all books |
| `GET` | `/book_by_id/{id}` | — | Get book by ID |
| `POST` | `/upload_book` | Staff | Upload book with file (`.pdf`, `.doc`, `.docx`, `.txt`) |
| `PATCH` | `/patch_book/{id}` | Staff | Update book |
| `DELETE` | `/delete_books/{id}` | Staff | Delete book |

#### Authors — `/api/v1/authors`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/get_all_authors` | — | Get all authors |
| `GET` | `/author_by_id/{id}` | — | Get author by ID |
| `POST` | `/add_author` | Staff | Add new author |
| `PATCH` | `/update_author/{id}` | Staff | Update author |
| `DELETE` | `/delete_author/{id}` | Staff | Delete author |

#### Users — `/api/v1/users`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/all_users` | Staff | Get all users |
| `GET` | `/user_by_id/{id}` | Staff | Get user by ID |
| `PATCH` | `/patch_user/me` | User | Update own profile |
| `PATCH` | `/patch_user/{id}` | Staff | Update any user |
| `DELETE` | `/delete_user/{id}` | Staff | Delete user |

### Roles

| Role | Permissions |
|------|-------------|
| `USER` | Read books/authors, update own profile |
| `MODERATOR` | All USER permissions + manage books, authors, users |
| `ADMIN` | Full access |

> An initial admin user is created automatically on startup from `SUPERUSER_*` env vars.

### Database Migrations

```bash
alembic upgrade head                           # apply all migrations
alembic revision --autogenerate -m "message"   # generate new migration
alembic downgrade -1                           # roll back one step
```

---

<a name="ukrainian"></a>
## 🇺🇦 Українська

### Про проєкт

Пет-проєкт на **FastAPI** з **async SQLAlchemy 2.0**. Реалізує каталог книг та авторів із завантаженням файлів, JWT-аутентифікацією через HTTP-only cookies та рольовим доступом.

### Технологічний стек

| Шар | Технологія |
|---|---|
| Фреймворк | FastAPI |
| База даних | PostgreSQL + asyncpg |
| ORM | SQLAlchemy 2.0 (async) |
| Міграції | Alembic |
| Авторизація | AuthX (JWT в HTTP-only cookies) |
| Валідація | Pydantic v2 |
| Хешування паролів | bcrypt |
| Контейнеризація | Docker + Docker Compose |

### Архітектура

```
Запит → Router → Service → Repository → SQLAlchemy → PostgreSQL
```

- **`api/v1/routers/`** — HTTP-ендпоінти, тонкі обробники
- **`services/`** — бізнес-логіка
- **`repository/`** — запити до БД, всі наслідують `CrudBase`
- **`models/`** — ORM-моделі SQLAlchemy
- **`schemas/`** — схеми запитів/відповідей Pydantic v2

### Запуск

#### Через Docker (рекомендовано)

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
cp .env.example .env   # заповніть значення
docker-compose up --build
```

API буде доступне за адресою: `http://localhost:8000`  
Інтерактивна документація: `http://localhost:8000/docs`

#### Локально

```bash
pip install -r requirements.txt
cp .env.example .env        # заповніть значення
alembic upgrade head        # застосувати міграції
python main.py              # запуск на порту 8000 з hot-reload
```

### Змінні середовища

Скопіюйте `.env.example` у `.env` та заповніть:

```env
DB_USER=postgres
DB_PASSWORD=ваш_пароль
DB_HOST=localhost            # для Docker вкажіть "db"
DB_PORT=5432
DB_NAME=назва_бази

SECRET_KEY=ваш_секретний_ключ  # згенеруйте: openssl rand -hex 32

SUPERUSER_USERNAME=admin
SUPERUSER_EMAIL=admin@example.com
SUPERUSER_PASSWORD=пароль_адміна

PROD=false                   # true у продакшні (вмикає прапор Secure для cookie)
```

### API Ендпоінти

#### Авторизація — `/api/v1/auth`

| Метод | Ендпоінт | Доступ | Опис |
|-------|----------|--------|------|
| `POST` | `/register` | — | Реєстрація нового користувача |
| `POST` | `/login` | — | Вхід, встановлює JWT cookies |
| `POST` | `/refresh` | refresh token | Оновлення access токена |

#### Книги — `/api/v1/books`

| Метод | Ендпоінт | Доступ | Опис |
|-------|----------|--------|------|
| `GET` | `/get_all_books` | — | Отримати всі книги |
| `GET` | `/book_by_id/{id}` | — | Отримати книгу за ID |
| `POST` | `/upload_book` | Staff | Завантажити книгу з файлом (`.pdf`, `.doc`, `.docx`, `.txt`) |
| `PATCH` | `/patch_book/{id}` | Staff | Оновити книгу |
| `DELETE` | `/delete_books/{id}` | Staff | Видалити книгу |

#### Автори — `/api/v1/authors`

| Метод | Ендпоінт | Доступ | Опис |
|-------|----------|--------|------|
| `GET` | `/get_all_authors` | — | Отримати всіх авторів |
| `GET` | `/author_by_id/{id}` | — | Отримати автора за ID |
| `POST` | `/add_author` | Staff | Додати автора |
| `PATCH` | `/update_author/{id}` | Staff | Оновити автора |
| `DELETE` | `/delete_author/{id}` | Staff | Видалити автора |

#### Користувачі — `/api/v1/users`

| Метод | Ендпоінт | Доступ | Опис |
|-------|----------|--------|------|
| `GET` | `/all_users` | Staff | Отримати всіх користувачів |
| `GET` | `/user_by_id/{id}` | Staff | Отримати користувача за ID |
| `PATCH` | `/patch_user/me` | User | Оновити власний профіль |
| `PATCH` | `/patch_user/{id}` | Staff | Оновити будь-якого користувача |
| `DELETE` | `/delete_user/{id}` | Staff | Видалити користувача |

### Ролі

| Роль | Дозволи |
|------|---------|
| `USER` | Читання книг/авторів, редагування власного профілю |
| `MODERATOR` | Всі дозволи USER + керування книгами, авторами, користувачами |
| `ADMIN` | Повний доступ |

> Початковий адмін-користувач створюється автоматично при запуску зі змінних `SUPERUSER_*`.

### Міграції бази даних

```bash
alembic upgrade head                           # застосувати всі міграції
alembic revision --autogenerate -m "message"   # згенерувати нову міграцію
alembic downgrade -1                           # відкотити один крок
```
