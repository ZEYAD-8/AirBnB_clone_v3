#!/usr/bin/python3
"""
Handles all amenities links with places routes in the API
"""

from flask import jsonify, abort, make_response
from models.place import Place
from models.amenity import Amenity
from models import storage, storage_t
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities',
                 methods=["GET"], strict_slashes=False)
def all_amenities_by_place(place_id):
    """ returns all amenities linked to the specified place """
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)

    if storage_t == "db":
        amenity_list = place.amenities
    else:
        amenity_list = place.amenities()

    amenity_list = [amenity.to_dict() for amenity in amenity_list]
    return jsonify(amenity_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    """ delets the amenity from the specified place """
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return abort(404)

    if storage_t == "db":
        place_amenities_list = place.amenities
    else:
        place_amenities_list = place.amenities()

    is_linked = False
    for p_am in place_amenities_list:
        if p_am.id == amenity.id:
            is_linked = True

    if not is_linked:
        return abort(404)

    if storage_t == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity.id)

    place.save()
    return make_response({}, 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=["POST"], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """ links an amenity to the place specified """
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return abort(404)

    if storage_t == "db":
        place_amenities_list = place.amenities
    else:
        place_amenities_list = place.amenities()

    is_linked = False
    for p_am in place_amenities_list:
        if p_am.id == amenity.id:
            is_linked = True

    if is_linked:
        return jsonify(amenity.to_dict()), 200

    if storage_t == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)

    place.save()
    return jsonify(amenity.to_dict()), 201
