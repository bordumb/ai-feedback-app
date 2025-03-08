# backend/app/models/signup_request.py
from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
