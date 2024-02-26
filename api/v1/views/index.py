#!/usr/bin/python3
"""
Returns the status of the api
"""

from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """ return the status """
    status = {"status": "OK"}
    return jsonify(status)

@app_views.route("/stats", strict_slashes=False)
def num_obj():
    """retrieves the number of each object by type"""
    return jsonify({
        "amenities": models.storage.count(Amenity),
        "cities": models.storage.count(City),
        "places": models.storage.count(Place),
        "reviews": models.storage.count(Review),
        "states": models.storage.count(State),
        "users": models.storage.count(User)
    })
