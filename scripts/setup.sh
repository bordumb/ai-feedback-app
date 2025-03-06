#!/bin/bash

echo "🚀 Setting up the project..."

# 🧠 Install Python dependencies
if [ -f "backend/requirements.txt" ]; then
    pip install -r backend/requirements.txt
else
    echo "❌ ERROR: requirements.txt not found in backend/. Please create it!"
    exit 1
fi

# 🖥️ Install frontend dependencies (checking if package.json exists)
if [ -f "frontend/package.json" ]; then
    cd frontend && npm install && cd ..
else
    echo "❌ ERROR: package.json not found in frontend/. Please create it!"
    exit 1
fi

# 🗄️ Setup database (if docker-compose is present)
if [ -f "database/docker-compose.yml" ]; then
    docker-compose up -d
else
    echo "⚠️ WARNING: No docker-compose.yml found. Skipping database setup."
fi

echo "✅ Setup complete! 🎉"
