import time
from flask import Flask
from .extensions import db, ma, api, guard
from api.controllers.artist_controller import *
from api.controllers.user_controller import *
from api.models.user_model import User
import os


def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["JWT_ACCESS_LIFESPAN"] = {"hours": 24}
    app.config["JWT_REFRESH_LIFESPAN"] = {"days": 30}
    guard.init_app(app, User)
    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)

    with app.app_context():
        db.create_all()
    return app

# app = create_app()
# ma = Marshmallow(app)
# api = Api(app)
