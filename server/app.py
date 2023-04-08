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
        smartie = Scientist.query.all()
        smart_kid_list = []
        for s in smartie:
            s_dict = {
                'id':s.id,
                "name":s.name,
                "field_of_study": s.field_of_study,
                "avatar": s.avatar,
            }
            smart_kid_list.append(s_dict)

        # return make_response({'scientists':smart_kid_list}, 200)
        return make_response(jsonify(smart_kid_list), 200)
    
    # The below code returns all the information...including the nested data ####
        # smart_kid = [s.to_dict() for s in Scientist.query.all()]
        # return make_response(jsonify(smart_kid), 200)

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
            smartie = Scientist.query.get(id)
            if smartie:
                field_trip = Mission.query.filter_by(id = id).all()
                planets = []
                for trip in field_trip:
                    planet = Planet.query.get(trip.planet_id)
                    planets.append({
                        'id': planet.id,
                        'name': planet.name,
                        'distance_from_earth': planet.distance_from_earth,
                        'nearest_star': planet.nearest_star,
                        'image': planet.image
                    })
                smartie_data = {
                    'id': smartie.id,
                    'name': smartie.name,
                    'field_of_study': smartie.field_of_study,
                    'avatar': smartie.avatar,
                    'planets': planets
                }
                return make_response(jsonify(smartie_data), 200)
            else:
                return make_response(jsonify({'message': 'Scientist not found'}), 404)

    ##### Returns Everything#### 
    # smart_kid = Scientist.query.filter_by(id = id).first().to_dict()
    # return make_response(jsonify(smart_kid), 200)
    
    def patch(self,id):
        data = request.get_json()
        new_info = Scientist.query.filter_by(id = id).first()
        for info in data:
            setattr(new_info, info, data[info])

        db.session.add(new_info)
        db.session.commit()

        new_info_dict = new_info.to_dict()
        response = make_response(new_info_dict, 202)
        return response
    
    def delete(self, id):
        doomed = Scientist.query.filter_by(id = id).first()
        db.session.delete(doomed)
        db.session.commit()

        doomed_dict = {"message": " "}
        response = make_response(doomed_dict, 204)
        return response

api.add_resource(ScientistsById, '/scientists/<int:id>')

class Planets(Resource):
    def get(self):
        world = Planet.query.all()
        world_list = []
        for w in world:
            w_dict = {
                "id": w. id,
                "name": w.name,
                "distance_from_earth": w.distance_from_earth,
                "nearest_star": w.nearest_star,
                "image": w.image,
            }
            world_list.append(w_dict)
        return make_response(jsonify(world_list), 200)

api.add_resource(Planets, '/planets')

if __name__ == '__main__':
    app.run(port=5555)
