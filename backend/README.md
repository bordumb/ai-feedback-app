# 🧠 Backend (FastAPI) - AI Feedback System

## 📂 Project Structure
The backend is built using **FastAPI** and handles:
- **Receiving user feedback** from the frontend.
- **Processing feedback** (categorization, sentiment analysis).
- **Storing feedback** in a **PostgreSQL database**.
- **Retrieving stored feedback** for analysis.

```
backend/ 
│── app/ # 🏗️ Main FastAPI application 
│ │── api/ # 🌐 API route handlers 
│ │ │── routes/ # 🚏 API endpoints 
│ │ │ ├── feedback.py # ✍️ API for submitting & retrieving feedback 
│ │── models/ # 🗄️ Database models & session management 
│ │ │── database.py # 🔗 Connects FastAPI to PostgreSQL (SQLAlchemy) 
│ │── services/ # 🤖 AI-powered feedback processing 
│ │ │── ai_feedback.py # 🧠 Categorizes feedback & sentiment analysis 
│ │── main.py # 🚀 FastAPI entry point 
│── .env # 🔐 Environment variables (database URLs, secrets) 
│── Dockerfile # 🐳 Containerizes FastAPI │── requirements.txt # 📦 Backend dependencies
```

---

# 🚀 **Runbook: Initial Installation**

## **1️⃣ Install Dependencies**
Ensure you have **Python 3.10+** installed.

```bash
cd backend
pip install -r requirements.txt
```

## 2️⃣ Set Up Environment Variables

Copy the sample .env file:

```bash
cp .env.example .env
```

Edit .env to include your database configuration:

```ini
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=my_database
POSTGRES_HOST=postgres_db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/my_database
DATABASE_URL_DOCKER=postgresql://postgres:postgres@postgres_db:5432/my_database
```

# 🏁 Runbook: Starting & Restarting the Backend

## 1️⃣ Start FastAPI Locally (Without Docker)

```bash
uvicorn app.main:app --reload
```
✅ Runs FastAPI at:

```cpp
http://127.0.0.1:8000
```

## 2️⃣ Start FastAPI with Docker

```bash
docker-compose up --build -d backend
```
✅ Runs FastAPI inside Docker, connected to PostgreSQL.

## 3️⃣ Restart Backend

If something breaks, restart FastAPI:

```bash
docker-compose restart backend
```
📌 This stops and restarts the backend without affecting the database.

## 4️⃣ Debugging

Check Backend Logs:
```bash
docker logs -f backend_api
```

Manually Test API:
```bash
curl -X GET "http://localhost:8000/docs"
```
## ✅ Expected Output: Swagger UI JSON.

🌐 API Endpoints
Method	Endpoint	Description
POST	/feedback/	Submit user feedback
GET	/feedback/	Retrieve all stored feedback

## 🎯 Common Issues & Fixes

❌ FastAPI fails to connect to PostgreSQL:
```bash
sqlalchemy.exc.OperationalError: connection to server at "postgres_db" failed
```
✅ Fix:
```bash
docker-compose restart postgres
```

❌ Changes are not applied:
```bash
uvicorn app.main:app --reload
```
📌 Restart backend container if running inside Docker.

---

Let me know if you need **any additional details!** 🚀🔥