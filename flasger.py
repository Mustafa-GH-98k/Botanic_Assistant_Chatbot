from flask import Flask
from flasgger import Swagger
from flasger_route import greeting_bp

app = Flask(__name__)
swagger = Swagger(app)

# Register the Blueprint
app.register_blueprint(greeting_bp)

if __name__ == '__main__':
    app.run(debug=True)
