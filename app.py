# app.py
from config import api, db
from flask import request, current_app, jsonify
from flask_restx import Resource
from models import Movie, Genre, Director
from schemas import MovieSchema, GenreSchema, DirectorSchema
from data_manager.create_data import fill_db

fill_db()

app = current_app

movie_namespace = api.namespace('movies')
director_namespace = api.namespace('directors')
genre_namespace = api.namespace('genres')


@movie_namespace.route('/')
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
        with db.session.begin():
            db.session.add(new_movie)
        return '', 204


@movie_namespace.route('/<int:uid>')
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


#########################################


@genre_namespace.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = Genre.query.all()
        if len(all_genres) == 0:
            return '', 404
        return GenreSchema(many=True).dump(all_genres)

    def post(self):
        requested_json = request.json
        new_genre = Genre(**requested_json)
        with db.session.begin():
            db.session.add(new_genre)
        return '', 204


@genre_namespace.route('/<int:uid>')
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


#########################################


@director_namespace.route('/')
class DirectorsView(Resource):
    def get(self):
        all_directors = Director.query.all()
        if len(all_directors) == 0:
            return '', 404

    def post(self):
        requested_json = request.json
        new_director = Director(**requested_json)
        with db.session.begin():
            db.session.add(new_director)
        return '', 204


@director_namespace.route('/<int:uid>')
class DirectorView(Resource):
    def get(self, uid):
        director = Director.query.get(uid)
        if not director:
            return '', 404
        return DirectorSchema().dump(director), 200

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
