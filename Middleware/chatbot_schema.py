from marshmallow import Schema, fields , validate

class ChatRequestSchema(Schema):
    content = fields.String(required=True, error_messages={"required": "Content is required."})

class GenerateImageRequestSchema(Schema):
    content = fields.String(required=True, error_messages={"required": "Content is required."})
