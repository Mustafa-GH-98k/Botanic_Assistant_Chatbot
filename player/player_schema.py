from marshmallow import Schema, fields

class PlayerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    age = fields.Int(required=True)
    team = fields.Str(required=True)
