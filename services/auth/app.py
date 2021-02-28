from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_cors import CORS
from marshmallow import ValidationError

from db import db
from ma import ma
from config import Config
from errors import errors
from routes import initialize_routes

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app, errors=errors)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

CORS(app)

"""
db.init_app(app)
ma.init_app(app)
"""


@app.before_first_request
def create_tables():
    db.drop_all()
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


initialize_routes(api)


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000)
