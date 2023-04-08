from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Scientist, Planet, Mission

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)


db.init_app(app)
api = Api(app)

class Index(Resource):
    def get(self):
        response = make_response(
            {"message": "Hello Scientists!"}
        )
        return response

api.add_resource(Index, '/')

class Scientists(Resource):
    def get(self):
        smart_kid = [s.to_dict() for s in Scientist.query.all()]
        return make_response(jsonify(smart_kid), 200)

    def post(self):
        data = request.get_json()
        new_kid = Scientist(
            name = data['name'],
            field_of_study = data['field_of_study'],
            avatar = data['avatar'],
        )
        db.session.add(new_kid)
        db.session.commit()

        return make_response(new_kid.to_dict(), 201)


api.add_resource(Scientists, '/scientists')

class ScientistsById(Resource):
    def get(self, id):
        smart_kid = Scientist.query.filter_by(id = id).first().to_dict()
        return make_response(jsonify(smart_kid), 200)
    
    def patch(self,id):
        data = request.get_json()
        new_info = Scientist.query.filter_by(id = id).first()
        for info in data:
            setattr(new_info, info, data[info])

        db.session.add(new_info)
        db.session.commit()

        new_info_dict = new_info.to_dict()
        response = make_response(new_info_dict, 200)
        return response

api.add_resource(ScientistsById, '/scientists/<int:id>')

if __name__ == '__main__':
    app.run(port=5555)
