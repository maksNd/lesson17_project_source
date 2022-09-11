from flask_restx import Resource, Namespace
from apis.models_schemas.models import Director
from apis.models_schemas.schemas import DirectorSchema
from flask import request
from import_sqlalchemy import db

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_directors = Director.query.all()
        if len(all_directors) == 0:
            return '', 404
        return DirectorSchema(many=True).dump(all_directors), 200

    def post(self):
        requested_json = request.json
        new_director = Director(**requested_json)
        with db.session.begin():
            db.session.add(new_director)
        return '', 204


@director_ns.route('/<int:uid>')
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
