chat_doc = {
    'tags': ['chatbot'],
    'parameters': [
        {
            'name': 'x-api-key',
            'in': 'header',
            'required': True,
            'description': 'API key for authentication',
            'schema': {
                'type': 'string',
                'example': 'your-api-key-here'
            }
        },
        {
            'name': 'content',
            'in': 'body',
            'required': True,
            'description': 'The content to send to the chatbot',
            'schema': {
                'type': 'object',
                'properties': {
                    'content': {
                        'type': 'string',
                        'example': 'Hello, chatbot!'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Successful chat response',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status_code': {
                                'type': 'integer',
                                'example': 200
                            },
                            'success': {
                                'type': 'boolean',
                                'example': True
                            },
                            'response': {
                                'type': 'string',
                                'example': 'Chatbot response here'
                            }
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad request due to validation errors',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status_code': {
                                'type': 'integer',
                                'example': 400
                            },
                            'success': {
                                'type': 'boolean',
                                'example': False
                            },
                            'error_messages': {
                                'type': 'array',
                                'items': {
                                    'type': 'string',
                                    'example': 'Validation error message here'
                                }
                            }
                        }
                    }
                }
            }
        },
        500: {
            'description': 'Internal Server Error',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status_code': {
                                'type': 'integer',
                                'example': 500
                            },
                            'success': {
                                'type': 'boolean',
                                'example': False
                            },
                            'error_messages': {
                                'type': 'array',
                                'items': {
                                    'type': 'string',
                                    'example': 'Internal Server Error'
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

generate_image_doc = {
    'tags': ['chatbot'],
    'parameters': [
        {
            'name': 'x-api-key',
            'in': 'header',
            'required': True,
            'description': 'API key for authentication',
            'schema': {
                'type': 'string',
                'example': 'your-api-key-here'
            }
        },
        {
            'name': 'imageType',
            'in': 'header',
            'required': True,
            'description': 'The type of image to generate. Can be "base64" or "image".',
            'schema': {
                'type': 'string',
                'enum': ['base64', 'image'],
                'example': 'base64'
            }
        },
        {
            'name': 'content',
            'in': 'body',
            'required': True,
            'description': 'The content to generate the image from.',
            'schema': {
                'type': 'object',
                'properties': {
                    'content': {
                        'type': 'string',
                        'example': 'Generate an image based on this text.'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Successful image generation response',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status_code': {
                                'type': 'integer',
                                'example': 200
                            },
                            'success': {
                                'type': 'boolean',
                                'example': True
                            },
                            'response': {
                                'type': 'object',
                                'properties': {
                                    'base64': {
                                        'type': 'string',
                                        'example': 'data:image/png;base64,...'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad request due to validation errors',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status_code': {
                                'type': 'integer',
                                'example': 400
                            },
                            'success': {
                                'type': 'boolean',
                                'example': False
                            },
                            'error_messages': {
                                'type': 'array',
                                'items': {
                                    'type': 'string',
                                    'example': 'Validation error message here'
                                }
                            }
                        }
                    }
                }
            }
        },
        500: {
            'description': 'Internal Server Error',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status_code': {
                                'type': 'integer',
                                'example': 500
                            },
                            'success': {
                                'type': 'boolean',
                                'example': False
                            },
                            'error_messages': {
                                'type': 'array',
                                'items': {
                                    'type': 'string',
                                    'example': 'Internal Server Error'
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

generate_api_key_doc = {
    'tags': ['chatbot'],
    'responses': {
        200: {
            'description': 'Successfully generated new API key',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'api_key': {
                                'type': 'string',
                                'example': 'd2f8f1c6e69b6d6fd937d32dbb5c8aeb'
                            }
                        }
                    }
                }
            }
        }
    }
}
