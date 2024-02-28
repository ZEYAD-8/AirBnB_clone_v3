#!/usr/bin/python3
"""
Handles all city routes in the API
"""

from flask import jsonify, abort, make_response, request
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/cities', methods=["GET"], strict_slashes=False)
def all_cities():
    """ return all city objects """
    cities = storage.all(City).values()
    cities = [city.to_dict() for city in cities]
    return jsonify(cities)


@app_views.route('/states/<state_id>/cities',
                 methods=["GET"], strict_slashes=False)
def all_cities_by_state(state_id):
    """ returns all cities linked to the specified state """
    state = storage.get(State, state_id)
    if not state:
        return abort(404)

    cities_list = state.cities
    cities_list = [city.to_dict() for city in cities_list]
    return jsonify(cities_list)


@app_views.route('/states/<state_id>/cities',
                 methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """ Creates a new City and links it to the state specified """
    try:
        city_dict = request.get_json()
    except Exception:
        return make_response(jsonify("Not a JSON"), 400)

    if "name" not in city_dict:
        return make_response(jsonify("Missing name"), 400)

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    city_dict["state_id"] = state_id
    created = City(**city_dict)
    created.save()
    return jsonify(created.to_dict()), 201


@app_views.route('/cities/<id>', methods=["GET"], strict_slashes=False)
def get_city_by_id(id):
    """ return the city related to that specific id """
    city = storage.get(City, id)
    if not city:
        return abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<id>', methods=["DELETE"], strict_slashes=False)
def delete_city_by_id(id):
    """ delets the city related to that specific id """
    city = storage.get(City, id)
    if not city:
        return abort(404)

    city.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('/cities/<id>', methods=["PUT"], strict_slashes=False)
def modify_city(id):
    """ Modifies an existing City """
    try:
        city_dict = request.get_json()
    except Exception:
        return make_response(jsonify("Not a JSON"), 400)

    city = storage.get(City, id)
    if not city:
        return abort(404)

    for key, value in city_dict.items():
        if key in ["id", "created_at", "updated_at", "state_id"]:
            continue
        setattr(city, key, value)

    city.save()
    return make_response(jsonify(city.to_dict()), 200)
