from flask_restx import Api
from .player_controller import create_player_namespace

def register_routes(app):
    api = Api(app, title="Player API", version="1.0", description="API for managing players")
    api.add_namespace(create_player_namespace(api))
