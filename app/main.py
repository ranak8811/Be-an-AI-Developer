from fastapi import FastAPI
from app.routes.chat import router as chat_router
from app.services.memory import Base, engine
from app.config import settings

# 1. Initialize the FastAPI Application
app = FastAPI(
    title=settings.APP_NAME,
    description="A ChatGPT-style conversational AI chatbot with persistent memory.",
    version="1.0.0"
)

# 2. Database Initialization
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
