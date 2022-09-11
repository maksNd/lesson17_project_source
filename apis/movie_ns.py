from flask import request
from flask_restx import Namespace, Resource
from apis.models_schemas.schemas import MovieSchema
from apis.models_schemas.models import Movie
from import_sqlalchemy import db

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):

        page = request.values.get('page')
        director_id = request.values.get('director_id')
        genre_id = request.values.get('genre_id')

        if director_id and genre_id:
            wanted_movies = Movie.query.filter(Movie.genre_id == genre_id and Movie.director_id == director_id).all()

        elif director_id and not genre_id:
            wanted_movies = Movie.query.filter(Movie.director_id == director_id).all()

        elif genre_id and not director_id:
            wanted_movies = Movie.query.filter(Movie.genre_id == genre_id).all()

        elif page:
            page = int(page)
            wanted_movies = db.session.query(Movie).offset((page * 5) - 5).limit(5).all()

        else:
            wanted_movies = Movie.query.all()

        if len(wanted_movies) == 0:
            return '', 404
        return MovieSchema(many=True).dump(wanted_movies), 200

    def post(self):
        requested_data = request.json
        new_movie = Movie(**requested_data)
        # with db.session.begin():
        db.session.add(new_movie)
        db.session.commit()
        return '', 204


@movie_ns.route('/<int:uid>/')
class MovieView(Resource):
    def get(self, uid):
        movie_by_id = Movie.query.get(uid)
        if not movie_by_id:
            return '', 404
        return MovieSchema().dump(movie_by_id), 200

    def put(self, uid):
        requested_data = request.json
        movie = Movie.query.get(uid)
        if not movie:
            return '', 404

        movie.title = requested_data.get('title')
        movie.description = requested_data.get('description')
        movie.trailer = requested_data.get('trailer')
        movie.year = requested_data.get('year')
        movie.rating = requested_data.get('rating')
        movie.genre_id = requested_data.get('genre_id')
        movie.director_id = requested_data.get('director_id')

        # with db.session.begin():
        db.session.add(movie)
        db.session.commit()
        return '', 204

    def delete(self, uid):
        movie = Movie.query.get(uid)
        if not movie:
            return '', 404
        # with db.session.begin():
        db.session.delete(movie)
        db.session.commit()
        return '', 204
