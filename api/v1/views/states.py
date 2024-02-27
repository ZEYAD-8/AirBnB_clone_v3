#!/usr/bin/python3
""" Handles all state routes in the API """

from flask import jsonify, abort, make_response, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def all_states():
    """ return the states """
    states = storage.all(State).values()
    states = [state.to_dict() for state in states]
    return jsonify(states)


@app_views.route('/states', methods=["POST"], strict_slashes=False)
def create_state():
    """ Creates a new State """
    try:
        state_dict = request.get_json()
    except Exception:
        return make_response(jsonify("Not a JSON"), 400)

    if "name" not in state_dict:
        return make_response(jsonify("Missing name"), 400)

    created = State(**state_dict)
    created.save()
    return make_response(jsonify(created.to_dict()), 200)


@app_views.route('/states/<id>', methods=["GET"], strict_slashes=False)
def get_state_by_id(id):
    """ return the state related to that specific id """
    state = storage.get(State, id)
    if not state:
        return abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<id>', methods=["DELETE"], strict_slashes=False)
def delete_state_by_id(id):
    """ delets the state related to that specific id """
    state = storage.get(State, id)
    if not state:
        return abort(404)

    state.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('/states/<id>', methods=["PUT"], strict_slashes=False)
def modify_state(id):
    """ Modifies an existing state """
    try:
        state_dict = request.get_json()
    except Exception:
        return make_response(jsonify("Not a JSON"), 400)

    state = storage.get(State, id)
    if not state:
        return abort(404)

    if "name" not in state_dict:
        return make_response(jsonify("Missing name"), 400)

    for key, value in state_dict.items():
        if key in ["id", "created_at", "updated_at"]:
            continue
        setattr(state, key, value)

    state.save()
    return make_response(jsonify(state.to_dict()), 200)
