#!/bin/bash

echo "🚀 Creating directories and files for the MVP..."

# 🖥️ Frontend (Next.js)
mkdir -p frontend/src/{pages,api}
touch frontend/src/pages/index.tsx
touch frontend/src/api/index.ts
echo "✅ Created frontend structure."

# 🧠 Backend (FastAPI)
mkdir -p backend/app/{api/routes,models,services}
touch backend/app/main.py
touch backend/app/api/routes/feedback.py
touch backend/app/models/database.py
touch backend/app/services/ai_feedback.py
echo "✅ Created backend structure."

# 🗄️ Database (PostgreSQL)
mkdir -p database
touch database/schema.sql
echo "✅ Created database structure."

# 🔧 Scripts
mkdir -p scripts
touch scripts/setup.sh
touch scripts/start.sh
chmod +x scripts/*.sh
echo "✅ Created setup scripts."

# 📝 Populate key files
echo 'from fastapi import FastAPI' > backend/app/main.py
echo 'from sqlalchemy import create_engine' > backend/app/models/database.py
echo 'import random' > backend/app/services/ai_feedback.py
echo 'export const sendFeedback = async (input: string) => {};' > frontend/src/api/index.ts

echo 'CREATE TABLE feedback (id SERIAL PRIMARY KEY, user_input TEXT NOT NULL);' > database/schema.sql

# 🎉 Success message
echo "🚀 MVP structure created! Start coding! 🎨"

