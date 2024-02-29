#!/usr/bin/python3
"""
Handles all place routes in the API
"""

from flask import jsonify, abort, make_response, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=["GET"], strict_slashes=False)
def all_places_by_city(city_id):
    """ returns all places linked to the specified city """
    city = storage.get(City, city_id)
    if not city:
        return abort(404)

    places = storage.all(Place)
    places_list = []
    for place in places:
        if place.city_id == city.id:
            places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/cities/<city_id>/places',
                 methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """ Creates a new place and links it to the city and user specified """
    try:
        place_dict = request.get_json()
    except Exception:
        return make_response(jsonify("Not a JSON"), 400)

    if "user_id" not in place_dict:
        return make_response(jsonify("Missing user_id"), 400)

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    user = storage.get(User, place_dict["user_id"])
    if user is None:
        abort(404)

    if "name" not in place_dict:
        return make_response(jsonify("Missing name"), 400)

    place_dict["city_id"] = city_id
    created = Place(**place_dict)
    created.save()
    return jsonify(created.to_dict()), 201


@app_views.route('/places/<id>', methods=["GET"], strict_slashes=False)
def get_place_by_id(id):
    """ return the place related to that specific id """
    place = storage.get(Place, id)
    if not place:
        return abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<id>', methods=["DELETE"], strict_slashes=False)
def delete_place_by_id(id):
    """ delets the place related to that specific id """
    place = storage.get(Place, id)
    if not place:
        return abort(404)

    place.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('/places/<id>', methods=["PUT"], strict_slashes=False)
def modify_place(id):
    """ Modifies an existing Place """
    try:
        place_dict = request.get_json()
    except Exception:
        return make_response(jsonify("Not a JSON"), 400)

    place = storage.get(City, id)
    if not place:
        return abort(404)

    for key, value in place_dict.items():
        if key in ["id", "created_at", "updated_at", "city_id", "user_id"]:
            continue
        setattr(place, key, value)

    place.save()
    return make_response(jsonify(place.to_dict()), 200)
