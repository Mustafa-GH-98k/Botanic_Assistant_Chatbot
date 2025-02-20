import secrets
from flask import jsonify, request, send_file
import logging
from marshmallow import ValidationError

from Middleware.authenticate_api_key import authenticate_api_key
from Middleware.validate_headers import validate_headers
from Models.api_response import ApiResponse
from Models.service_exception import ServiceException
from Services.chatbot_service import ChatbotService
from Middleware.chatbot_schema import *
from flasgger import swag_from
from Config.swagger_docs import *


api_keys = {"test"}  # FOR TESTING - NON PRODUCTION
lambda: list(api_keys)

logging.basicConfig(level=logging.ERROR)

@swag_from(chat_doc)
@authenticate_api_key(
    api_header='x-api-key',
    valid_apikeys_getter=lambda: list(api_keys)
)
def chat():
    """Handle chat requests.

    Processes a chat request and returns the chatbot's response.

    Returns:
        ApiResponse: A JSON response containing the chatbot's reply.

    Raises:
        ValidationError: If the request data fails schema validation.
        ServiceException: If there is an error in the chat process.
        Exception: For any unexpected errors.
    """
    schema = ChatRequestSchema()

    try:
        data = schema.load(request.json)
        chatbot = ChatbotService()
        response = chatbot.chat(data["content"], "user_session")

        return ApiResponse(
            status_code=200,
            success=True,
            response=response
        ).to_json()

    except ValidationError as e:
        return ApiResponse(
            status_code=400,
            success=False,
            error_messages=[e.messages] if isinstance(e.messages, dict) else e.messages
        ).to_json()

    except ServiceException as e:
        return ApiResponse(
            status_code=e.status_code,
            success=False,
            error_messages=[str(e)]
        ).to_json()

    except Exception as e:
        logging.exception("An unexpected error occurred")
        return ApiResponse(
            status_code=500,
            success=False,
            error_messages=["Internal Server Error"]
        ).to_json()

@swag_from(generate_image_doc)
@authenticate_api_key(
    api_header='x-api-key',
    valid_apikeys_getter=lambda: list(api_keys)
)
@validate_headers(
    required_headers=['imageType'],
    allowed_values={
        'imageType': ['base64', 'image'],
    }
)
def generateImage():
    """Generate an image based on input content.

    Processes image generation requests and returns the image in the specified format.

    Returns:
        ApiResponse: A JSON response containing base64 image data or an image file.

    Raises:
        ValidationError: If the request data fails schema validation.
        ServiceException: If there is an error in the image generation process.
        Exception: For any unexpected errors.

    """
    schema = GenerateImageRequestSchema()

    try:
        data = schema.load(request.json)

        image_type = request.headers.get("imageType")

        chatbot = ChatbotService()
        response = chatbot.generate_image(data["content"], image_type)

        if image_type == "base64":
            return ApiResponse(
                status_code=200,
                success=True,
                response={"base64": response},
            ).to_json()

        if image_type == "image":
            return send_file(
                response,
                mimetype='image/png',
                as_attachment=True,
                download_name='generated_image.png'
            )

    except ValidationError as e:
        return ApiResponse(
            status_code=400,
            success=False,
            error_messages=[e.messages] if isinstance(e.messages, dict) else e.messages
        ).to_json()

    except ServiceException as e:
        return ApiResponse(
            status_code=e.status_code,
            success=False,
            error_messages=[str(e)]
        ).to_json()

    except Exception as e:
        logging.exception("An unexpected error occurred")
        return ApiResponse(
            status_code=500,
            success=False,
            error_messages=["Internal Server Error"]
        ).to_json()

@swag_from(generate_api_key_doc)
def generateApiKey():
    """Generate a new API key for testing.

    Generates a new API key and adds it to the set of valid keys.

    Returns:
        Response: A JSON response containing the new API key.

    """
    new_key = secrets.token_hex(16)
    api_keys.add(new_key)
    return jsonify({"api_key": new_key})
