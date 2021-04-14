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

#import JWT for tokenization
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# config for jwt
app.config["JWT_SECRET_KEY"] = "4g33ks4c4d3my"
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

############# Endpoints that require authentication or are related with JWT ###########
# Get User that is logged
@app.route('/get_logged_user', methods=['GET'])
@jwt_required()
def get_logged_user():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({"id": user.id, "username": user.user_name }), 200

# Login route
@app.route('/login', methods=['POST'])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    if email is None:
        return jsonify({"msg": "Invalid or empty email"}), 400
    if password is None:
        return jsonify({"msg": "Invalid password"}), 400

    user = User.query.filter_by(email=email, pswd=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Invalid username or password"}), 401
    else:
        # create a new token with the user id inside
        access_token = create_access_token(identity=user.id)
        return jsonify({ "msg":"ok", "token": access_token, "user_id": user.id }), 200

# Get the favorites of the user that logged in
@app.route('/get_fav_user_logged', methods=['GET'])
@jwt_required()
def get_fav_user_logged():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # get only the favorites for the given user
    tmp = Favorites.query.filter_by(user_id=user.id)

    # map the results 
    favorites = list(map(lambda x: x.serialize(), tmp)) 

    return jsonify(favorites), 200

# Add favorites to the todo list
@app.route('/add_fav_to_list', methods=['POST'])
@jwt_required()
def add_fav_to_list():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user is None:
        raise APIException('No User was found', status_code=400)

    #Get the request body
    request_body = request.get_json()
    # Validate the data
    if request_body["object_Type"] is None:
        raise APIException('You need to specify the object type', status_code=400)
    elif request_body["object_Name"] is None:
        raise APIException('You need to specify the object Id', status_code=400)
    #Create the new entry
    newFav = Favorites(user_id = user.id, object_Type = request_body["object_Type"],
    object_Name = request_body["object_Name"])

    db.session.add(newFav)
    db.session.commit()     

    return jsonify('Favorite added'), 200

# Delete favorites from the todo list
@app.route('/delete_fav_from_list/<int:idx>', methods=['DELETE'])
@jwt_required()
def delete_fav_from_list(idx):
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user is None:
        raise APIException('No User was found', status_code=400)

    # If an user was found, then delete the favorite from the list
    # Get the favorite Id
    fav = Favorites.query.get(idx)
    # If the favorite ID does not exist, return an error message
    if fav is None:
        raise APIException('Favorite Id not found', status_code=404)
    db.session.delete(fav)
    db.session.commit()      

    return jsonify('Favorite deleted'), 200

############# Endpoints that require authentication or are related with JWT ###########

# Register a new user
@app.route('/add_new_user', methods=['POST'])
def add_new_user():

    # Get the request body
    request_body = request.get_json()

    # Check that the password is not empty
    if (request_body["pswd"] == "" or request_body["user_name"] == "" or request_body["email"] == ""):
        raise APIException('Password, username and email cannot be empty', status_code=401)

    # Check if the user_name is already registered
    tmp = User.query.filter_by(user_name=request_body["user_name"])
    tmp = list(map(lambda x: x.serialize(), tmp))
    print("User extracted",tmp)
    if tmp != []:
        raise APIException('The username is already registered', status_code=402)
    # Check if the email is already registered
    tmp2 = User.query.filter_by(email=request_body["email"])
    tmp2 = list(map(lambda x: x.serialize(), tmp2))
    if tmp2 != []:
        raise APIException('The email is already registered', status_code=403)

    # Add the new user
    newUser = User(user_name=request_body["user_name"], email=request_body["email"],
    pswd=request_body["pswd"])
    db.session.add(newUser)
    db.session.commit()

    return jsonify('OK'), 200

# Get all the favorites that are registered
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

# Get Favorite by User - Part of the first assignment
@app.route('/get_fav/<int:idx>/favorites', methods=['GET'])
def get_favorite_by_user(idx):

    # get only the user(idx)
    tmp = Favorites.query.filter_by(user_id=idx)

    # map the results and your list of people  inside of the all_people variable
    favorites = list(map(lambda x: x.serialize(), tmp))  

    return jsonify(favorites), 200

# Add favorite by ID - Part of the first assignment
@app.route('/add_favorite/<int:idx>/favorites', methods=['POST'])
def add_favorite(idx):

    #Get the request body
    request_body = request.get_json()
    # Validate the data
    if request_body["object_Type"] is None:
        raise APIException('You need to specify the object type', status_code=400)
    elif request_body["object_Name"] is None:
        raise APIException('You need to specify the object Id', status_code=400)
    #Create the new entry
    newFav = Favorites(user_id = idx, object_Type = request_body["object_Type"],
    object_Name = request_body["object_Name"])

    db.session.add(newFav)
    db.session.commit()     

    return jsonify('Favorite added'), 200

# Delete favorite by ID
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

# Get all the users that are registered
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

# Get User by ID
@app.route('/get_user_by_id/<int:idx>', methods=['GET'])
def get_user_by_id(idx):
    # get the requested user
    user = User.query.get(idx)

    # If there requested user does not exist, return a warning message
    if user is None:
        raise APIException('User not found', status_code=404)
    
    user = user.serialize()

    return jsonify(user), 200

# Get All the characters
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

#Get Character by ID
@app.route('/get_character_by_id/<int:idx>', methods=['GET'])
def get_character_by_id(idx):
    # get the requested character
    character = Characters.query.get(idx)

    # If there requested character does not exist, return a warning message
    if character is None:
        raise APIException('Character not found', status_code=404)
    
    character = character.serialize()

    return jsonify(character), 200

# Get all the Planets
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

# Get Planet by ID
@app.route('/get_planet_by_id/<int:idx>', methods=['GET'])
def get_planet_by_id(idx):
    # get the requested planet
    planet = Planets.query.get(idx)

    # If there requested planet does not exist, return a warning message
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    
    planet = planet.serialize()

    return jsonify(planet), 200

# Get all the starships
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

# Get starship by ID
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
