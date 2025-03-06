#!/bin/bash

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

echo "🚀 Starting the application..."
echo "Current directory: $(pwd)"
echo "Checking for frontend directory..."

# Start backend
if [ -d "backend" ]; then
    cd backend
    if [ -f "app/main.py" ]; then
        uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
        echo "✅ FastAPI backend started on http://localhost:8000"
    else
        echo "❌ ERROR: 'app/main.py' not found in backend/. Is FastAPI set up?"
        exit 1
    fi
    cd ..
else
    echo "❌ ERROR: 'backend/' directory not found!"
    exit 1
fi

# Start frontend
if [ -d "frontend" ]; then
    echo "✅ Found frontend directory!"
    cd frontend
    if [ -f "package.json" ]; then
        echo "✅ Found package.json! Starting Next.js..."
        npm run dev -- -p 3001 &
    else
        echo "❌ ERROR: 'package.json' not found in frontend/. Run 'npm init' first."
        exit 1
    fi
    cd ..
else
    echo "❌ ERROR: 'frontend/' directory not found! Listing current files..."
    ls -l
    exit 1
fi

echo "✅ App is running! 🚀"
