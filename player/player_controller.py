from flask_restx import Resource, fields, Namespace
from marshmallow import ValidationError
from .player_service import PlayerService
from .player_schema import player_schema, players_schema

# Define the Flask-RESTx API namespace
def create_player_namespace(api):
    ns = api.namespace("players", description="Player operations")

    # POST /players
    @ns.route("/")
    class PlayerList(Resource):
        def get(self):
            """Get all players"""
            players = PlayerService.get_all_players()
            return players_schema.dump(players)

        @ns.doc("create_player")
        @ns.expect(player_schema, validate=True)  # <-- Add the Marshmallow schema to expect
        @ns.marshal_with(player_schema, code=201)
        def post(self):
            """Create a new player"""
            # Validate the incoming request data using Marshmallow
            try:
                data = player_schema.load(ns.payload)  # Validate incoming JSON body
            except ValidationError as err:
                return {"message": "Invalid data", "errors": err.messages}, 400

            # Pass the validated data to your service layer
            return PlayerService.add_player(data), 201

    return ns
