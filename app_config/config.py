from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from apis.movie_ns import movie_ns
from apis.genre_ns import genre_ns
from apis.director_ns import director_ns
db = SQLAlchemy()


app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_ensure_ascii = False

db.init_app(app)

api = Api(app)
api.app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4}

api.add_namespace(movie_ns)
api.add_namespace(genre_ns)
api.add_namespace(director_ns)
