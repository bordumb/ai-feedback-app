#!/bin/bash

# Automatically set environment to development (unless already set)
export ENV=${ENV:-development}
export PYTHONPATH=$(pwd)/backend
export NODE_ENV=development

echo "🚀 Restarting Docker to ensure a fresh start..."

# Kill any existing Docker processes
pkill Docker

sleep 5  # Adjust if needed

# Restart Docker
open -a Docker

# Wait for Docker to fully restart
echo "⏳ Waiting for Docker to restart..."
while ! docker info &> /dev/null; do
    echo "⏳ Waiting for Docker daemon..."
    sleep 10  # Adjust if needed
done

echo "✅ Docker is running!"

echo "🚀 Checking for existing processes on ports 3001 and 8000..."

# Kill any process running on port 3001 (Next.js)
if lsof -ti :3001 > /dev/null; then
    echo "⚠️  Port 3001 is in use. Stopping previous process..."
    kill -9 $(lsof -ti :3001)
fi

# Kill any process running on port 8000 (FastAPI)
if lsof -ti :8000 > /dev/null; then
    echo "⚠️  Port 8000 is in use. Stopping previous process..."
    kill -9 $(lsof -ti :8000)
fi

echo "✅ All old processes stopped. Starting the application..."

echo "🔹 Checking Node.js version..."
REQUIRED_NODE="20"
CURRENT_NODE=$(node -v | cut -d. -f1 | cut -c2-)

if [ "$CURRENT_NODE" -lt "$REQUIRED_NODE" ]; then
    echo "❌ Node.js version is too old ($CURRENT_NODE). Switching to Node.js $REQUIRED_NODE..."
    nvm use 20 || nvm install 20
fi

echo "🔹 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "🔹 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

echo "🔹 Removing stale Python cache..."
find backend -name "__pycache__" -exec rm -rf {} +

echo "🔹 Restarting Docker services..."
docker compose down
docker compose up -d

# Run this if new tables added or schemas have changed
# echo "🔹 Checking if database is already initialized..."
# if ! docker exec -it postgres_db psql -U postgres -d my_database -c "SELECT 1 FROM accounts LIMIT 1;" > /dev/null 2>&1; then
#     echo "⚡ Running migrations..."
#     docker exec -it postgres_db psql -U postgres -d my_database -f database/schema.sql
# else
#     echo "✅ Database already initialized. Skipping migrations."
# fi

echo "🔹 Starting backend FastAPI server..."
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
echo "✅ FastAPI backend started on http://localhost:8000"
cd ..

echo "🔹 Starting frontend Next.js app..."
cd frontend
npm run dev -- -p 3001 &
echo "✅ Next.js frontend started on http://localhost:3001"
cd ..

echo "✅ App is running! 🚀"
