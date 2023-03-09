
from flask_restful import Resource
from ..app.extensions import db, api, guard
from flask import request
from flask_restful import Resource
import flask_praetorian


class ResourceRecommendations(Resource):
    # @flask_praetorian.auth_required
    def get(self):
        return [{
            "username": "Chopin",
            "id": 1,
            "roles": "{user}"
        },
            {
            "username": "Johann Sebastian Bach",
            "id": 2,
            "roles": "{admin,user}"
        },
            {
            "username": "The Beatles",
            "id": 3,
            "roles": "{admin,user}"
        },
            {
            "username": "Queen",
            "id": 4,
            "roles": "{admin,user}"
        }]


api.add_resource(ResourceRecommendations, '/api/recommendations/')
