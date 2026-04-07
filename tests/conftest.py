import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """
    Returns a FastAPI TestClient. 
    This allows us to simulate sending requests to our API.
    """
    with TestClient(app) as c:
        yield c
