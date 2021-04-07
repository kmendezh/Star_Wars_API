from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class Characters(db.Model):
    # Define the structure of the people table
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable=False)
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(30))
    skin_color = db.Column(db.String(30))
    eye_color = db.Column(db.String(30))
    birth_year = db.Column(db.Integer)
    gender = db.Column(db.String(30))
    created = db.Column(db.String(100))
    edited = db.Column(db.String(100))
    homeworld = db.Column(db.String(30))
    description = db.Column(db.String(50))
    url = db.Column(db.String(50))

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass, 
            "hair color": self.hair_color,
            "skin color": self.skin_color, 
            "eye color": self.eye_color, 
            "birth year": self.birth_year, 
            "gender": self.gender,
            "created": self.created,
            "edited": self.edited,
            "homeworld": self.homeworld,
            "description": self.description,
            "url": self.url


        }


class Planets(db.Model):
    # Define the structure of the planets table
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable=False)
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    gravity = db.Column(db.String(30))
    population = db.Column(db.Integer)
    climate = db.Column(db.String(30))
    terrain = db.Column(db.String(30))
    surface_water = db.Column(db.String(30))
    created = db.Column(db.String(30))
    edited = db.Column(db.String(30))
    url = db.Column(db.String(50))
    description = db.Column(db.String(30))

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation period": self.rotation_period,
            "orbital period": self.orbital_period, 
            "gravity": self.gravity,
            "population": self.population, 
            "climate": self.climate, 
            "terrain": self.terrain, 
            "surface_water": self.surface_water,
            "created": self.created,
            "edited": self.edited,
            "url": self.url,
            "description": self.description
        }


class Starships(db.Model):
    # Define the structure of the starships table
    id = db.Column(db.Integer, primary_key = True)
    model = db.Column(db.String(30))
    starship_class = db.Column(db.String(30))
    manufacturer = db.Column(db.String(30))
    cost_in_credits = db.Column(db.Integer)
    length = db.Column(db.Integer)
    crew = db.Column(db.Integer)
    passengers = db.Column(db.Integer)
    max_atmosphering_speed = db.Column(db.Integer)
    hyperdrive_rating = db.Column(db.Integer)
    mglt = db.Column(db.Integer)
    cargo_capacity = db.Column(db.Integer)
    consumables = db.Column(db.String(30))
    url = db.Column(db.String(50))
    description = db.Column(db.String(30))

    def __repr__(self):
        return '<Starships %r>' % self.model

    def serialize(self):
        return {
            "id": self.id,
            "model": self.model,
            "starship class": self.starship_class,
            "manufacturer": self.manufacturer, 
            "cost in credits": self.cost_in_credits,
            "length": self.length, 
            "crew": self.crew, 
            "max atmosphering speed": self.max_atmosphering_speed, 
            "hyperdrive rating": self.hyperdrive_rating,
            "mglt": self.mglt,
            "cargo capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "url": self.url,
            "description": self.description
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    object_Type = db.Column(db.String(2))
    object_Id = db.Column(db.String(50))

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user id": self.user_id,
            "object type": self.object_Type,
            "object id": self.object_Id
        }

class User(db.Model):
    # Define the structure of the user table
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    pswd = db.Column(db.String(30), nullable=False)
    favorites = relationship(Favorites)

    def __repr__(self):
        return '<User %r>' % self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "user name": self.user_name,
            "email": self.email
        }
