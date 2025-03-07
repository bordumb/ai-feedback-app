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

🧪 Testing the AI Model Locally
Once the backend is running, you can test the AI-powered feedback analysis in two ways:

Using curl (to interact with the FastAPI endpoint)
Using Python (to call the function directly)
1️⃣ Test with curl (via FastAPI)
You can send feedback to the API and see the AI-generated category & sentiment using curl:

sh
Copy
Edit
curl -X POST "http://localhost:8000/feedback" \
     -H "Content-Type: application/json" \
     -d '{"user_input": "The UI is terrible and slow."}'
Expected Response:
json
Copy
Edit
{
  "user_input": "The UI is terrible and slow.",
  "category": "performance",
  "sentiment": "negative",
  "created_at": "2025-03-06T02:26:00.454592",
  "id": 10
}
If you get null values for category and sentiment, check that the AI model is correctly loaded in the backend logs.

2️⃣ Test Directly in Python
You can manually test the AI model inside the backend container or on your local machine.

Inside the Docker Container:
Enter the running backend container:
sh
Copy
Edit
docker exec -it backend_api /bin/sh
Open a Python shell:
sh
Copy
Edit
python
Run the following:
python
Copy
Edit
from app.services.ai_feedback import analyze_feedback

feedback_text = "The checkout process is confusing and slow."
result = analyze_feedback(feedback_text)

print(result)  # Should output the category & sentiment
Expected Output:
python
Copy
Edit
{'category': 'usability', 'sentiment': 'negative'}
If this works but curl requests return null, ensure that:

The AI function is properly called inside backend/app/api/routes/feedback.py.
The backend service has restarted to apply changes:
sh
Copy
Edit
docker restart backend_api

Let me know if you need **any additional details!** 🚀🔥