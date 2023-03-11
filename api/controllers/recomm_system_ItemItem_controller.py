
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


class ResourceRecommendations(Resource):
    @flask_praetorian.auth_required
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


class ResourceItemItemRecommendations(Resource):

    # @flask_praetorian.auth_required
    def post(self):
        username = request.json.get("body").get("username").replace('"', "")
        # 'user_001000'
        my_dict = artist_recommender(username, 3, 5)
        return my_dict  # {"Termino": "SI"}


api.add_resource(ResourceRecommendations, '/api/recommendations/')
api.add_resource(ResourceItemItemRecommendations,
                 '/api/recommendations/item-item')


def recommend_artists(user, num_recommended_artists, df, df1):
    data = []
    my_dict = {"listened_artist": [], "recomended_artists": []
               }
    # print('The list of the artists {} Has Watched \n'.format(user))

    for m in df[df[user] > 0][user].index.tolist():
        my_dict["listened_artist"].append(m)
        print(m)

    print('\n')

    recommended_artists = []

    for m in df[df[user] == 0].index.tolist():

        index_df = df.index.tolist().index(m)
        predicted_rating = df1.iloc[index_df,
                                    df1.columns.tolist().index(user)]
        recommended_artists.append((m, predicted_rating))

    sorted_rm = sorted(recommended_artists,
                       key=lambda x: x[1], reverse=True)

    print('The list of the recommended artist \n')
    rank = 1
    for recommended_movie in sorted_rm[:num_recommended_artists]:

        print('{}: {} - predicted rating:{}'.format(rank,
              recommended_movie[0], recommended_movie[1]))

        item = {}
        item["recomended_artists"] = recommended_movie[0]
        item["recommended_artists_rank"] = rank
        item["raiting"] = recommended_movie[1]
        data.append(item)

        my_dict["recomended_artists"].append(item)

        rank = rank + 1
    return my_dict


def artist_recommender(user, num_neighbors, num_recommendation):

    print("Reading Matrix")
    matrix = pd.read_csv(
        './utils/item-item-matrix.csv', index_col="artist-name")

    try:
        matrix.columns.tolist().index(user)
    except ValueError as e:
        print("ES FALSO")
        data = []
        my_dict = {"listened_artist": [], "recomended_artists": []
                   }
        item = {}
        item["recomended_artists"] = "Please score some artists"
        item["recommended_artists_rank"] = ""
        item["raiting"] = ""
        data.append(item)
        my_dict["recomended_artists"].append(item)
        return my_dict

    df = matrix.fillna(0)
    df1 = df.copy()
    print("Loading KNN model")
    number_neighbors = num_neighbors
    knn = pickle.load(open(
        './utils/item-item-knn.pkl', 'rb'))
    distances, indices = knn.kneighbors(
        df.values, n_neighbors=number_neighbors)

    user_index = df.columns.tolist().index(user)
    print("predicting all non listened artist")
    for m, t in list(enumerate(df.index)):
        if df.iloc[m, user_index] == 0:
            sim_artists = indices[m].tolist()
            movie_distances = distances[m].tolist()

            if m in sim_artists:
                id_movie = sim_artists.index(m)
                sim_artists.remove(m)
                movie_distances.pop(id_movie)

            else:
                sim_artists = sim_artists[:number_neighbors-1]
                movie_distances = movie_distances[:number_neighbors-1]

            movie_similarity = [1-x for x in movie_distances]
            movie_similarity_copy = movie_similarity.copy()
            nominator = 0

            for s in range(0, len(movie_similarity)):
                if df.iloc[sim_artists[s], user_index] == 0:
                    if len(movie_similarity_copy) == (number_neighbors - 1):
                        movie_similarity_copy.pop(s)

                    else:
                        movie_similarity_copy.pop(
                            s-(len(movie_similarity)-len(movie_similarity_copy)))

                else:
                    nominator = nominator + \
                        movie_similarity[s] * \
                        df.iloc[sim_artists[s], user_index]

            if len(movie_similarity_copy) > 0:
                if sum(movie_similarity_copy) > 0:
                    predicted_r = nominator/sum(movie_similarity_copy)

                else:
                    predicted_r = 0

            else:
                predicted_r = 0

            df1.iloc[m, user_index] = predicted_r
    my_dict = recommend_artists(user, num_recommendation, df, df1)
    return my_dict
