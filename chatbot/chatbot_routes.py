from flask import Blueprint
from .chatbot_controller import *

chatbot_bp = Blueprint("chatbot", __name__)

chatbot_bp.route("/chat", methods=["POST"])(chat)
chatbot_bp.route("/generateImage", methods=["POST"])(generateImage)
chatbot_bp.route("/generateApiKey", methods=["GET"])(generateApiKey) ## FOR TESTING - NON PRODUCTION

