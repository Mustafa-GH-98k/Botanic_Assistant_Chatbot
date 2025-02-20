from unittest.mock import patch


def test_hello_world(client):
    """Test the root endpoint (/) to ensure it returns a 200 status code and the expected 'Hello, World!' response."""

    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'Hello, World!'


def test_generate_api_key(client, api_keys_fixture):
    """Test the /chatbot/generate, ApiKey endpoint."""
    response = client.get("/chatbot/generateApiKey")  
    data = response.get_json()  

    assert response.status_code == 200  
    assert "api_key" in data  
    assert isinstance(data["api_key"], str)  
    assert len(data["api_key"]) == 32  
    assert data["api_key"] in api_keys_fixture  


def test_chat_success(client, api_keys_fixture):
    """Test /chat with valid API key and valid request."""

    with patch("Services.chatbot_service.ChatbotService.chat") as mock_generate_image:
        mock_generate_image.return_value = "mocked chatbot response"

        valid_api_key = client.get("/chatbot/generateApiKey").get_json()["api_key"]
        print(api_keys_fixture)
        response = client.post(
            "/chatbot/chat",
            json={"content": "Hello, chatbot!"},
            headers={"x-api-key": valid_api_key},
        )

        data = response.get_json()
        assert response.status_code == 200
        assert data["success"] is True
        assert "response" in data  


def test_chat_missing_api_key(client):
    """Test /chatbot/chat without an API key (should return 401)."""
    response = client.post(
        "/chatbot/chat",
        json={"content": "Hello!"},  
    )

    assert response.status_code == 401
    assert "error_messages" in response.get_json()

def test_chat_invalid_api_key(client):
    """Test /chatbot/chat with an invalid API key (should return 403)."""
    response = client.post(
        "/chatbot/chat",
        json={"content": "Hello!"},
        headers={"x-api-key": "invalid_key"},
    )

    assert response.status_code == 403
    assert "error_messages" in response.get_json()


def test_chat_invalid_request_data(client, api_keys_fixture):
    """Test /chatbot/chat with invalid JSON body (should return 400)."""
    valid_api_key = client.get("/chatbot/generateApiKey").get_json()["api_key"]

    response = client.post(
        "/chatbot/chat",
        json={},  
        headers={"x-api-key": valid_api_key},
    )

    assert response.status_code == 400
    assert "error_messages" in response.get_json()


def test_chat_internal_error(client, api_keys_fixture):
    """Test /chatbot/chat when chatbot service fails should return 500."""
    response = client.get("/chatbot/generateApiKey")
    api_key = response.get_json()["api_key"]

    headers = {"x-api-key": api_key}
    data = {"content": "Hello, chatbot!"}

    with patch("Services.chatbot_service.ChatbotService.chat", side_effect=Exception("Chatbot failure")):
        response = client.post("/chatbot/chat", json=data, headers=headers)
        response_data = response.get_json()

        assert response.status_code == 500
        assert response_data["success"] is False
        assert "error_messages" in response_data

