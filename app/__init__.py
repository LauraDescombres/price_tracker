from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Price Tracker fonctionne !"

    return app