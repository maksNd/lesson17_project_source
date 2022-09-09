# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_ensure_ascii = False
db = SQLAlchemy(app)

api = Api(app)
api.app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4}

movie_namespace = api.namespace('movies')
director_namespace = api.namespace('directors')
genre_namespace = api.namespace('genres')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    genre = fields.Pluck(GenreSchema, 'name')
    director_id = fields.Int()
    director = fields.Pluck(DirectorSchema, 'name')


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


# genre_schema = GenreSchema()
# genres_schema = GenreSchema(many=True)
# director_schema = DirectorSchema()
# directors_schema = DirectorSchema(many=True)


@movie_namespace.route('/')
class MoviesView(Resource):
    def get(self):
        with app.app_context():
            movie_id = request.values.get('movie_id')
            page = request.values.get('page')
            director_id = request.values.get('director_id')
            genre_id = request.values.get('genre_id')

        if page:
            page = int(page)
            per_page = 5
            all_movies = db.session.query(Movie).offset((page * per_page) - per_page).limit(per_page).all()
            return movies_schema.dump(all_movies), 200

        if movie_id:
            movie_id = int(movie_id)
            movie_by_id = db.session.query(Movie).filter(Movie.id == movie_id).one()
            return movie_schema.dump(movie_by_id), 200

        if director_id:
            director_id = int(director_id)
            movies_by_director_id = db.session.query(Movie).filter(Movie.director_id == director_id)
            return movies_schema.dump(movies_by_director_id), 200

        if genre_id:
            genre_id = int(genre_id)
            movies_by_genre_id = db.session.query(Movie).filter(Movie.genre_id == genre_id)
            return movies_schema.dump(movies_by_genre_id), 200

        if director_id and genre_id:
            director_id = int(director_id)
            genre_id = int(genre_id)
            movies = db.session.query(Movie).filter(Movie.genre_id == genre_id, Movie.director_id == director_id)
            return movies_schema.dump(movies), 200

        return '', 404


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
class GenresView(Resource):
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
