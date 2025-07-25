# Sparrow - Messaging App

## Overview
Sparrow is a Django-based messaging application that provides user authentication, room management, and messaging features. It uses Django REST Framework for API endpoints and JWT for authentication.

# 🐦 Sparrow Backend Setup (Windows Friendly)

This is the backend of the Sparrow messenger project built with Django, PostgreSQL, Redis, JWT, and WebSockets (Django Channels).

---

## 🧩 Requirements

Make sure you have the following installed on your Windows system:

- Python 3.10+  
- PostgreSQL 13+  
- Redis  
- Git  
- [Node.js (optional)](https://nodejs.org) — if you want to run frontend or use tools like `npm`.

---

## 🚀 Quick Setup Guide

### 1. Clone the Project

```bash
git clone <your-repo-url>
cd sparrow
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create `.env` File

Create a `.env` file in the root of the project with the following content:

```env
DEBUG=True
SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
USE_DOCKER=False
```

---

### 5. Set Up PostgreSQL Database

- Open **pgAdmin** or use **psql** CLI
- Create a database named `sparrow`
- Create a user `postgres` with password `postgres` (or change the config in `settings.py`)

```sql
CREATE DATABASE sparrow;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE sparrow TO postgres;
```

---

### 6. Start Redis

Install Redis using [this guide for Windows](https://github.com/tporadowski/redis/releases) or use WSL.  
Make sure Redis is running on: `127.0.0.1:6379`

---

### 7. Run Migrations

```bash
python manage.py migrate
```

---

### 8. Create Superuser

```bash
python manage.py createsuperuser
```

---

### 9. Run the Development Server

```bash
python manage.py runserver
```

Or if you're using Channels/WebSockets:

```bash
daphne -b 127.0.0.1 -p 8000 sparrow.asgi:application
```

---

## 🔌 WebSocket Support

This project uses Django Channels with Redis:

- Channels config: `ASGI_APPLICATION = 'sparrow.asgi.application'`
- Redis must be running locally at `localhost:6379`

---

## 🔐 Auth System

- JWT authentication via `djangorestframework-simplejwt`
- OAuth2 via Google is also supported:
  - Redirect URI: `http://localhost:8000/auth/google/callback/`

---

## 📚 API Docs (Swagger)

After running the server, access:

```
http://localhost:8000/swagger/
```

---

## 🐞 Debugging Tips

- Make sure PostgreSQL and Redis are running before starting the server
- If you see a `connection refused` error, double-check the `.env`, Redis, or PostgreSQL settings
- You can enable debug toolbar in dev mode

---

## 📂 Static Files

Collected at:  
```
/staticfiles
```

---

## 🛠 Tech Stack

- Django + DRF
- PostgreSQL
- Redis (Cache + Channels)
- JWT (Access + Refresh)
- Google OAuth2
- Swagger Docs (drf_yasg)
- Channels (ASGI WebSockets)

---

## 📞 Contact

If you need help with setup, contact the backend team.

---
