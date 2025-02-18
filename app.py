import os
import secrets
import tempfile
from flask import Flask, jsonify
from flasgger import Swagger
from flask_cors import CORS
from chatbot.chatbot_routes import chatbot_bp
from flasgger import swag_from

gcloud_json_file_path = os.environ["GCOULD_TEXT_CREDENTIALS_PATH"]

if os.path.exists(gcloud_json_file_path):
    
    with open(gcloud_json_file_path, "r") as file:
        gcloud_json_str = file.read()

    
    temp_json_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    with open(temp_json_file.name, "w") as temp_file:
        temp_file.write(gcloud_json_str)

    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_json_file.name
else:
    raise ValueError("Google Cloud credentials file not found!")

# GET : /
#POST : /chat  /generateImage

app = Flask(__name__)
CORS(app)  

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
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

