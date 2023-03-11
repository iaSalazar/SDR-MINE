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
from flask import Response


class ResourceGenericRecommendations(Resource):
    @flask_praetorian.auth_required
    def get(self):

        ratings = pd.read_csv(
            '/home/ivs/Documents/MyProjects/SDR/sdr-taller-1/api/data/preprocessed_user_item_rating.csv').rename(columns={"artist-name": "artist_name"})

        agg_ratings = ratings.groupby('artist_name').agg(mean_rating=('rating', 'mean'),
                                                         number_of_ratings=('rating', 'count')).reset_index().sort_values('number_of_ratings',  ascending=False)
        agg_ratings = agg_ratings[agg_ratings['number_of_ratings'] > 10]

        agg_ratings = agg_ratings.sort_values(
            ['number_of_ratings', 'mean_rating'],  ascending=False)[:10]

        return Response(agg_ratings.to_json(orient="records"), mimetype='application/json')


api.add_resource(ResourceGenericRecommendations,
                 '/api/recommendations/generic')
