from flask import Flask
from player.player_routes import register_routes

app = Flask(__name__)

# Register Blueprints (services)
register_routes(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True)

