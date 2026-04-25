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

#### Auth — `/v1/auth`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/register` | — | Register new user |
| `POST` | `/login` | — | Login, sets JWT cookies |
| `POST` | `/refresh` | refresh token | Refresh access token |
| `GET` | `/staff_check` | User | Check if current user has staff role |

#### Books — `/v1/book`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/` | — | Get all books |
| `GET` | `/{book_id}` | — | Get book by ID |
| `POST` | `/` | Staff | Upload book with file (`.pdf`, `.doc`, `.docx`, `.txt`) |
| `PATCH` | `/{book_id}` | Staff | Update book |
| `DELETE` | `/{book_id}` | Staff | Delete book |

#### Authors — `/v1/author`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/` | — | Get all authors |
| `GET` | `/{author_id}` | — | Get author by ID |
| `POST` | `/` | Staff | Add new author |
| `PATCH` | `/{author_id}` | Staff | Update author |
| `DELETE` | `/{author_id}` | Staff | Delete author |

#### Users — `/v1/user`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/` | Staff | Get all users |
| `GET` | `/me` | User | Get own profile |
| `GET` | `/{user_id}` | Staff | Get user by ID |
| `PATCH` | `/me` | User | Update own profile |
| `PATCH` | `/{user_id}` | Staff | Update any user |
| `DELETE` | `/{user_id}` | Staff | Delete user |

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

#### Авторизація — `/v1/auth`

| Метод | Ендпоінт | Доступ | Опис |
|-------|----------|--------|------|
| `POST` | `/register` | — | Реєстрація нового користувача |
| `POST` | `/login` | — | Вхід, встановлює JWT cookies |
| `POST` | `/refresh` | refresh token | Оновлення access токена |
| `GET` | `/staff_check` | User | Перевірити чи поточний користувач є staff |

#### Книги — `/v1/book`

| Метод | Ендпоінт | Доступ | Опис |
|-------|----------|--------|------|
| `GET` | `/` | — | Отримати всі книги |
| `GET` | `/{book_id}` | — | Отримати книгу за ID |
| `POST` | `/` | Staff | Завантажити книгу з файлом (`.pdf`, `.doc`, `.docx`, `.txt`) |
| `PATCH` | `/{book_id}` | Staff | Оновити книгу |
| `DELETE` | `/{book_id}` | Staff | Видалити книгу |

#### Автори — `/v1/author`

| Метод | Ендпоінт | Доступ | Опис |
|-------|----------|--------|------|
| `GET` | `/` | — | Отримати всіх авторів |
| `GET` | `/{author_id}` | — | Отримати автора за ID |
| `POST` | `/` | Staff | Додати автора |
| `PATCH` | `/{author_id}` | Staff | Оновити автора |
| `DELETE` | `/{author_id}` | Staff | Видалити автора |

#### Користувачі — `/v1/user`

| Метод | Ендпоінт | Доступ | Опис |
|-------|----------|--------|------|
| `GET` | `/` | Staff | Отримати всіх користувачів |
| `GET` | `/me` | User | Отримати власний профіль |
| `GET` | `/{user_id}` | Staff | Отримати користувача за ID |
| `PATCH` | `/me` | User | Оновити власний профіль |
| `PATCH` | `/{user_id}` | Staff | Оновити будь-якого користувача |
| `DELETE` | `/{user_id}` | Staff | Видалити користувача |

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
