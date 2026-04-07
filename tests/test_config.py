from app.config import settings

def test_app_name():
    """
    Checks if the app name is correctly loaded.
    """
    assert settings.APP_NAME == "AI Chatbot"

def test_database_url_format():
    """
    Checks if the database URL is constructed correctly.
    """
    # The URL should always start with postgresql://
    assert settings.DATABASE_URL.startswith("postgresql://")
    # It should also contain the DB_NAME we specified in .env
    assert settings.DB_NAME in settings.DATABASE_URL
