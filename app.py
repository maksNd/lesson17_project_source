# app.py
from config import api, db
from flask import request, current_app
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from marshmallow import Schema, fields
from models import Movie, Genre, Director
from schemas import MovieSchema, GenreSchema, DirectorSchema

app = current_app

movie_namespace = api.namespace('movies')
director_namespace = api.namespace('directors')
genre_namespace = api.namespace('genres')


@movie_namespace.route('/')
class MoviesView(Resource):
    def get(self):
        with app.app_context():
            page = request.values.get('page')
            director_id = request.values.get('director_id')
            genre_id = request.values.get('genre_id')

        if page and not genre_id and not director_id:
            page = int(page)
            per_page = 5
            all_movies = db.session.query(Movie).offset((page * per_page) - per_page).limit(per_page).all()
            return MovieSchema(many=True).dump(all_movies), 200

        if director_id and not genre_id:
            director_id = int(director_id)
            movies_by_director_id = Movie.query.filter(Movie.director_id == director_id).all()
            if len(movies_by_director_id) == 0:
                return '', 404
            return MovieSchema(many=True).dump(movies_by_director_id), 200

        if genre_id and not director_id:
            genre_id = int(genre_id)
            movies_by_genre_id = Movie.query.filter(Movie.genre_id == genre_id).all()
            if len(movies_by_genre_id) == 0:
                return '', 404
            return MovieSchema(many=True).dump(movies_by_genre_id), 200

        if director_id and genre_id:
            director_id = int(director_id)
            genre_id = int(genre_id)
            movies = Movie.query.filter(Movie.genre_id == genre_id and Movie.director_id == director_id).all()
            if len(movies) == 0:
                return '', 404
            return MovieSchema(many=True).dump(movies), 200


        else:
            all_movies = db.session.query(Movie).all()
            return MovieSchema(many=True).dump(all_movies), 200
        # return '', 404

    def post(self):
        requested_data = request.json
        new_movie = Movie(**requested_data)
        with db.session.begin():
            db.session.add(new_movie)


@movie_namespace.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid):
        try:
            movie_by_id = Movie.query.filter(Movie.id == uid).one()
        except exc.NoResultFound:
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

        db.session.add(movie)
        db.session.commit()
        return '', 204

    def delete(self, uid):
        movie = Movie.query.get(uid)
        if not movie:
            return '', 404
        db.session.delete(movie)
        db.session.commit()
        return '', 204


@genre_namespace.route('/')
class GenresView(Resource):
    def post(self):
        requested_json = request.json
        new_genre = Genre(**requested_json)
        with db.session.begin():
            db.session.add(new_genre)
        return '', 201


@genre_namespace.route('/<int:uid>')
class GenreView(Resource):
    def put(self, uid):
        genre = Genre.query.get(uid)
        print(genre)
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


@director_namespace.route('/')
class DirectorsView(Resource):
    def post(self):
        requested_json = request.json
        new_director = Director(**requested_json)
        with db.session.begin():
            db.session.add(new_director)
        return '', 201


@director_namespace.route('/<int:uid>')
class GenreView(Resource):
    def put(self, uid):
        director = Director.query.get(uid)
        if not director:
            return '', 404
        requested_json = request.json
        director.name = requested_json.get('name')
        db.session.add(director)
        db.session.commit()
        return '', 204

    def delete(self, uid):
        director = Director.query.get(uid)
        if not director:
            return '', 404
        db.session.delete(director)
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    app.run()
