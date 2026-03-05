# 📚 StudyOS — Full-Stack Django Student Dashboard

A full-screen, OS-style academic command center built with Django + vanilla JS.

---

## 🚀 Quick Start

### 1. Install Python (3.10+) & pip
Make sure Python is installed: `python --version`

### 2. Install Django
```bash
pip install -r requirements.txt
```

### 3. Set up the database
```bash
python manage.py makemigrations api
python manage.py migrate
```

Or just run the setup script:
```bash
bash setup.sh
```

### 4. Start the server
```bash
python manage.py runserver
```

### 5. Open in browser
```
http://127.0.0.1:8000
```

Register a new account → you'll get a pre-seeded set of subjects (Math, Physics, Chemistry, English).

---

## 🗂️ Project Structure

```
studyos/
├── manage.py
├── requirements.txt
├── setup.sh
├── db.sqlite3              ← auto-created on first run
│
├── studyos/                ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── api/                    ← Main app
│   ├── models.py           ← All DB models
│   ├── views.py            ← API + page views
│   ├── urls.py             ← URL routing
│   └── admin.py            ← Admin panel config
│
├── templates/
│   └── api/
│       ├── index.html      ← Main OS dashboard
│       ├── login.html      ← Login page
│       └── register.html   ← Registration page
│
└── static/                 ← Static files (if needed)
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 Auth | Register / Login / Logout with Django sessions |
| ✅ Tasks | Add, complete, delete tasks with priority & subject |
| ⏱ Pomodoro | 25/5/15 min timer with sound, session logging |
| 📊 Analytics | 7-day bar + line chart (Chart.js) |
| ✦ Habits | 7-day habit tracker with streak counter |
| 📓 Notes | Subject-wise notes with auto-save to DB |
| 📅 Calendar | Monthly calendar with events |
| ☾/☀ Theme | Dark & Light mode (saved to DB per user) |
| 🔥 Streaks | Habit streak tracking per user |
| 🛡️ Admin | Full Django admin for all models |

---

## 🔧 API Endpoints

| Method | URL | Description |
|---|---|---|
| POST | `/api/theme/` | Save user theme preference |
| GET | `/api/tasks/` | List tasks |
| POST | `/api/tasks/create/` | Create task |
| PATCH/DELETE | `/api/tasks/<id>/` | Update/delete task |
| GET | `/api/subjects/` | List subjects |
| POST | `/api/subjects/create/` | Create subject |
| GET | `/api/notes/` | List notes |
| POST | `/api/notes/save/` | Save note |
| GET | `/api/habits/` | List habits |
| POST | `/api/habits/create/` | Create habit |
| PATCH | `/api/habits/<id>/toggle/` | Toggle habit day |
| DELETE | `/api/habits/<id>/delete/` | Delete habit |
| GET | `/api/sessions/` | List focus sessions |
| POST | `/api/sessions/create/` | Save session |
| GET | `/api/events/` | List calendar events |
| POST | `/api/events/create/` | Create event |
| DELETE | `/api/events/<id>/delete/` | Delete event |
| GET | `/api/analytics/` | 7-day analytics data |

---

## 🛡️ Admin Panel

Access at `/admin/` after creating a superuser:
```bash
python manage.py createsuperuser
```

---

## 🎨 Tech Stack

- **Backend**: Django 4.2, SQLite (dev) / PostgreSQL (prod)
- **Frontend**: Vanilla JS, Chart.js, Google Fonts (Syne + Space Mono + DM Sans)
- **Auth**: Django session authentication
- **Storage**: Django ORM with SQLite

---

## 🌐 Production Deployment

For production:
1. Set `DEBUG = False` in `settings.py`
2. Change `SECRET_KEY` to a secure random value
3. Set `ALLOWED_HOSTS` to your domain
4. Use PostgreSQL instead of SQLite
5. Run `python manage.py collectstatic`
6. Use Gunicorn + Nginx

---

Made with ❤️ for students everywhere.
