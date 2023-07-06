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
        

@app.route('/hero_powers', methods=['GET','POST'])
def create_hero_power():
    power = Power.query.all()

    if request.method == 'POST':
        # Handle POST request
        data = request.get_json()
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')

        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            return make_response(jsonify({'errors': ['Validation errors']}), 400)

        power = Power.query.get(power_id)
        hero = Hero.query.get(hero_id)

        if not power or not hero:
            return make_response(jsonify({'errors': ['Power or Hero not found']}), 404)

        new_hero_power = hero_powers.insert().values(strength=strength, power_id=power_id, hero_id=hero_id)
        db.session.execute(new_hero_power)
        db.session.commit()

if __name__ == '__main__':
    app.run(port=5555)
