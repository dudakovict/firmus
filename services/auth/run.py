from flask import jsonify
from marshmallow import ValidationError
from models import db
from app import create_app

app = create_app()

@app.before_first_request
def create_tables():
    db.drop_all()
    db.create_all()

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

if __name__ == "__main__":
    app.run(port=5000, use_reloader=False)
