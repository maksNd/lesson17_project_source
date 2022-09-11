# app.py
from config import api, db
from flask import request, current_app
from flask_restx import Resource, Api
from apis.models import Movie, Genre, Director
from apis.schemas import MovieSchema, GenreSchema, DirectorSchema

# from data_manager.create_data import fill_db

# fill_db()

app = current_app

if __name__ == '__main__':
    app.run(debug=True)
