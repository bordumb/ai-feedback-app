# backend/models/schemas.py
from typing import TypedDict
from datetime import datetime

class FeedbackDict(TypedDict):
    id: int
    user_input: str
    category: str | None
    sentiment: str | None
    created_at: datetime | None
