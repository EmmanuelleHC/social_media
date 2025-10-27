
# Simple Social Media App with FastAPI

A basic social media web application built with **FastAPI**, **MySQL**, and **HTML templates** (Bootstrap + EasyUI). Users can **register, login, create posts**, and view posts from others in a feed-style dashboard.

---

## Features

* User **registration** and **login** (with hashed passwords).
* **Create posts** and view all posts in the dashboard.
* Dashboard shows posts from **all users**.
---

## Prerequisites

* **Python 3.10+**
* **MySQL server** (e.g., XAMPP, WAMP)
* **pip** package manager

---

## Setup Instructions

1. **Clone the repository:**

```bash
git clone <your-repo-url>
cd <repo-folder>
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Create MySQL database:**

```sql
CREATE DATABASE socialmedia;
```

> Make sure to update `database.py` with your MySQL credentials.

4. **Run the FastAPI app:**

```bash
uvicorn app.main:app --reload
```

5. **Open in browser:**
   Go to [http://127.0.0.1:8000](http://127.0.0.1:8000) to see the login page.

---

## Project Structure

```
app/
├── main.py              # Entry point, mounts routers and templates
├── models.py            # SQLAlchemy models (User, Post)
├── database.py          # Database connection setup
├── auth.py              # Password hashing & verification
├── routers/
│   ├── users.py         # User-related routes (API & HTML)
│   └── posts.py         # Post-related routes (API & HTML)
├── templates/           # HTML templates (login, register, dashboard)
└── static/              # CSS, JS, images
```


