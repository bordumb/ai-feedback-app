# database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)

# PostgreSQL Config
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "my_database")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres_db")  # Use `postgres_db` inside Docker
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# Select correct DATABASE_URL
ENV = os.getenv("ENV", "development")

if ENV == "production":
    DATABASE_URL = os.getenv("DATABASE_URL_DOCKER", f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
else:
    DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}")

if not DATABASE_URL:
    raise ValueError("❌ ERROR: DATABASE_URL is not set! Check your .env file.")

print(f"✅ Using database: {DATABASE_URL}")

# SQLAlchemy Engine & Session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Feedback Model
class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(Text, nullable=False)
    category = Column(String, index=True)
    sentiment = Column(String, index=True)
    created_at = Column(TIMESTAMP, server_default="now()")

# Create Tables
Base.metadata.create_all(bind=engine)

def init_db():
    # If you want to run migrations or create tables automatically, do it here.
    with engine.connect() as conn:
        with open("database/schema.sql", "r") as f:
            conn.execute(f.read())
