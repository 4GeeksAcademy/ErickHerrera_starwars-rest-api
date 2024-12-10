"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character,Planet,Vehicle
#from models import Person
#AQUI SE TRABAJAN LAS RUTAS, TRABAJAR DESPUES DE LA LINEA 34
app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

#Obtener todos los usuarios
@app.route('/user', methods=['GET'])
def get_all_users():
    try:
        users=User.query.all()
        if len(users)<1:
            return jsonify({"msg":"not found"}),404
        serialized_users=list(map(lambda x: x.serialize(),users))
        return serialized_users, 200
    except Exception as e:
        return jsonify({"msg":"Server error", "error":str(e)}), 500
    
#Obtener usuario por ID
@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    try:
        user=User.query.get(user_id)
        if user is None:
            return jsonify({"msg":f"user {user_id} not found"}), 404
        serialized_user=user.serialize()
        return serialized_user, 200
    except Exception as e:
        return jsonify({"msg":"Server error", "error":str(e)}), 500
    
#crear usuario
@app.route('/user', methods=['POST'])
def create_one_user():
    try:
        body=json.loads(request.data)
        new_user=User(
            email=body["email"],
            password=body["password"],
            is_active=True
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg":"User created succesfully"}),201
    except Exception as e:
        return jsonify({"msg":"Server error", "error":str(e)}), 500
#editar usuario
#borrar el usuario


#Obtener personajes
@app.route('/characters', methods=['GET'])
def get_all_characters():
    try:
        characters=Character.query.all()
        if len(characters)<1:
            return jsonify({"msg":"not found"}),404
        serialized_users=list(map(lambda x: x.serialize(),characters))
        return serialized_users, 200
    except Exception as e:
        return jsonify({"msg":"Server error", "error":str(e)}), 500
    
#Obtener planetas
@app.route('/planets', methods=['GET'])
def get_all_planets():
    try:
        planets=Planet.query.all()
        if len(planets)<1:
            return jsonify({"msg":"not found"}),404
        serialized_users=list(map(lambda x: x.serialize(),planets))
        return serialized_users, 200
    except Exception as e:
        return jsonify({"msg":"Server error", "error":str(e)}), 500

#Obtener starships
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    try:
        vehicles=Vehicle.query.all()
        if len(vehicles)<1:
            return jsonify({"msg":"not found"}),404
        serialized_users=list(map(lambda x: x.serialize(),vehicles))
        return serialized_users, 200
    except Exception as e:
        return jsonify({"msg":"Server error", "error":str(e)}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
