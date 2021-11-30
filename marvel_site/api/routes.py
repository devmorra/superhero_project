from flask import Blueprint, request, jsonify, flash
from marvel_site.helpers import token_required
from marvel_site.models import db, User, Hero, hero_schema, heroes_schema
from flask_cors import CORS, cross_origin

api = Blueprint('api', __name__, url_prefix='/api' )

@api.route('/heroes', methods=['POST'])
@token_required
def createHero(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    hero = Hero(name, description, comics_appeared_in, super_power, current_user_token.token)
    db.session.add(hero)
    # print("hero created")
    db.session.commit()
    # print("hero committed")
    response = hero_schema.dump(hero)
    # print("response created")
    return jsonify(response)
    

# RETRIEVE ALL heroes ENDPOINT
@api.route('/heroes', methods = ['GET'])
@token_required
def getheroes(current_user_token):
    owner = current_user_token.token
    heroes = Hero.query.filter_by(owner = owner).all()
    response = heroes_schema.dump(heroes)
    return jsonify(response)

# RETRIEVE ONE hero ENDPOINT
@api.route('/heroes/<id>', methods = ['GET'])
@token_required
def gethero(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        try:
            hero = Hero.query.get(id)
            response = hero_schema.dump(hero)
            return jsonify(response)
        except:
            return jsonify({"message": "hero ID not found"}), 401
    else:
        return jsonify({"message": "Valid Token Required"}),401

# update hero endpoint
@api.route('/heroes/<id>', methods=['POST', 'PUT'])
@token_required
def updatehero(current_user_token, id):
    hero = Hero.query.get(id)
    hero.name = request.json['name']
    hero.description = request.json['description']
    hero.comics_appeared_in = request.json['comics_appeared_in']
    hero.super_power = request.json['super_power']
    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)

# DELETE hero ENDPOINT
@api.route('/heroes/<id>', methods = ['DELETE'])
@token_required
def delete_hero(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        hero = Hero.query.get(id)
        db.session.delete(hero)
        db.session.commit()
        response = hero_schema.dump(hero)
        return jsonify(response)
    else:
        return jsonify({"message": "Only the owners of a hero can delete a hero"}),401
    
