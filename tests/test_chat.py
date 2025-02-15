from unittest.mock import patch


def test_hello_world(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'Hello, World!'


def test_generate_api_key(client, api_keys_fixture):
    """Test the /chatbot/generate, ApiKey endpoint."""
    response = client.get("/chatbot/generateApiKey")  # Make a GET request
    data = response.get_json()  # Parse the JSON response

    assert response.status_code == 200  # Ensure response is OK
    assert "api_key" in data  # Ensure response contains the API key
    assert isinstance(data["api_key"], str)  # Ensure API key is a string
    assert len(data["api_key"]) == 32  # Ensure it's a 32-character hex string
    assert data["api_key"] in api_keys_fixture  # Ensure API key is stored in the set


def test_chat_success(client, api_keys_fixture):
    """Test /chat with valid API key and valid request."""

    with patch("chatbot.chatbot_service.ChatbotService.chat") as mock_generate_image:
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
        json={"content": "Hello!"},  # Valid JSON
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
        json={},  # Missing "content"
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

    with patch("chatbot.chatbot_service.ChatbotService.chat", side_effect=Exception("Chatbot failure")):
        response = client.post("/chatbot/chat", json=data, headers=headers)
        response_data = response.get_json()

        assert response.status_code == 500
        assert response_data["success"] is False
        assert "error_messages" in response_data

