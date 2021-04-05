"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Characters, Planets, Starships, User, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/get_favorites', methods=['GET'])
def get_favorites():

    # get all the Favorites
    tmp = Favorites.query.all()

    # If there are no characters stored, return a warning message
    if len(tmp) == 0:
        raise APIException('There are no favorites stored in the API', status_code=404)

    # map the results and your list of favorites inside of the favorites variable
    favorites = list(map(lambda x: x.serialize(), tmp))

    return jsonify(favorites), 200

@app.route('/get_character/<int:idx>/favorites', methods=['GET'])
def get_favorite_by_user(idx):

    # get only the user(idx)
    tmp = Favorites.query.filter_by(user_id=idx)

    # map the results and your list of people  inside of the all_people variable
    favorites = list(map(lambda x: x.serialize(), tmp))  

    return jsonify(favorites), 200

@app.route('/add_favorite/<int:idx>/favorites', methods=['POST'])
def add_favorite(idx):
    
    #Get the request body
    request_body = request.get_json()
    # Validate the data
    if request_body["object_Type"] is None:
        raise APIException('You need to specify the object type', status_code=400)
    elif request_body["object_Id"] is None:
        raise APIException('You need to specify the object Id', status_code=400)
    #Create the new entry
    newFav = Favorites(user_id = idx, object_Type = request_body["object_Type"],
    object_Id = request_body["object_Id"])

    db.session.add(newFav)
    db.session.commit()     

    return jsonify('Favorite added'), 200


@app.route('/delete_favorite/<int:idx>', methods=['DELETE'])
def delete_favorite(idx):
    
    # Get the favorite Id
    fav = Favorites.query.get(idx)
    # If the favorite ID does not exist, return an error message
    if fav is None:
        raise APIException('Favorite Id not found', status_code=404)
    db.session.delete(fav)
    db.session.commit()      

    return jsonify('Favorite deleted'), 200


@app.route('/get_users', methods=['GET'])
def get_users():
    # get all the characters
    tmp = User.query.all()

    # If there are no characters stored, return a warning message
    if len(tmp) == 0:
        raise APIException('There are no users stored in the API', status_code=404)

    # map the results and your list of people  inside of the all_people variable
    users = list(map(lambda x: x.serialize(), tmp))

    return jsonify(users), 200

@app.route('/get_user_by_id/<int:idx>', methods=['GET'])
def get_user_by_id(idx):
    # get the requested user
    user = User.query.get(idx)

    # If there requested user does not exist, return a warning message
    if user is None:
        raise APIException('User not found', status_code=404)
    
    user = user.serialize()

    return jsonify(user), 200

@app.route('/get_characters', methods=['GET'])
def get_characters():
    # get all the characters
    tmp = Characters.query.all()

    # If there are no characters stored, return a warning message
    if len(tmp) == 0:
        raise APIException('There are no characters stored in the API', status_code=404)

    # map the results and your list of people  inside of the all_people variable
    characters = list(map(lambda x: x.serialize(), tmp))

    return jsonify(characters), 200

@app.route('/get_character_by_id/<int:idx>', methods=['GET'])
def get_character_by_id(idx):
    # get the requested character
    character = Characters.query.get(idx)

    # If there requested character does not exist, return a warning message
    if character is None:
        raise APIException('Character not found', status_code=404)
    
    character = character.serialize()

    return jsonify(character), 200

@app.route('/get_planets', methods=['GET'])
def get_planets():
    # get all the planets
    tmp = Planets.query.all()

    # If there are no planets stored, return a warning message
    if len(tmp) == 0:
        raise APIException('There are no planets stored in the API', status_code=404)

    # map the results 
    planets = list(map(lambda x: x.serialize(), tmp))

    return jsonify(planets), 200

@app.route('/get_planet_by_id/<int:idx>', methods=['GET'])
def get_planet_by_id(idx):
    # get the requested planet
    planet = Planets.query.get(idx)

    # If there requested planet does not exist, return a warning message
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    
    planet = planet.serialize()

    return jsonify(planet), 200

@app.route('/get_starships', methods=['GET'])
def get_starships():
    # get all the starships
    tmp = Starships.query.all()

    # If there are no starships stored, return a warning message
    if len(tmp) == 0:
        raise APIException('There are no starships stored in the API', status_code=404)

    # map the results 
    starships = list(map(lambda x: x.serialize(), tmp))

    return jsonify(starships), 200 

@app.route('/get_starship_by_id/<int:idx>', methods=['GET'])
def get_starship_by_id(idx):
    # get the requested starship
    starship = Starships.query.get(idx)

    # If there requested starship does not exist, return a warning message
    if starship is None:
        raise APIException('Starship not found', status_code=404)
    
    starship = starship.serialize()

    return jsonify(starship), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
