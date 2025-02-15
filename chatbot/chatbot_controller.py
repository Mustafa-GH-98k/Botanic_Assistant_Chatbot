import secrets
from flask import jsonify, request, send_file
import logging
from marshmallow import ValidationError

from Global.authenticate_api_key import authenticate_api_key
from Global.validate_headers import validate_headers
from Global.Models.api_response import ApiResponse
from chatbot.chatbot_exceptions import ServiceException
from .chatbot_service import ChatbotService
from .chatbot_schema import *
from flasgger import swag_from
from chatbot.chatbot_docs import *

api_keys = {"test"} ## FOR TESTING - NON PRODUCTION
lambda: list(api_keys) 

logging.basicConfig(level=logging.ERROR)

@swag_from(chat_doc)
@authenticate_api_key(
    api_header='x-api-key',
    valid_apikeys_getter= lambda: list(api_keys) 
)
def chat():
    schema = ChatRequestSchema()

    try:
        data = schema.load(request.json)
        chatbot = ChatbotService()
        response = chatbot.chat(data["content"])

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
    valid_apikeys_getter= lambda: list(api_keys) 
)
@validate_headers(
    required_headers=['imageType'],
    allowed_values={
        'imageType': ['base64', 'image'],
    }
)
def generateImage():
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
def generateApiKey(): ## FOR TESTING - NON PRODUCTION
    new_key = secrets.token_hex(16) 
    api_keys.add(new_key)
    return jsonify({"api_key": new_key})