from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import ChatRequest, ChatResponse, HistoryResponse, MessageHistory, HealthResponse
from app.services.memory import add_message, get_history, clear_history
from app.services.ai import generate_ai_response
from app.config import settings
from slowapi import Limiter
from slowapi.util import get_remote_address

# Create a router instance
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/chat", response_model=ChatResponse)
@limiter.limit("5/minute")
async def chat_endpoint(request_data: ChatRequest, request: Request):
    """
    Main chat endpoint with a rate limit of 5 requests per minute.
    """
    try:
        # 1. Save user message
        add_message(request_data.session_id, "user", request_data.message)
        
        # 2. Get history (to provide context to the AI, limited to keep it efficient)
        history = get_history(request_data.session_id, limit=settings.MAX_HISTORY_MESSAGES)
        
        # 3. Generate response from Gemini
        history_context = history[:-1] if history else []
        ai_reply = generate_ai_response(history_context, request_data.message)
        
        # 4. Save AI's response
        add_message(request_data.session_id, "assistant", ai_reply)
        
        return ChatResponse(reply=ai_reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}", response_model=HistoryResponse)
@limiter.limit("10/minute")
async def get_history_endpoint(session_id: str, request: Request):
    """
    Retrieves history with a rate limit of 10 requests per minute.
    """
    try:
        history_objs = get_history(session_id)
        formatted_history = [
            MessageHistory(role=msg.role, content=msg.content) 
            for msg in history_objs
        ]
        return HistoryResponse(session_id=session_id, history=formatted_history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/history/{session_id}")
async def delete_history_endpoint(session_id: str):
    """
    Deletes all messages for a specific session.
    """
    try:
        clear_history(session_id)
        return {"message": f"History for session {session_id} has been cleared."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Simple health check to verify the API is running.
    """
    return HealthResponse(status="ok")
