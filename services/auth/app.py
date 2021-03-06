import config
from flask import Flask
from flask_cors import CORS
from models import db, bcrypt
from schemas import ma
from resources import api
from decorators import jwt, metrics

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)
    api.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    metrics.init_app(app, api)
    return app
