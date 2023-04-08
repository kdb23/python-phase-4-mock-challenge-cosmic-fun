from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    serialize_rules = ('-scientist.missions', '-planet.missions',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    @validates('name')
    def validate_name(self, key, name):
        names = db.session.query(Mission.name).all()
        if not name:
            raise ValueError("Name field is Required")
        return names
    
    @validates('scientist_id')
    def validate_explorer(self, key, explorer):
        smartie = Scientist.query.all()
        ids = [e.id for e in smartie]
        if not explorer:
                raise ValueError("Mission must have Scientist")
        elif not explorer in ids:
                raise ValueError("Scientist must Exist to Join the Mission")
        return explorer
            

    @validates('planet_id')
    def validate_planet(self, key, world):
        new_world = Planet.query.all()
        ids = [w.id for w in new_world]
        if not world:
            raise ValueError("Planet must be provided")
        elif not world in ids:
            raise ValueError("Planet must Exist to be Explored")
        return new_world



    def __repr__(self):
        return f'<Mission id={self.id}, name={self.name}, scientist_id={self.scientist_id}, planet_id={self.planet_id}>'

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    serialize_rules = ('-missions.scientist',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False )
    field_of_study = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    missions = db.relationship("Mission", backref = 'scientist')

    @validates('name')
    def validate_name(self, key, name):
        names = db.session.query(Scientist.name).all()
        if not name:
            raise ValueError("Name Field is Required")
        elif name in names:
            raise ValueError("Name must be unique")
        return name

    @validates('field_of_study')
    def validate_study(self, key, field_of_study):
        studies = db.session.query(Scientist.field_of_study).all()
        if not field_of_study:
            raise ValueError("Field of Study is Required")
        return studies

    def __repr__(self):
        return f'<Scientist {self.name}, {self.field_of_study}, {self.avatar}>'
    


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    serialize_rules = ('-missions.planet',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    missions = db.relationship("Mission", backref = 'planet')

    def repr__(self):
        return f'<Planet {self.name}, {self.distance_from_earth}, {self.nearest_star}, {self.image}>'
