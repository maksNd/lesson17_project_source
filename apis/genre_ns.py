from flask_restx import Namespace, Resource
from apis.models_schemas.models import Genre
from apis.models_schemas.schemas import GenreSchema
from flask import request
from import_sqlalchemy import db

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = Genre.query.all()
        if len(all_genres) == 0:
            return '', 404
        return GenreSchema(many=True).dump(all_genres)

    def post(self):
        requested_json = request.json
        new_genre = Genre(**requested_json)
        db.session.add(new_genre)
        db.session.commit()
        return '', 204


@genre_ns.route('/<int:uid>/')
class GenreView(Resource):
    def get(self, uid):
        genre = Genre.query.get(uid)
        if not genre:
            return '', 404
        return GenreSchema().dump(genre), 200

    def put(self, uid):
        genre = Genre.query.get(uid)
        if not genre:
            return '', 404
        requested_json = request.json
        genre.name = requested_json.get('name')
        db.session.add(genre)
        db.session.commit()
        return '', 204

    def delete(self, uid):
        genre = Genre.query.get(uid)
        if not genre:
            return '', 404
        db.session.delete(genre)
        db.session.commit()
        return '', 204
