import secrets
from flask import Flask, jsonify
from flasgger import Swagger
from chatbot.chatbot_routes import chatbot_bp
from flasgger import swag_from

# GET : /
#POST : /chat  /generateImage

app = Flask(__name__)

swagger = Swagger(app  )

app.register_blueprint(chatbot_bp, url_prefix="/chatbot")

@app.route('/')
@swag_from({
    'responses': {
        200: {
            'description': 'Hello, World! response',
            'content': {
                'text/plain': {
                    'schema': {
                        'type': 'string',
                        'example': 'Hello, World!'
                    }
                }
            }
        }
    }
})
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True)

