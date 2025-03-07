from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(Text, nullable=False)
    category = Column(String, index=True, nullable=True)
    sentiment = Column(String, index=True, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())  # ✅ Ensures timestamps work
