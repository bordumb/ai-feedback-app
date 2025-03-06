from sqlalchemy import create_engine

DATABASE_URL = "postgresql://user:password@localhost/feedback_db"
engine = create_engine(DATABASE_URL)
