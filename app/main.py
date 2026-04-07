from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routes.chat import router as chat_router
from app.services.memory import Base, engine
from app.config import settings

# 1. Initialize the Rate Limiter
# This will track requests based on the client's IP address.
limiter = Limiter(key_func=get_remote_address)

# 2. Initialize the FastAPI Application
app = FastAPI(
    title=settings.APP_NAME,
    description="A ChatGPT-style conversational AI chatbot with persistent memory.",
    version="1.0.0"
)

# Attach the limiter to the app and its error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 3. Database Initialization
# This ensures that the 'chat_history' table is created in PostgreSQL 
# as soon as the application starts up.
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# 3. Include Routers
# We add the chat, history, and health endpoints we built in the previous step.
app.include_router(chat_router)

# 4. Root Endpoint
@app.get("/")
async def root():
    """
    A simple welcome message at the root URL.
    """
    return {
        "message": f"Welcome to the {settings.APP_NAME} API!",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    # This allows running the app directly with 'python app/main.py'
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
