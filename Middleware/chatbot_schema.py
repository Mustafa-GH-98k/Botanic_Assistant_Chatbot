from marshmallow import Schema, fields , validate

# Schemas for validating requests to chatbot endpoints
# These are used to parse and validate the JSON payload of
# incoming requests, and to generate documentation for the API

class ChatRequestSchema(Schema):
    # Request body for chat endpoint
    # This endpoint takes a single string parameter "content"
    # and returns a response from the chatbot
    content = fields.String(required=True, error_messages={"required": "Content is required."})

class GenerateImageRequestSchema(Schema):
    # Request body for generateImage endpoint
    # This endpoint takes a single string parameter "content"
    # and returns an image generated from the content
    content = fields.String(required=True, error_messages={"required": "Content is required."})
