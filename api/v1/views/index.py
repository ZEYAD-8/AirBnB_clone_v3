#!/usr/bin/python3
"""
Returns the status of the api
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.amenity import Amenity
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """ return the status """
    status = {
        "status": "OK"
    }
    return jsonify(status)


@app_views.route("/stats", strict_slashes=False)
def num_obj():
    """retrieves the number of each object by type"""
    return jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    })
