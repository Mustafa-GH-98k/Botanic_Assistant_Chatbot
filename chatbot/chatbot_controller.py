from flask import jsonify, request, send_file
import logging
from marshmallow import ValidationError

from Global.Models.api_response import ApiResponse
from chatbot.chatbot_exceptions import ServiceException
from .chatbot_service import ChatbotService
from .chatbot_schema import *

# TODO :
# make an api response model
# add authentication with a randomly generated key
logging.basicConfig(level=logging.ERROR)


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
            error_messages=[str(e)]  # Always wrap in a list
        ).to_json()

    except Exception as e:
        logging.exception("An unexpected error occurred")  
        return ApiResponse(
            status_code=500,
            success=False,
            error_messages=["Internal Server Error"]
        ).to_json()


def generateImage():
    schema = GenerateImageRequestSchema()

    try:
        data = schema.load(request.json) 

        image_type = request.headers.get("imageType")  
        if not image_type:
            return ApiResponse(
                status_code=400,
                success=False,
                error_messages=["imageType header is required"],
            ).to_json()

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