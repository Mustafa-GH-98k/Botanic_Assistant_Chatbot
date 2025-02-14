import secrets
from flask import Flask, jsonify
from chatbot.chatbot_routes import chatbot_bp

# GET : /
#POST : /chat  /generateImage

app = Flask(__name__)
app.register_blueprint(chatbot_bp, url_prefix="/chatbot")

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True)

