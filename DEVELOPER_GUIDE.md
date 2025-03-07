# 🚀 AI Feedback App - DEV Guide

Welcome to the AI Feedback App! This documentation covers everything from setup to troubleshooting.

---

## 📂 Table of Contents

- [Database Setup](#database-setup)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [AI Feedback Processing](#ai-feedback-processing)
- [Frontend Guide](#frontend-guide)
- [Start Script](#start-script)
- [Docker Setup](#docker-setup)

---

## 🛠️ Database Setup

### 📌 Initial Setup

Your database runs inside a **Docker container**. To initialize it:

```sh
docker compose up -d
```

To apply database schema:
```sh
docker exec -i postgres_db psql -U postgres -d my_database < database/schema.sql
```

📊 Checking Tables

To see existing tables:

```sh
docker exec -it postgres_db psql -U postgres -d my_database -c "\dt"
```
⚠️ Common Issues
❌ "relation does not exist" error

If a table is missing, reapply the schema:

```sh
docker restart postgres_db
docker exec -i postgres_db psql -U postgres -d my_database < database/schema.sql
```
❌ Database not visible in TablePlus
Ensure TablePlus connects to localhost:5432
Use:
User: postgres
Password: postgres

## 🔐 Authentication

### 🔹 How Authentication Works
Uses JWT tokens (`fastapi.security.OAuth2PasswordBearer`)
Passwords hashed using `bcrypt`
Frontend stores login state in cookies

### 🔑 Creating an Admin Account

Run:
```sh
python backend/app/scripts/create_admin_account.py
```

This creates:
```plaintext
Email: admin@example.com
Password: admin123
```

### ⚠️ Debugging Login Issues

❌ "Invalid username or password"
Check the hashed password in the database:
```sh
docker exec -it postgres_db psql -U postgres -d my_database -c "SELECT * FROM accounts;"
```
Ensure is_admin is `true`.

## 🚀 API Endpoints

### 🔹 Feedback API

`POST /feedback` (Submit Feedback)

Request:
```json
{
  "user_input": "This app is slow."
}
```
Response:
```json
{
  "id": 1,
  "user_input": "This app is slow.",
  "category": "Performance",
  "sentiment": "Negative",
  "created_at": "2025-03-07T12:34:56Z"
}
```

`GET /feedback` (Fetch All Feedback)

## 🧠 AI Feedback Processing

### 📌 How it Works
* Uses NLP to analyze feedback
* Categorizes feedback based on predefined models

### 📤 Expected Input
```json
{
  "user_input": "The UI is slow."
}
```

### 📥 Expected Output
```json
{
  "category": "Performance",
  "sentiment": "Negative"
}
```

### ⚠️ Debugging AI Issues

❌ AI returns None
Check backend logs:
```sh
docker logs backend_api
```
Manually test AI:
```sh
docker exec -it backend_api python
from app.services.ai_feedback import analyze_feedback
print(analyze_feedback("The UI is terrible."))
```

## 🖥️ Frontend Guide

### 🚀 Running the Frontend
```sh
cd frontend
npm install
npm run dev
```

### 🔑 Authentication Flow
* JWT stored in cookies
* Redirects to /auth if user isn't logged in

📝 Sending Feedback
```js
fetch("http://localhost:8000/feedback/", {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ user_input: input })
});
```

### 🏁 Start Script (start.sh)
🛠️ What It Does
* 1️⃣ Stops any running processes on ports 3001 & 8000
* 2️⃣ Starts backend (uvicorn app.main:app --port 8000)
* 3️⃣ Starts frontend (npm run dev --port 3001)

### 📌 Running the Script
```sh
bash scripts/start.sh
```

### ⚠️ Debugging Issues

❌ App doesn’t start
Run manually:
```sh
cd backend && uvicorn app.main:app --port 8000
cd frontend && npm run dev --port 3001
```

Check logs:
```sh
docker logs backend_api
🐳 Docker Setup
📦 Running with Docker
sh
Copy
Edit
docker compose up -d
```

## 📊 Database Setup

To initialize tables:
```sh
docker exec -i postgres_db psql -U postgres -d my_database < database/schema.sql
```

---

## **📌 Summary**
- 🛠️ **Database Setup** → `Database.md`
- 🔐 **Authentication** → `auth/README.md`
- 📩 **API Endpoints** → `routes/README.md`
- 🧠 **AI Processing** → `services/README.md`
- 🖥️ **Frontend Guide** → `frontend/README.md`
- 🏁 **Start Script** → `scripts/README.md`
- 🐳 **Docker Setup** → `Docker.md`

---