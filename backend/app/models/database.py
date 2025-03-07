# database.py
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from app.models.feedback_table import feedback_table
from app.models.accounts import Account


load_dotenv()

# ✅ Debug: Print values
print("🔍 DEBUG: Database Connection Details")
print("POSTGRES_USER:", os.getenv("POSTGRES_USER"))
print("POSTGRES_PASSWORD:", os.getenv("POSTGRES_PASSWORD"))
print("POSTGRES_DB:", os.getenv("POSTGRES_DB"))
print("POSTGRES_HOST:", os.getenv("POSTGRES_HOST"))
print("POSTGRES_PORT:", os.getenv("POSTGRES_PORT"))


# Load environment variables
def load_env(dotenv_path: Path = None) -> None:
    """
    Loads environment variables from a .env file if it exists.
    """
    if dotenv_path is None:
        dotenv_path = Path(__file__).resolve().parent.parent / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path)


# Get database config from environment variables
def get_database_config() -> dict:
    """
    Retrieves database configuration from environment variables.
    """
    return {
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "db": os.getenv("POSTGRES_DB", "my_database"),
        "host": os.getenv("POSTGRES_HOST", "postgres_db"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
        "env": os.getenv("ENV", "development"),
    }


# Build the DATABASE_URL from environment variables
def get_database_url(config: dict) -> str:
    """
    Constructs the DATABASE_URL based on environment and fallback settings.
    """
    if config["env"] == "production":
        return f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['db']}"
    return f"postgresql://{config['user']}:{config['password']}@localhost:{config['port']}/{config['db']}"


# Create database engine
def create_db_engine(database_url: str):
    """
    Creates a SQLAlchemy engine.
    """
    if not database_url:
        raise ValueError("❌ ERROR: DATABASE_URL is not set! Check your .env file.")
    
    print(f"✅ Using database: {database_url}")
    return create_engine(database_url)


# Create session maker
def create_session_local(engine):
    """
    Creates a session factory.
    """
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Initialize database schema
def init_db(engine):
    """
    Creates all tables if they don't exist.
    """
    metadata = MetaData()
    with engine.begin() as conn:
        print("🚀 Creating tables if not exist...", flush=True)
        metadata.create_all(bind=conn)  # Ensures tables are created
        print("✅ Tables created successfully!", flush=True)


# Main setup function (can be used in __main__)
def setup_database():
    """
    Orchestrates the database setup process.
    """
    load_env()
    config = get_database_config()
    database_url = get_database_url(config)
    engine = create_db_engine(database_url)
    session_local = create_session_local(engine)
    init_db(engine)
    return session_local  # Return session for further use


# Run database setup and store SessionLocal globally
SessionLocal = setup_database()  # ✅ Defined globally

# Explicitly export it for external imports
__all__ = ["SessionLocal"]

if __name__ == "__main__":
    print("Database setup complete!")  # This runs only if script is executed directly

