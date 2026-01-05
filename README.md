# 🚀 Django REST API Platform
❤️ For kelaasor platform 
## 📖 Reference
- [Platform for learning ](https://kelaasor.com/)

A scalable and modular backend built with **Django REST Framework**, featuring **JWT authentication**, **Redis caching**, **Celery background tasks**, and multiple apps including **User Account**, **Bootcamp**, **Ticket**, **Support**, and **Blog**.

![Demo](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZGpuanNhc2g3ZDJrMXkzdGc3NjlqdWpvdTAxeWdnM2FsbmloMmNmNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5XnfRp2sTnw1qYdLUV/giphy.gif)

# 🧠 Django REST Backend System

A production-ready Django REST API project with:
- 🔐 JWT authentication  
- ⚙️ Rate limiting  
- ⚡ Redis caching  
- 🔁 Celery background tasks  
- postgreSQL
- 🧩 Modular apps: useraccount, bootcamp, ticket, support, and blog




## 🧰 Technologies Used

This project is built using modern and production-ready technologies to ensure performance, scalability, and clean architecture.

### ⚙️ Backend
- 🐍 **Python 3.11**
- 🧱 **Django 5.x**
- ⚡ **Django REST Framework (DRF)** — for building robust RESTful APIs
- 🔐 **JWT Authentication** — secure user authentication using JSON Web Tokens

### 🧩 Apps
- 👤 **UserAccount** — user management & authentication
- 🎓 **Bootcamp** — training or course management
- 🎟️ **Ticket** — ticketing & issue tracking system
- 💬 **Support** — support chat / helpdesk functionality
- 📰 **Blog** — article publishing & content management

### 🚀 Performance & Optimization
- 🧮 **Rate Limiting** — API request throttling using DRF throttles
- ⚡ **Caching with Redis** — improving performance and response time
- 🔁 **Background Tasks with Celery + Redis** — for async task processing (emails, notifications, etc.)

### 🗄️ Database & Storage
- 🐘 **PostgreSQL** — main relational database
- 🧰 **Redis** — in-memory cache and message broker

### 🧰 DevOps / Tools
- 🐳 **Docker & Docker Compose** — containerized environment setup
- 🧪 **Pytest / Django Test Framework** — testing and CI-ready setup
- 🧹 **Black / isort / flake8** — code formatting and linting
- ☁️ **Environment Variables (.env)** — secure configuration management

---

### 📦 Example Stack Overview
```text
Django + DRF  →  PostgreSQL  →  Redis  →  Celery  →  Docker

# Kelassor – Django REST Framework

Production-ready Django REST Framework project, fully containerized with Docker Compose. This setup is designed for **consistent development**, **team collaboration**, and **production-like environments**.

---

## 🚀 Quick Start (Docker Compose – Recommended)

This project runs **exclusively via Docker Compose**. No local Python, PostgreSQL, or Redis installation is required.

### Prerequisites

* Docker (v20+)
* Docker Compose (v2+)

Verify installation:

```bash
docker --version
docker compose version
```

---

## ▶️ Run the Project

```bash
# 1. Clone the repository
git clone https://github.com/Amir-hash19/Final_Project.v2-DRF.git
cd Kelassor

# 2. Create environment file
cp .env.example .env

# 3. Build and start services
docker-compose up --build
```

This will start all required services automatically.

---

## 🌐 Application Access

* API: [http://localhost:8000](http://localhost:8000)
* Admin Panel: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 🧱 Services Architecture

```
+-------------+        +-------------+
|   Client    | -----> |   Django    |
| (Browser /  |        |   REST API  |
|  Mobile)    |        +------+------+ 
+-------------+               |
                              |
        +---------------------+---------------------+
        |                     |                     |
+-------v-------+     +-------v-------+     +-------v-------+
| PostgreSQL DB |     |     Redis     |     |   Celery      |
|   (Data)     |     | (Cache/Broker)|     |   Workers     |
+---------------+     +---------------+     +---------------+
```

---

## ⚙️ Environment Variables

All configuration is managed via environment variables.

Create a `.env` file based on `.env.example`.

### Required Variables

```env
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=kelassor
POSTGRES_USER=kelassor
POSTGRES_PASSWORD=kelassor
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

⚠️ **Never commit `.env` files to version control.**

---

## 🛠 Common Commands

### Django Management

```bash
docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py createsuperuser
docker-compose exec app python manage.py collectstatic
```

### Code Formatting

```bash
docker-compose exec app isort .
docker-compose exec app black .
```

### Stop Services

```bash
docker-compose down
```

---

## 🧪 Development Notes

* Source code is mounted as a Docker volume (hot reload enabled)
* Static files are collected automatically on startup
* Celery workers run as separate services
* Formatting is enforced using **Black + isort**

---

## 🚫 Local (Non-Docker) Execution

Running the project outside Docker is **not supported**.

Docker Compose is the single source of truth for development and deployment.

---

## 📦 Tech Stack

* Django & Django REST Framework
* PostgreSQL
* Redis
* Celery
* Docker & Docker Compose

---

## 📄 License

This project is licensed under the MIT License.
