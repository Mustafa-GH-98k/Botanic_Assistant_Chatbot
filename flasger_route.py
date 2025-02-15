from flask import Blueprint
from flasger_controller import hello, greet

greeting_bp = Blueprint("greeting", __name__)

# Register the routes with the blueprint
greeting_bp.route('/hello', methods=["GET"])(hello)
greeting_bp.route('/greet', methods=["POST"])(greet)
