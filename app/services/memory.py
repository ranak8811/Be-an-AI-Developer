from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, asc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config import settings

# 1. Database Setup
# The engine handles the actual connection to PostgreSQL
engine = create_engine(settings.DATABASE_URL)

# SessionLocal is a factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models
Base = declarative_base()

# 2. Database Model
class ChatHistory(Base):
    """
    SQLAlchemy model for the 'chat_history' table.
    Stores every message sent by the user and the assistant.
    """
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)  # To group messages by session
    role = Column(String)                   # 'user' or 'assistant'
    content = Column(Text)                  # The actual message text
    timestamp = Column(DateTime, default=datetime.utcnow) # When it was sent

# Create the table in the database (if it doesn't exist)
Base.metadata.create_all(bind=engine)

# 3. Helper Functions
def add_message(session_id: str, role: str, content: str):
    """
    Saves a new message to the database.
    """
    db = SessionLocal()
    try:
        new_msg = ChatHistory(session_id=session_id, role=role, content=content)
        db.add(new_msg)
        db.commit()
    finally:
        db.close()

def get_history(session_id: str):
    """
    Retrieves the full, ordered history for a specific session.
    """
    db = SessionLocal()
    try:
        # We order by timestamp so the AI receives messages in the correct sequence
        messages = db.query(ChatHistory).filter(ChatHistory.session_id == session_id).order_by(asc(ChatHistory.timestamp)).all()
        return messages
    finally:
        db.close()

def clear_history(session_id: str):
    """
    Deletes all messages for a specific session (resets the memory).
    """
    db = SessionLocal()
    try:
        db.query(ChatHistory).filter(ChatHistory.session_id == session_id).delete()
        db.commit()
    finally:
        db.close()
