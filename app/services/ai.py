import google.generativeai as genai
from app.config import settings
from typing import List, Any

# 1. Configure the Gemini API
# We use the key loaded from our .env file via settings
genai.configure(api_key=settings.GEMINI_API_KEY)

# 2. Initialize the Model
# 'gemini-2.5-flash' is a fast and efficient model, perfect for chatbots
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_ai_response(history_context: List[Any], user_message: str) -> str:
    """
    Generates a response from the Gemini AI model.
    
    Args:
        history_context: A list of SQLAlchemy objects from the database.
        user_message: The latest message from the user.
        
    Returns:
        The text response from the AI.
    """
    # Gemini expects history in a specific format:
    # [{'role': 'user', 'parts': ['message']}, {'role': 'model', 'parts': ['message']}]
    # Note: Gemini uses 'model' instead of 'assistant'
    formatted_history = []
    
    for msg in history_context:
        # Map 'assistant' to 'model' for Gemini compatibility
        role = "user" if msg.role == "user" else "model"
        formatted_history.append({
            "role": role,
            "parts": [msg.content]
        })
    
    try:
        # Start a chat session with the existing history
        chat_session = model.start_chat(history=formatted_history)
        
        # Send the user's latest message and get the response
        response = chat_session.send_message(user_message)
        
        # Return the generated text
        return response.text
        
    except Exception as e:
        # Basic error handling for API issues
        return f"Error generating AI response: {str(e)}"
