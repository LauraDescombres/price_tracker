from flask import Flask
from app.config import secret_key
from app.routes import bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.secret_key = secret_key

    return app