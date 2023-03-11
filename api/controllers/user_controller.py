from ..models.user_model import User, user_schema, users_schema
from flask_restful import Resource
from ..app.extensions import db, api, guard
from flask import request
from flask_restful import Resource


class ResourceUsers(Resource):
    def get(self):
        user = User.query.all()
        return users_schema.dump(user)


class ResourceUser(Resource):
    def get(self, id_user):
        user = User.query.get_or_404(id_user)
        return user_schema.dump(user)


api.add_resource(ResourceUsers, '/api/users/')
api.add_resource(ResourceUser, '/api/users/<int:id_user>/')
