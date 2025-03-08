# Database

# 🗄️ Database - PostgreSQL Setup for AI Feedback System

## 📂 Project Structure
The `database` directory contains everything needed to set up and manage a **PostgreSQL database** for the AI feedback system.

```
database/ 
│── docker-compose.yml # 🛠️ Defines PostgreSQL service 
│── schema.sql # 📜 SQL script for creating feedback table 
│── migrations/ # 🔄 (Optional) Future database migrations
```

---

# 🚀 **Runbook: Initial Setup & Installation**

## **1️⃣ Install Docker & Docker Compose**
If you don’t have Docker installed, follow the official guide:  
🔗 [Docker Installation](https://docs.docker.com/get-docker/)

Verify installation:
```bash
docker -v
docker-compose -v
```
✅ Expected output:

```pgsql
Docker version 20.x.x
docker-compose version 1.x.x
```

## 2️⃣ Configure Environment Variables

📍 Edit backend/.env to match your database configuration:

```ini
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=my_database
POSTGRES_HOST=postgres_db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/my_database
DATABASE_URL_DOCKER=postgresql://postgres:postgres@postgres_db:5432/my_database
```

# 🏁 Runbook: Starting & Managing the Database

## 1️⃣ Start PostgreSQL with Docker

To start the PostgreSQL database, run:
```bash
docker-compose up -d postgres
```
✅ Expected Output:
```bash
Creating network ai-feedback-app_default
Creating volume database_postgres_data
Creating postgres_db ... done
```
📌 This starts PostgreSQL as a container with a persistent volume.

## 2️⃣ Check if PostgreSQL is Running

Run:
```bash
docker ps
```
✅ Expected Output:
```nginx
CONTAINER ID   IMAGE         PORTS                    NAMES
abcdef123456   postgres:15   0.0.0.0:5432->5432/tcp   postgres_db
```
❌ If postgres_db is missing, restart it:

```bash
docker-compose up -d postgres
```

## 3️⃣ Apply Database Schema

The schema.sql file contains the structure for the feedback table.

📍 Apply the schema manually:

```bash
docker exec -it postgres_db psql -U postgres -d my_database -f /database/schema.sql
```
✅ Expected Output:
```sql
CREATE TABLE
```
📌 This ensures the feedback table exists.

## 4️⃣ Verify Database & Tables

After applying the schema, check if the feedback table exists:

```bash
docker exec -it postgres_db psql -U postgres -d my_database
```
Then, run:
```sql
SELECT * FROM pg_tables WHERE tablename = 'feedback';
```
✅ Expected Output:

```cpp
 schemaname |  tablename  | tableowner | ...
------------+------------+------------
 public     | feedback   | postgres   |
```

# 🏁 Runbook: Restarting & Debugging

## 1️⃣ Restart PostgreSQL

If the database stops responding:

```bash
docker-compose restart postgres
```
📌 This restarts PostgreSQL without deleting data.

## 2️⃣ Reset PostgreSQL (Deletes Data)

If you need a fresh start:

```bash
docker-compose down -v
docker volume rm database_postgres_data
docker-compose up -d postgres
```
📌 WARNING: This deletes all database data.

## 3️⃣ View Database Logs

To check for errors:
```bash
docker logs -f postgres_db
```

## 4️⃣ Manually Insert Test Data

To manually insert feedback:
```sql
INSERT INTO feedback (user_input, category, sentiment)
VALUES ('This app is great!', 'usability', 'positive');
```

## 5️⃣ Query Feedback Data

To view stored feedback:
```sql
SELECT * FROM feedback;
```
✅ Expected Output:
```python
 id |       user_input       |  category   | sentiment |      created_at
----+------------------------+------------+-----------+------------------------
  1 | This app is great!     | usability  | positive  | 2025-03-06 01:10:00
```

## 📜 Database Schema Reference

📍 schema.sql
```sql
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    user_input TEXT NOT NULL,
    category VARCHAR(255),
    sentiment VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);
```

# TODO:

🔹 Next Steps for Full GDPR Compliance
1️⃣ Privacy Policy Update

Make sure your system explicitly states what user data is collected, why, and how long it’s retained.
2️⃣ Data Export API

Create an endpoint that allows users to download their data (export_token allows verification).
3️⃣ Automated Deletion

If a user requests account deletion, set deleted_at and remove personal data after a set retention period.
4️⃣ Hashing Strategy

Use SHA-256 or bcrypt to hash emails and phone numbers, so they’re stored securely without exposing real data.

# Debugging Notes

6. Troubleshooting Checklist
Docker not running?
bash
Copy
Edit
open -a Docker
docker info
Containers not up?
bash
Copy
Edit
docker compose ps
docker compose logs backend_api
docker compose logs postgres_db
Database not found or “host not found”?
Check POSTGRES_HOST=postgres.
Both backend_api and postgres must be in the same Docker Compose file.
“Connection refused”?
The database might be starting slower than the backend. Use healthcheck with depends_on: condition: service_healthy.
Recv failure: Connection reset by peer?
The backend is crashing. Check logs to see why.
🚀 Final Workflow Summary
Start Docker
bash
Copy
Edit
open -a Docker
Navigate to your project
bash
Copy
Edit
cd ai-feedback-app
Start everything
bash
Copy
Edit
docker compose up -d --build
Check containers
bash
Copy
Edit
docker compose ps
docker logs backend_api --tail=50
If database is new, run
bash
Copy
Edit
docker exec -it postgres_db psql -U postgres -d my_database -f database/schema.sql
Create an admin
bash
Copy
Edit
python backend/app/scripts/create_admin_account.py
Test
bash
Copy
Edit
curl http://localhost:8000/docs
Stop everything
bash
Copy
Edit
docker compose down
With these steps in place—one Docker Compose file, the correct environment variables, and a wait-for-database strategy—your entire environment should “just work” next time.