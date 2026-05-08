# Smart Task Management System

A modern Flask-based Smart Task Management System designed for real-time collaboration, analytics-driven insights, and clean modular architecture. Built with production readiness in mind while staying approachable for internship-level development.

## Project Overview
SmartTask is a task management platform that helps teams plan, prioritize, and track work. It includes authentication, task CRUD, analytics summaries, and real-time notifications through WebSockets.

## Features
- Secure authentication with session management
- Task CRUD APIs with validation and proper error handling
- Analytics summaries powered by Pandas and NumPy
- Real-time task notifications with Flask-SocketIO
- Modular Flask architecture (routes, services, models, utils)
- PostgreSQL-first configuration with SQLAlchemy ORM
- Clean responsive UI templates for dashboard and auth pages
- Centralized logging with request and error tracking

## Architecture
The project follows a clean layered architecture:
- **Routes (API layer):** Flask blueprints that expose REST endpoints.
- **Services (business layer):** Reusable logic (analytics, domain services).
- **Models (data layer):** SQLAlchemy ORM models and relationships.
- **Utils/Infrastructure:** Logging, database setup, and websocket handlers.

The app uses a factory pattern to create the Flask application and wire extensions, making it testable and scalable.

## Folder Structure
```
SmartTask/
├─ .env.example
├─ .gitignore
├─ config.py
├─ requirements.txt
├─ run.py
├─ logs/
├─ app/
│  ├─ __init__.py
│  ├─ db/
│  │  └─ __init__.py
│  ├─ models/
│  │  ├─ __init__.py
│  │  ├─ task.py
│  │  └─ user.py
│  ├─ routes/
│  │  ├─ __init__.py
│  │  ├─ analytics.py
│  │  ├─ auth.py
│  │  └─ tasks.py
│  ├─ services/
│  │  ├─ __init__.py
│  │  ├─ analytics_service.py
│  │  └─ task_service.py
│  ├─ static/
│  │  ├─ css/style.css
│  │  ├─ img/.keep
│  │  └─ js/app.js
│  ├─ templates/
│  │  ├─ base.html
│  │  ├─ dashboard.html
│  │  ├─ login.html
│  │  └─ register.html
│  ├─ utils/
│  │  └─ logger.py
│  └─ websocket/
│     ├─ __init__.py
│     └─ events.py
└─ tests/
   ├─ __init__.py
   └─ test_health.py
```

## Tech Stack
- **Backend:** Flask, Flask-Login, Flask-SocketIO
- **Database:** PostgreSQL, SQLAlchemy, Flask-Migrate
- **Analytics:** Pandas, NumPy
- **Frontend:** HTML, CSS, Bootstrap 5, Vanilla JS
- **Testing:** Pytest

## Installation
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Setup
Copy the sample environment file and update values:
```bash
cp .env.example .env
```

Key variables:
- `FLASK_CONFIG` (default: `config.DevelopmentConfig`)
- `SECRET_KEY`
- `DATABASE_URL`
- `LOG_LEVEL`

## PostgreSQL Setup
Create a database and user:
```sql
CREATE DATABASE smarttask;
CREATE USER smarttask WITH PASSWORD 'smarttask';
GRANT ALL PRIVILEGES ON DATABASE smarttask TO smarttask;
```

Update `.env`:
```
DATABASE_URL=postgresql+psycopg2://smarttask:smarttask@localhost:5432/smarttask
```

## Running Locally
```bash
python run.py
```

The API will be available at `http://localhost:5000`.

## WebSocket (Flask-SocketIO)
Socket.IO is used to broadcast task changes in real time. The server emits:
- `task_created`
- `task_updated`

Each event includes the task payload and user id. You can subscribe to these events in the frontend to update the UI instantly without refresh.

## API Endpoints Summary
Auth
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/logout`

Tasks (login required)
- `GET /tasks`
- `GET /tasks/<id>`
- `POST /tasks`
- `PUT /tasks/<id>`
- `DELETE /tasks/<id>`

Analytics
- `GET /analytics/health` (placeholder)

## Screenshots
- Dashboard: `./screenshots/dashboard.png`
- Login: `./screenshots/login.png`
- Register: `./screenshots/register.png`

## Deployment
1. Set production config:
   ```bash
   export FLASK_CONFIG=config.ProductionConfig
   ```
2. Configure environment variables on your host (SECRET_KEY, DATABASE_URL, LOG_LEVEL).
3. Use a production WSGI server (e.g., Gunicorn) and a Socket.IO-compatible worker.
4. Set up a process manager (systemd, supervisor, or Docker).
5. Configure reverse proxy (Nginx) with WebSocket support.

Example Gunicorn command:
```bash
gunicorn run:app --worker-class eventlet -w 1 -b 0.0.0.0:5000
```

## Future Improvements
- Role-based access control
- Task labels, tags, and advanced filters
- Search and pagination for tasks
- Background jobs for notifications
- Audit logs and activity history
- Metrics and tracing integrations

## License
MIT (or choose your preferred license)
