from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, Feedback  # Import Feedback model
from app.services.ai_feedback import analyze_feedback

router = APIRouter()

# Pydantic model for creating feedback
class FeedbackCreate(BaseModel):
    user_input: str
    category: str | None = None
    sentiment: str | None = None

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/feedback")
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    """
    Inserts new feedback into the database and returns the newly created row.
    """
    structured_feedback = analyze_feedback(feedback.user_input)  # AI categorization

    new_feedback = Feedback(
        user_input=feedback.user_input,
        category=feedback.category,
        sentiment=feedback.sentiment
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)  # Refresh to get the latest row data

    return new_feedback

@router.get("/feedback")
def get_feedback(db: Session = Depends(get_db)):
    """
    Retrieves all feedback, ordered by the most recent first.
    """
    feedback_list = db.query(Feedback).order_by(Feedback.created_at.desc()).all()
    return feedback_list
