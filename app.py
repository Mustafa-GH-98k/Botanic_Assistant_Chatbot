from flask import Flask
from player.player_routes import register_routes
from flask_restx import Api

app = Flask(__name__)

# api = Api(app, title="Player API", version="1.0", description="API for managing players")
# Register Blueprints (services)
register_routes(app)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True)

