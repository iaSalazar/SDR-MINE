
from ..app.extensions import db, ma


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nationality = db.Column(db.String(50))
    gender = db.Column(db.String(255))
    name = db.Column(db.String(255))
    lastName = db.Column(db.String(255))


class ArtistSchema(ma.Schema):
    class Meta:
        fields = ("id", "nationality", "gender", "name", "lastName",
                  )


artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)
