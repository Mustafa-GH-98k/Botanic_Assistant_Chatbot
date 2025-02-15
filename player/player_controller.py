from flask import jsonify, request
from .player_service import PlayerService
from .player_schema import PlayerSchema

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)

def get_players():
    players = PlayerService.get_all_players()
    return jsonify(players_schema.dump(players))

def create_player():
    """
    Create a new player.
    ---
    parameters:
      - name: player
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            age:
              type: integer
            team:
              type: string
    responses:
      201:
        description: Player created
        schema:
          $ref: '#/definitions/Player'
    """
    data = request.get_json()
    errors = player_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    new_player = PlayerService.add_player(data)
    return jsonify(player_schema.dump(new_player)), 201

swagger_definitions = {
    'Player': {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'name': {'type': 'string'},
            'age': {'type': 'integer'},
            'team': {'type': 'string'}
        }
    }
}