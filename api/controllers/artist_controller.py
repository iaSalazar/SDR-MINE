from flask import request
from flask_restful import Resource
from ..models.artist_model import artist_schema, artists_schema, Artist
from ..app.extensions import db, api


class ResourceArtists(Resource):
    def get(self):
        artist = Artist.query.all()
        return artists_schema.dump(artist)


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


api.add_resource(ResourceArtists, '/api/artists')
api.add_resource(ResourceArtist, '/api/artists/<int:id_artist>')
