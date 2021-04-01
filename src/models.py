from flask_sqlalchemy import SQLAlchemy

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
    created = db.Column(db.String(30))
    edited = db.Column(db.String(30))
    homeworld = db.Column(db.String(30))
    description = db.Column(db.String(30))
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
            "url": self.url,


        }