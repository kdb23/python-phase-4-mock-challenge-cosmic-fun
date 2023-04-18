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

    serialize_rules = ('-created_at', '-updated_at', '-scientist', '-planet')

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    serialize_rules = ('-created_at', '-updated_at', '-missions', )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    avatar = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    planets =  association_proxy('missions', 'planet')
    missions = db.relationship('Mission', backref = 'scientist')


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    serialize_rules = ('-created_at', '-updated_at', '-planet', '-missions')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    scientists = association_proxy('missions', 'scientist')
    missions = db.relationship("Mission", backref = 'planet')

    
