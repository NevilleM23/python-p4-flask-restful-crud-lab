#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)  

@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants])

@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get(id)
    if plant:
        return jsonify(plant.to_dict())
    return make_response(jsonify({"error": "Plant not found"}), 404)

@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()
    new_plant = Plant(
        name=data['name'],
        image=data['image'],
        price=data['price'],
        is_in_stock=data.get('is_in_stock', True)  
    )
    db.session.add(new_plant)
    db.session.commit()
    return jsonify(new_plant.to_dict()), 201


@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return make_response(jsonify({"error": "Plant not found"}), 404)
    
    data = request.get_json()
    
    if 'is_in_stock' in data:
        plant.is_in_stock = data['is_in_stock']
    # Commit changes
    db.session.commit()
  
    return jsonify({
        "id": plant.id,
        "name": plant.name,
        "image": plant.image,
        "price": float(plant.price),  
        "is_in_stock": plant.is_in_stock
    })


@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return make_response(jsonify({"error": "Plant not found"}), 404)
    
    db.session.delete(plant)
    db.session.commit()
    
    
    return '', 204






if __name__ == '__main__':
    app.run(port=5555, debug=True)
