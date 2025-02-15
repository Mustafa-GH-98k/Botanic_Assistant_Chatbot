import io
from marshmallow import ValidationError
import pytest
from unittest.mock import patch
import logging


def test_generate_image_base64_success(client, api_keys_fixture):
    """Test /generateImage with valid API key and base64 image type."""

    # Mock the generate_image method to return a base64 response
    with patch("chatbot.chatbot_service.ChatbotService.generate_image") as mock_generate_image:
        mock_generate_image.return_value = "mocked_base64_image_data"

        # Get the valid API key by generating it
        valid_api_key = client.get("/chatbot/generateApiKey").get_json()["api_key"]
        
        # Make a POST request to /generateImage with base64 type
        response = client.post(
            "/chatbot/generateImage",
            json={"content": "generate a base64 image"},
            headers={"x-api-key": valid_api_key, "imageType": "base64"},
        )

        # Assert the response is as expected
        data = response.get_json()
        assert response.status_code == 200
        assert data["success"] is True
        assert "base64" in data["response"]


def test_generate_image_image_success(client, api_keys_fixture):
    """Test /generateImage with valid API key and image type."""

    # Mock the generate_image method to return an image response
    with patch("chatbot.chatbot_service.ChatbotService.generate_image") as mock_generate_image:
        mock_generate_image.return_value = io.BytesIO(b"mocked_image_data")  # Image data

        # Get the valid API key by generating it
        valid_api_key = client.get("/chatbot/generateApiKey").get_json()["api_key"]
        
        # Make a POST request to /generateImage with image type
        response = client.post(
            "/chatbot/generateImage",
            json={"content": "generate an image"},
            headers={"x-api-key": valid_api_key, "imageType": "image"},
        )

        # Assert the response is as expected
        assert response.status_code == 200
        assert response.mimetype == 'image/png'
        assert response.headers["Content-Disposition"] == 'attachment; filename=generated_image.png'


def test_generate_image_invalid_image_type(client, api_keys_fixture):
    """Test /generateImage with invalid image type."""

    # Get the valid API key by generating it
    valid_api_key = client.get("/chatbot/generateApiKey").get_json()["api_key"]

    # Make a POST request to /generateImage with an invalid image type
    response = client.post(
        "/chatbot/generateImage",
        json={"content": "generate an image"},
        headers={"x-api-key": valid_api_key, "imageType": "invalid_type"},
    )

    # Assert the response is a validation error
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] is False
    assert "error_messages" in data


def test_generate_image_missing_image_type(client, api_keys_fixture):
    """Test /generateImage with missing imageType header."""

    # Get the valid API key by generating it
    valid_api_key = client.get("/chatbot/generateApiKey").get_json()["api_key"]

    # Make a POST request to /generateImage without imageType
    response = client.post(
        "/chatbot/generateImage",
        json={"content": "generate an image"},
        headers={"x-api-key": valid_api_key},
    )

    # Assert the response is a validation error
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] is False
    assert "error_messages" in data


def test_generate_image_invalid_api_key(client, api_keys_fixture):
    """Test /generateImage with invalid API key."""

    # Get an invalid API key (we use a random string here for testing)
    invalid_api_key = "invalid_api_key"

    # Make a POST request to /generateImage with the invalid API key
    response = client.post(
        "/chatbot/generateImage",
        json={"content": "generate an image"},
        headers={"x-api-key": invalid_api_key, "imageType": "base64"},
    )

    assert response.status_code == 403


def test_generate_image_validation_error(client, api_keys_fixture):
    """Test /generateImage with schema validation errors."""

    # Mock the schema loading to raise a validation error


    # Get the valid API key by generating it
    valid_api_key = client.get("/chatbot/generateApiKey").get_json()["api_key"]

    # Make a POST request to /generateImage with invalid data
    response = client.post(
    "/chatbot/generateImage",
    json={"wrong_field": "invalid data"},  # This will trigger schema validation error
    headers={"x-api-key": valid_api_key, "imageType": "base64"},
    )

    # Assert the response is a validation error
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] is False
    assert "error_messages" in data


def test_generate_image_unexpected_error(client, api_keys_fixture , caplog, capsys):
    """Test /generateImage with an unexpected error."""

    # Mock the generate_image method to raise an exception
    with patch("chatbot.chatbot_service.ChatbotService.generate_image") as mock_generate_image:
        mock_generate_image.side_effect = Exception("Unexpected error")

        # Get the valid API key by generating it
        valid_api_key = client.get("/chatbot/generateApiKey").get_json()["api_key"]

        # Make a POST request to /generateImage
        response = client.post(
            "/chatbot/generateImage",
            json={"content": "generate an image"},
            headers={"x-api-key": valid_api_key, "imageType": "base64"},
        )

        # Assert the response is a generic server error
        data = response.get_json()
        assert response.status_code == 500
        assert data["success"] is False
        assert "error_messages" in data

        #read error
        # Capture the log output and assert it contains the expected log message
        captured_log = caplog.text
        assert "Unexpected error" in captured_log # Ensure the exception message is logged

        # Capture and print everything that was printed to stdout
        # captured_stdout = capsys.readouterr()
        # print("Captured prints:\n", captured_stdout.out)
