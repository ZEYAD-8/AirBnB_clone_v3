#!/usr/bin/python3
"""
Handles all User routes in the API
"""

from flask import jsonify, abort, make_response, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', methods=["GET"], strict_slashes=False)
def all_users():
    """ return all Users """
    users = storage.all(User).values()
    users = [user.to_dict() for user in users]
    return jsonify(users)


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def create_user():
    """ Creates a new User """
    try:
        user_dict = request.get_json()
    except Exception:
        return make_response(jsonify("Not a JSON"), 400)

    if "email" not in user_dict:
        return make_response(jsonify("Missing email"), 400)
    
    if "password" not in user_dict:
        return make_response(jsonify("Missing password"), 400)

    created = User(**user_dict)
    created.save()
    return jsonify(created.to_dict()), 201


@app_views.route('/users/<id>', methods=["GET"], strict_slashes=False)
def get_user_by_id(id):
    """ return the user related to that specific id """
    user = storage.get(User, id)
    if not user:
        return abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<id>', methods=["DELETE"], strict_slashes=False)
def delete_user_by_id(id):
    """ delets the user related to that specific id """
    user = storage.get(User, id)
    if not user:
        return abort(404)

    user.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('/users/<id>', methods=["PUT"], strict_slashes=False)
def modify_user(id):
    """ Modifies an existing user """
    try:
        user_dict = request.get_json()
    except Exception:
        return make_response(jsonify("Not a JSON"), 400)

    user = storage.get(User, id)
    if not user:
        return abort(404)

    for key, value in user_dict.items():
        if key in ["id", "created_at", "updated_at", "email"]:
            continue
        setattr(user, key, value)

    user.save()
    return make_response(jsonify(user.to_dict()), 200)
