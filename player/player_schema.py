from marshmallow import Schema, fields, validate

class PlayerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    score = fields.Int(required=True, validate=validate.Range(min=0))

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)
