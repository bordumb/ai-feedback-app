from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ai_feedback import analyze_feedback

router = APIRouter(prefix="/feedback", tags=["Feedback"])

# Define request model
class FeedbackRequest(BaseModel):
    user_input: str

@router.post("/")
async def collect_feedback(feedback: FeedbackRequest):
    """Receives feedback and processes it using AI."""
    return {"structured_feedback": analyze_feedback(feedback.user_input)}
