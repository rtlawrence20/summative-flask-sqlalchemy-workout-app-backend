# app.py
from flask import Flask, make_response
from flask_migrate import Migrate

from .models import db  # TODO: add other models as they are created

app = Flask(__name__)

# Basic assignment of config variables
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Define routes

if __name__ == "__main__":
    app.run(port=5555, debug=True)
