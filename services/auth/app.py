from resources.category import Category, CategoryList
from resources.job import Job, JobList
from resources.auth import UserRegister, UserCheckVerification, UserResendVerification
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from marshmallow import ValidationError

from models.category import CategoryModel
from db import db
from ma import ma
from config import Config
import json
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
api = Api(app)
jwt = JWTManager(app)
db.init_app(app)
ma.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


api.add_resource(CategoryList, "/categories", endpoint="categories")
api.add_resource(Category, "/categories/<string:slug>", endpoint="category")
api.add_resource(JobList, "/jobs", endpoint="jobs")
api.add_resource(Job, "/jobs/<string:slug>", endpoint="job")
api.add_resource(UserRegister, "/auth/register")
api.add_resource(UserCheckVerification, '/auth/verify')
api.add_resource(UserResendVerification, '/auth/resend')

"""
if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000)
"""