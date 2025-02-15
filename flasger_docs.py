hello_doc = {
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
}

greet_doc = {
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
}