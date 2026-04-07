from unittest.mock import patch

def test_health_check(client):
    """
    Checks if the GET /health endpoint returns 'ok'.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root_endpoint(client):
    """
    Checks if the root / endpoint returns a welcome message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_chat_endpoint_mock(client):
    """
    Tests the chat endpoint using a mock for the AI response.
    This prevents real (and slow) calls to the Gemini API during testing.
    """
    # Use a 'patch' to temporarily replace our AI response logic
    with patch("app.routes.chat.generate_ai_response") as mock_ai:
        # Set what we want the 'fake' AI to say
        mock_ai.return_value = "This is a mock response from the AI."
        
        # Call our endpoint
        response = client.post("/chat", json={"session_id": "test_1", "message": "Hi!"})
        
        # Verify the result
        assert response.status_code == 200
        assert response.json()["reply"] == "This is a mock response from the AI."
        
        # Check if our mock function was actually called
        mock_ai.assert_called_once()
