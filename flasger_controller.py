from flask import jsonify
from flasgger import swag_from
from flasger_docs import *

@swag_from(hello_doc)
def hello():
    """Returns a simple greeting."""
    return jsonify(message="Hello, World!")

@swag_from(greet_doc)
def greet(name):
    """Returns a personalized greeting."""
    return jsonify(message=f"Hello, {name}!")
