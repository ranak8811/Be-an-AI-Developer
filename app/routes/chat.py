from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, HistoryResponse, MessageHistory, HealthResponse
from app.services.memory import add_message, get_history, clear_history
from app.services.ai import generate_ai_response

# Create a router instance to organize our endpoints
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint. 
    1. Saves the user's message to the database.
    2. Retrieves previous chat history for the session.
    3. Sends history + new message to Gemini.
    4. Saves Gemini's response to the database.
    5. Returns the response to the user.
    """
    try:
        # 1. Save user message
        add_message(request.session_id, "user", request.message)
        
        # 2. Get history (to provide context to the AI)
        history = get_history(request.session_id)
        
        # 3. Generate response from Gemini
        # We pass the history we just got (which includes the user message we just added)
        # Note: In our current logic, we'll pass the history *excluding* the last message
        # as history_context, and pass the last message separately.
        history_context = history[:-1] if history else []
        ai_reply = generate_ai_response(history_context, request.message)
        
        # 4. Save AI's response
        add_message(request.session_id, "assistant", ai_reply)
        
        return ChatResponse(reply=ai_reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}", response_model=HistoryResponse)
async def get_history_endpoint(session_id: str):
    """
    Retrieves the full chat history for a specific session.
    """
    try:
        history_objs = get_history(session_id)
        # Convert SQLAlchemy objects to our Pydantic MessageHistory model
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
