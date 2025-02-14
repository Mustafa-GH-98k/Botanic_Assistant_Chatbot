from flask import jsonify, request, send_file
import logging
from marshmallow import ValidationError

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
        return jsonify({"response": response})
    
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    
    except ServiceException as e:
        return jsonify({"error": str(e)}), e.status_code

    except Exception as e:
        logging.exception("An unexpected error occurred") 
        return jsonify({"error": "Internal Server Error"}), 500


def generateImage():
    schema = GenerateImageRequestSchema()

    try:
        data = schema.load(request.json) 

        image_type = request.headers.get("imageType")  
        if not image_type:
            return jsonify({"error": "imageType header is required"}), 400
        
        chatbot = ChatbotService()
        response = chatbot.generate_image(data["content"], image_type)
  
        if image_type == "base64":
            return jsonify({"base64": response})

        if image_type == "image":
            return send_file(
                response,
                mimetype='image/png',
                as_attachment=True,
                download_name='generated_image.png'
            )
    
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    
    except ServiceException as e:
        return jsonify({"error": str(e)}), e.status_code

    except Exception as e:
        logging.exception("An unexpected error occurred") 
        return jsonify({"error": "Internal Server Error"}), 500
