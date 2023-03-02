
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
import flask_praetorian
# from flask_restx import Api

db = SQLAlchemy()
ma = Marshmallow()
api = Api()
guard = flask_praetorian.Praetorian()
