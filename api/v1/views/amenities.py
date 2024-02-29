#!/usr/bin/python3
"""
Handles all amenity routes in the API
"""

from flask import jsonify, abort, make_response, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def all_amenities():
    """ return the amenities """
    amenities = storage.all(Amenity).values()
    amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities)


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def create_amenity():
    """ Creates a new Amenity """
    try:
        amenity_dict = request.get_json()
    except Exception:
        return make_response(jsonify("Not a JSON"), 400)

    if "name" not in amenity_dict:
        return make_response(jsonify("Missing name"), 400)

    created = Amenity(**amenity_dict)
    created.save()
    return jsonify(created.to_dict()), 200


@app_views.route('/amenities/<id>', methods=["GET"], strict_slashes=False)
def get_amenity_by_id(id):
    """ return the amenity related to that specific id """
    amenity = storage.get(Amenity, id)
    if not amenity:
        return abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<id>', methods=["DELETE"], strict_slashes=False)
def delete_amenity_by_id(id):
    """ delets the amenity related to that specific id """
    amenity = storage.get(Amenity, id)
    if not amenity:
        return abort(404)

    amenity.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('/amenities/<id>', methods=["PUT"], strict_slashes=False)
def modify_amenity(id):
    """ Modifies an existing Amenity """
    try:
        amenity_dict = request.get_json()
    except Exception:
        return make_response(jsonify("Not a JSON"), 400)

    amenity = storage.get(Amenity, id)
    if not amenity:
        return abort(404)

    for key, value in amenity_dict.items():
        if key in ["id", "created_at", "updated_at"]:
            continue
        setattr(amenity, key, value)

    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
