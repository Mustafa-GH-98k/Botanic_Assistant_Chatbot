from flask import jsonify
from flasgger import swag_from

@swag_from({
    'responses': {
        200: {
            'description': 'A simple greeting message',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {
                                'type': 'string',
                                'example': 'Hello, World!'
                            }
                        }
                    }
                }
            }
        }
    }
})
def hello():
    """Returns a simple greeting."""
    return jsonify(message="Hello, World!")

@swag_from({
    'parameters': [
        {
            'name': 'name',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'example': 'John'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'A personalized greeting message',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {
                                'type': 'string',
                                'example': 'Hello, John!'
                            }
                        }
                    }
                }
            }
        }
    }
})
def greet(name):
    """Returns a personalized greeting."""
    return jsonify(message=f"Hello, {name}!")
