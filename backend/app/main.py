from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import feedback

app = FastAPI(title="AI Feedback API")

# Include API routes
app.include_router(feedback.router)

@app.get("/")
def read_root():
    return {"message": "AI Feedback API is running!"}
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)