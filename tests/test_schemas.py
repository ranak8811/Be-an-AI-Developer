from app.models.schemas import ChatRequest
import pytest
from pydantic import ValidationError

def test_chat_request_valid():
    """
    Checks if valid data is accepted.
    """
    data = {"session_id": "test_1", "message": "hello"}
    request = ChatRequest(**data)
    assert request.session_id == "test_1"
    assert request.message == "hello"

def test_chat_request_missing_field():
    """
    Checks if an error is raised when a field is missing.
    """
    with pytest.raises(ValidationError):
        # Missing 'message'
        ChatRequest(session_id="test_1")
