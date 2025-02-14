from flask import jsonify, request
from .chatbot_service import ChatbotService
from .chatbot_schema import *

def chat():
    return jsonify("chat")

def generateImage():
    return jsonify("generate image")
    # return send_file(img, mimetype='image/png') --> use in controller
