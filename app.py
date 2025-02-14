from flask import Flask
from player.player_routes import player_bp

app = Flask(__name__)

# Register Blueprints (services)
app.register_blueprint(player_bp, url_prefix="/players")

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True)

