#!/usr/bin/env python3

from flask import Flask, make_response,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Hero, HeroPower, Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>my app</h1>'

@app.route('/heroes')
def heroes():
    
    heros = []
    for hero in Hero.query.all():
        hero_dict = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name
        }
        heros.append(hero_dict)
    
    response = make_response(
        jsonify(heros),
        200
    )
    return response

@app.route('/heroes/<int:id>', methods = ['GET'])
def heroes_by_id(id):
    hero = Hero.query.filter_by(id=id).first()

    if hero == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(jsonify(response_body),404)
        return response
    
    else:
        if request.method == 'GET':
            hero_dict = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": [hero_power.power.name for hero_power in hero.hero_powers]
            }
            response = make_response(
                jsonify(hero_dict),
                200
            )
            return response
        
@app.route('/powers')
def powers():
    powers = []
    for power in Power.query.all():
        power_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        response = make_response(
            jsonify(power_dict),
            200
        )
        return response
    
@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def powers_by_id(id):
    power = Power.query.filter_by(id=id).first()

    if power == None:
        response_body = {
            "message": "Power not found."
        }
        response = make_response(jsonify(response_body),404)
        return response
    else:
        if request.method == 'GET':
            power_dict = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            response = make_response(
                jsonify(power_dict),
                200
            )
            return response
        
        elif request.method == 'PATCH':
            for attr in request.json:
                setattr(power, attr, request.json[attr])

            try:
                db.session.commit()
            except ValueError:
                response_body = {
                    "errors": "validation errors"
                }
                response = make_response(jsonify(response_body), 400)
                return response

            response_body = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            response = make_response(jsonify(response_body), 200)
            return response
        

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json

    # Validate the required fields
    if 'strength' not in data or 'power_id' not in data or 'hero_id' not in data:
        response_body = {
            "errors": ["strength, power_id, and hero_id are required fields"]
        }
        response = make_response(jsonify(response_body), 400)
        return response

    # Create a new HeroPower instance
    hero_power = HeroPower(strength=data['strength'], power_id=data['power_id'], hero_id=data['hero_id'])

    try:
        db.session.add(hero_power)
        db.session.commit()
    except ValueError:
        response_body = {
            "errors": ["validation errors"]
        }
        response = make_response(jsonify(response_body), 400)
        return response

    # Retrieve the related Hero data
    hero = Hero.query.filter_by(id=data['hero_id']).first()

    if hero is None:
        response_body = {
            "errors": ["Hero not found"]
        }
        response = make_response(jsonify(response_body), 404)
        return response

    # Retrieve the related Powers data
    powers = Power.query.join(HeroPower).filter_by(hero_id=data['hero_id']).all()
    powers_data = [{
        "id": power.id,
        "name": power.name,
        "description": power.description
    } for power in powers]

    response_body = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": powers_data
    }

    response = make_response(jsonify(response_body), 200)
    return response

if __name__ == '__main__':
    app.run(port=5555)
