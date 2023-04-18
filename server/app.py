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
        return make_response(smart_kid, 200)
    
    def post(self):
        data = request.get_json()
        try:
            new_kid = Scientist(
                name = data['name'],
                field_of_study = data['field_of_study'],
                avatar = data['avatar']
            )
        except:
            return make_response({'error': 'Scientist Not Found'}, 404)
        db.session.add(new_kid)
        db.session.commit()
        return make_response(new_kid.to_dict(), 201)
    
api.add_resource(Scientists, '/scientists')

class ScientistById(Resource):

    def get(self, id):
        smart_kid = Scientist.query.filter_by(id = id).first()
        if not smart_kid:
            return make_response({'error': 'scinetist not found'}, 404)
        smart_dict = smart_kid.to_dict(rules=('planets',))
        return make_response(smart_dict, 200)
    
    def patch(self, id):
        data = request.get_json()
        smart_kid = Scientist.query.filter_by(id = id).first()
        for info in data:
            setattr(smart_kid, info, data[info])
        db.session.add(smart_kid)
        db.session.commit()
        return make_response(smart_kid.to_dict(), 202)



api.add_resource(ScientistById, '/scientists/<int:id>')

class Planets(Resource):

    def get(self):
        planet = [s.to_dict() for s in Planet.query.all()]
        return make_response(planet, 200)
    
api.add_resource(Planets, '/planets')


class Missions(Resource):

    def get(self):
        mission = [m.to_dict() for m in Mission.query.all()]
        return make_response(mission, 200)
    
    def post(self):
        data = request.get_json()
        try:
            new_mission = Mission(
                name = data['name'],
                scientist_id = data['scientist_id'],
                planet_id = data['planet_id']
            )
        except:
            return make_response({'error': 'Scientist Not Found'}, 404)
        db.session.add(new_mission)
        db.session.commit()
        return make_response(new_mission.planet.to_dict(), 201)
    
api.add_resource(Missions, '/missions')
if __name__ == '__main__':
    app.run(port=5555)
