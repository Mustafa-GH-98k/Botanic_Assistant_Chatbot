from flask import Flask, request
from flask_restx import Api, Resource, fields
from marshmallow import Schema, fields as marshmallow_fields, ValidationError

app = Flask(__name__)
api = Api(app, version="1.0", title="My API", description="A simple API", doc="/swagger")

# Define Marshmallow schema for validation
class MessageSchema(Schema):
    message = marshmallow_fields.String(required=True, description="The greeting message")

# Define Swagger model for response documentation (if you're not using marshal_with)
message_model = api.model('Message', {
    'message': fields.String(description='The greeting message')
})

@api.route('/hello')
class HelloWorld(Resource):
    """Endpoint to say hello"""
    
    @api.doc(description="This endpoint returns a greeting message.")
    @api.param('message', 'The message to return', type='string', required=True)
    def post(self):
        """POST request to return a greeting message"""

        # Custom validation using Marshmallow
        schema = MessageSchema()
        try:
            data = schema.load(request.json)  # Validate incoming JSON data
        except ValidationError as err:
            return {'message': err.messages}, 400  # Return validation errors as a response

        # Respond with the message
        return {'message': data['message']}

if __name__ == "__main__":
    app.run(debug=True)
