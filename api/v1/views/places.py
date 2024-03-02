#!/usr/bin/python3
"""
Handles all place routes in the API
"""

from flask import jsonify, abort, make_response, request
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity
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
    for place in places.values():
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

    place = storage.get(Place, id)
    if not place:
        return abort(404)

    for key, value in place_dict.items():
        if key in ["id", "created_at", "updated_at", "city_id", "user_id"]:
            continue
        setattr(place, key, value)

    place.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=["POST"], strict_slashes=False)
def places_search():
    """retrieves all Place objects depending on the body of the request"""
    try:
        search_dict = request.get_json()
    except Exception:
        return make_response(jsonify("Not a JSON"), 400)

    if len(search_dict) == 0:
        return jsonify([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 400

    cities_to_search = list()

    # retrieve cities specified in search dict (direct or each city in a state)
    no_states = False
    if "states" in search_dict and len(search_dict["states"]) != 0:
        for state_id in search_dict["states"]:
            state = storage.get(State, state_id)
            if state is None:
                continue
            cities_to_search += state.cities
    else:
        no_states = True

    no_cities = False
    if "cities" in search_dict and len(search_dict["cities"]) != 0:
        for city_id in search_dict["cities"]:
            city = storage.get(City, city_id)
            if city is None:
                continue
            cities_to_search.append(city)
    else:
        no_cities = True

    # keep only unique cities
    cities_ids = set()
    cities = list()
    for city in cities_to_search:
        if city.id not in cities_ids:
            cities_ids.update(city.id)
            cities.append(city)

    # retrieve all places in the cities so far
    places = []
    for city in cities:
        places += city.places

    if no_states and no_cities:
        places = storage.all(Place).values()

    # if no amenities filter, return the places found
    if "amenities" not in search_dict or len(search_dict["amenities"]) == 0:
        places = [place.to_dict() for place in places]
        return jsonify(places), 200

    # filter out places that doesn't have all the amenities mentioned
    filtered_places = []
    for place in places:
        valid = True
        amenities = place.amenities

        for amenity_id in search_dict["amenities"]:
            found = False
            for amenity in amenities:
                if amenity.id == amenity_id:
                    found = True
                    break
            if not found:
                valid = False
                break

        if not valid:
            continue

        if not isinstance(place, Amenity):
            filtered_places.append(place.to_dict().pop("amenities", None))

    return jsonify(filtered_places), 200
