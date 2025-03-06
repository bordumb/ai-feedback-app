CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    user_input TEXT NOT NULL,
    category TEXT,
    sentiment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);