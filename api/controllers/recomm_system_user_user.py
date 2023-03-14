import json
import os
import pickle
from flask_restful import Resource
import pandas as pd
from ..app.extensions import db, api, guard
from flask import request
from flask_restful import Resource
import flask_praetorian
from sklearn.neighbors import NearestNeighbors


class ResourceUserUserRecommendations(Resource):
    # TODO
    pass


api.add_resource(ResourceUserUserRecommendations,
                 '/api/recommendations/user-user')
