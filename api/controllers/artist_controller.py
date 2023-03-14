from flask import request
from flask_restful import Resource
from ..models.artist_model import artist_schema, artists_schema, Artist
from ..app.extensions import db, api
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import pickle


class ResourceArtists(Resource):
    def get(self):
        artist = Artist.query.all()
        return artists_schema.dump(artist)

    def post(self):
        new_artist = Artist(

            name=request.json['name'],
            # lastName=request.json['lastName']
        )
        db.session.add(new_artist)
        db.session.commit()
        return artist_schema.dump(new_artist)


class ResourceArtist(Resource):
    def get(self, id_artist):
        artist = Artist.query.get_or_404(id_artist)
        return artist_schema.dump(artist)

    def put(self, id_artist):
        artist = Artist.query.get_or_404(id_artist)

        if 'name' in request.json:
            artist.name = request.json['name']
        if 'lastName' in request.json:
            artist.lastName = request.json['lastName']

        db.session.commit()
        return artist_schema.dump(artist)

    def delete(self, id_artist):
        artist = Artist.query.get_or_404(id_artist)
        db.session.delete(artist)
        db.session.commit()
        return '', 204

    def post(self):
        new_artist = Artist(

            name=request.json['name'],
            lastName=request.json['lastName']
        )
        db.session.add(new_artist)
        db.session.commit()
        return artist_schema.dump(new_artist)


class ResourceArtistRaiting(Resource):

    def post(self):

        artistName = request.json['name']
        rating = request.json['rating']
        username_dict = request.json['username']
        username = username_dict.get(
            "current").replace('"', "")

        print("READING RATINGS")
        user_rating = pd.DataFrame([[username, artistName, float(rating)]],
                                   columns=['userid', 'artist-name', 'rating'])

        user_ratings = pd.read_csv(
            './utils/preprocessed_user_item_rating.csv').drop("Unnamed: 0", axis=1)

        ratings = pd.concat([user_rating, user_ratings]).reset_index(
            drop=True).reset_index(drop=True)

        agg_ratings = ratings.groupby('artist-name').agg(mean_rating=('rating', 'mean'),
                                                         number_of_ratings=('rating', 'count')).reset_index().sort_values('number_of_ratings',  ascending=False)

        agg_ratings = agg_ratings[agg_ratings['number_of_ratings'] > 10]
        ratings_final = pd.merge(
            ratings, agg_ratings[['artist-name']], on='artist-name', how='inner')
        print("CREATING MATRIX")
        matrix = ratings_final.pivot_table(
            index='artist-name', columns='userid', values='rating')

        matrix.to_csv('./utils/item-item-matrix.csv', header=True)
        df = matrix.copy().fillna(0)

        knn = NearestNeighbors(metric='cosine', algorithm='brute')
        print("TRAINING MODEL")
        knn.fit(df.values)

        pickle.dump(knn, open('./utils/item-item-knn.pkl', 'wb'))

        return [{
            "name": artistName,
            "rating": rating,
            "username": username
        }]


api.add_resource(ResourceArtists, '/api/artists')
api.add_resource(ResourceArtistRaiting, '/api/artists/rate')
api.add_resource(ResourceArtist, '/api/artists/<int:id_artist>')
