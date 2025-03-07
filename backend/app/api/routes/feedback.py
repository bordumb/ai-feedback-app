# backend/app/api/routes/feedback.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.services.ai_feedback import analyze_feedback
from app.auth.auth import get_current_user
from app.models.feedback_model import Feedback
from app.models.feedback_table import feedback_table
import sys

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/feedback")
def get_feedback(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Retrieves all feedback, but only for authenticated users.
    """
    feedback_list = db.query(Feedback).order_by(Feedback.created_at.desc()).all()
    return feedback_list


# Pydantic model for creating feedback
class FeedbackCreate(BaseModel):
    user_input: str
    category: str | None = None
    sentiment: str | None = None


@router.post("/feedback", include_in_schema=True)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    """
    Inserts new feedback into the database and returns the newly created row.
    """
    sys.stdout.flush()  # Ensure logs appear in Docker
    print(f"🟢 Received Feedback: {feedback.user_input}", flush=True)

    structured_feedback = analyze_feedback(feedback.user_input)  # AI categorization
    print(f"✅ AI Analysis Result: {structured_feedback}", flush=True)

    if structured_feedback is None:
        raise HTTPException(status_code=500, detail="AI processing failed.")

    new_feedback = Feedback(
        user_input=feedback.user_input,
        category=structured_feedback.get("category", None),
        sentiment=structured_feedback.get("sentiment", None),
    )

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    print(f"✅ Successfully saved feedback: {new_feedback}", flush=True)
    return new_feedback


@router.get("/feedback", include_in_schema=True)
def get_feedback(db: Session = Depends(get_db)):
    """
    Retrieves all feedback, ordered by the most recent first.
    """
    feedback_list = db.query(Feedback).order_by(Feedback.created_at.desc()).all()
    return feedback_list


def get_all_feedback():
    with SessionLocal() as session:
        stmt = select([
            feedback_table.c.id,
            feedback_table.c.user_input,
            feedback_table.c.category,
            feedback_table.c.sentiment,
            feedback_table.c.created_at
        ])
        result = session.execute(stmt).fetchall()
        return [dict(row) for row in result]