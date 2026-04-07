from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    """
    Schema for a chat request.
    """
    session_id: str
    message: str

class ChatResponse(BaseModel):
    """
    Schema for a chat response.
    """
    reply: str

class MessageHistory(BaseModel):
    """
    Schema for a single message in the history.
    """
    role: str  # 'user' or 'assistant'
    content: str

class HistoryResponse(BaseModel):
    """
    Schema for the full chat history of a session.
    """
    session_id: str
    history: List[MessageHistory]

class HealthResponse(BaseModel):
    """
    Schema for the service health check.
    """
    status: str
