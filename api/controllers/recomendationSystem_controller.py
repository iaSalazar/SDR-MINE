
from flask_restful import Resource
from ..app.extensions import db, api, guard
from flask import request
from flask_restful import Resource
import flask_praetorian


class ResourceRecommendations(Resource):
    @flask_praetorian.auth_required
    def get(self):
        return {"recommendation": "this is a recommendation"}


api.add_resource(ResourceRecommendations, '/api/recommendations/')
