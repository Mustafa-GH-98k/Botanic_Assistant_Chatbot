from flask import jsonify, request
from .player_service import PlayerService
from .player_schema import get_player_model, get_player_input_model
from flask_restx import Resource

def create_player_namespace(api):
    ns = api.namespace("players", description="Player operations")

    player_model = get_player_model(api)
    player_input_model = get_player_input_model(api)

    @ns.route("/")
    class PlayerList(Resource):
        @ns.doc("list_players")
        @ns.marshal_list_with(player_model)
        def get(self):
            """List all players"""
            return PlayerService.get_all_players()

        @ns.doc("create_player")
        @ns.expect(player_input_model, validate=True)
        @ns.marshal_with(player_model, code=201)
        def post(self):
            """Create a new player"""
            return PlayerService.add_player(ns.payload), 201

    return ns

