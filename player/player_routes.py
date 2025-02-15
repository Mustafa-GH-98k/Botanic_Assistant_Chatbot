from flask import Blueprint
from .player_controller import get_players, create_player

player_bp = Blueprint("player", __name__)

player_bp.route("/", methods=["GET"])(get_players)
player_bp.route("/", methods=["POST"])(create_player)


