# backend/models/feedback_table.py
from sqlalchemy import (
    Table, Column, Integer, String, DateTime, MetaData
)
from sqlalchemy.sql import func

metadata = MetaData()

feedback_table = Table(
    "feedback",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_input", String, nullable=False),
    Column("category", String, index=True, nullable=True),
    Column("sentiment", String, index=True, nullable=True),
    Column("created_at", DateTime, server_default=func.now()),
)

