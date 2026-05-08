<<<<<<< HEAD
# SmartTask – Real-Time Task Management System

SmartTask is a Flask-based task management web application built with PostgreSQL, REST APIs, and WebSocket-powered real-time updates.

The project demonstrates backend engineering concepts such as authentication, database design, modular architecture, realtime communication, and frontend-backend integration.

---

# Features

- User registration and login authentication
- Secure password hashing and session management
- Create, update, complete, and delete tasks
- Real-time dashboard updates using Flask-SocketIO
- PostgreSQL integration with SQLAlchemy ORM
- Task analytics dashboard
- Responsive UI using Bootstrap 5
- Toast notifications and frontend validation
- Structured Flask architecture using blueprints and services
- Logging and request tracking

---

# Tech Stack

## Backend
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-SocketIO

## Database
- PostgreSQL
- SQLAlchemy ORM

## Frontend
- HTML
- CSS
- Bootstrap 5
- Vanilla JavaScript

## Data & Analytics
- Pandas
- NumPy

## Testing
- Pytest

---

# Project Structure

```bash
SmartTask/
│
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── static/
│   ├── templates/
│   ├── utils/
│   ├── websocket/
│   ├── db/
│   ├── __init__.py
│   └── socketio.py
│
├── tests/
├── logs/
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

---

# Installation

## 1. Clone Repository

```bash
git clone <your-repository-url>
cd SmartTask
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### macOS/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# PostgreSQL Setup

Open PostgreSQL:

```bash
psql postgres
```

Create database and user:

```sql
CREATE DATABASE smarttask;

CREATE USER smarttask WITH PASSWORD 'smarttask';

GRANT ALL PRIVILEGES ON DATABASE smarttask TO smarttask;
```

Connect database:

```sql
\c smarttask
```

Grant schema permissions:

```sql
GRANT ALL ON SCHEMA public TO smarttask;

ALTER SCHEMA public OWNER TO smarttask;
```

---

# Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key

DATABASE_URL=postgresql+psycopg2://smarttask:smarttask@localhost:5432/smarttask

FLASK_CONFIG=config.DevelopmentConfig
```

---

# Run Project

Start application:

```bash
python run.py
```

Application runs on:

```text
http://127.0.0.1:5001
```

---

# Real-Time WebSocket Updates

SmartTask uses Flask-SocketIO for realtime dashboard synchronization.

Realtime events include:
- Task creation
- Task completion
- Task deletion

The frontend automatically refreshes dashboard data without manual page reload.

---

# Main API Endpoints

## Authentication

| Method | Endpoint |
|---|---|
| POST | /auth/register |
| POST | /auth/login |
| GET | /auth/logout |

---

## Tasks

| Method | Endpoint |
|---|---|
| GET | /tasks |
| POST | /tasks |
| PUT | /tasks/<id> |
| DELETE | /tasks/<id> |

---

# Screenshots

## Dashboard
`screenshots/dashboard.png`

## Login
`screenshots/login.png`

## Register
`screenshots/register.png`

---

# Future Improvements

- Task search and filtering
- User profile settings
- Task deadlines and reminders
- Team collaboration
- Role-based permissions
- Docker deployment
- Email notifications

---

# Learning Outcomes

This project helped strengthen understanding of:

- Flask application architecture
- REST API development
- PostgreSQL integration
- ORM relationships
- Authentication systems
- Real-time communication with WebSockets
- Frontend and backend integration

---

# License

MIT License
=======
# SmartTask-Pro
Real-time task management system built with Flask, PostgreSQL, SQLAlchemy, and Flask-SocketIO.
>>>>>>> c3c6cfcfa44cd4f4737d3bd5115008abb069484c
