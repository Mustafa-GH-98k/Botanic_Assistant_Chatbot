from flask import jsonify, request
from .chatbot_service import ChatbotService
from .chatbot_schema import *

def chat():
    return jsonify("chat")

def generateImage():
    return jsonify("generate image")
