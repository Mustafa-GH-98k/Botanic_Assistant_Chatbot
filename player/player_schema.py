from flask_restx import fields

def get_player_model(api):
    return api.model("Player", {
        "id": fields.Integer(description="Player ID"),
        "name": fields.String(required=True, description="Player Name"),
        "score": fields.Integer(description="Player Score")
    })

def get_player_input_model(api):
    return api.model("PlayerInput", {
        "name": fields.String(required=True, description="Player Name"),
        "score": fields.Integer(description="Initial Score")
    })
