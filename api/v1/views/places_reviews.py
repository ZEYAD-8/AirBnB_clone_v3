#!/usr/bin/python3
"""
Handles all review routes in the API
"""

from flask import jsonify, abort, make_response, request
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=["GET"], strict_slashes=False)
def all_reviews_by_place(place_id):
    """ returns all reviews linked to the specified place """
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)

    reviews_list = place.reviews
    reviews_list = [review.to_dict() for review in reviews_list]
    return jsonify(reviews_list)


@app_views.route('places/<place_id>/reviews',
                 methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """ Creates a new review and links it to the place and user specified """
    try:
        review_dict = request.get_json()
    except Exception:
        return make_response(jsonify("Not a JSON"), 400)

    if "user_id" not in review_dict:
        return make_response(jsonify("Missing user_id"), 400)

    if "text" not in review_dict:
        return make_response(jsonify("Missing text"), 400)

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    user = storage.get(User, review_dict["user_id"])
    if user is None:
        abort(404)

    review_dict["place_id"] = place_id
    created = Review(**review_dict)
    created.save()
    return jsonify(created.to_dict()), 201


@app_views.route('/reviews/<id>', methods=["GET"], strict_slashes=False)
def get_review_by_id(id):
    """ return the review related to that specific id """
    review = storage.get(Review, id)
    if not review:
        return abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<id>', methods=["DELETE"], strict_slashes=False)
def delete_review_by_id(id):
    """ delets the review related to that specific id """
    review = storage.get(Review, id)
    if not review:
        return abort(404)

    review.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('/reviews/<id>', methods=["PUT"], strict_slashes=False)
def modify_review(id):
    """ Modifies an existing review """
    try:
        review_dict = request.get_json()
    except Exception:
        return make_response(jsonify("Not a JSON"), 400)

    review = storage.get(Review, id)
    if not review:
        return abort(404)

    for key, value in review_dict.items():
        if key in ["id", "created_at", "updated_at", "place_id", "user_id"]:
            continue
        setattr(review, key, value)

    review.save()
    return make_response(jsonify(review.to_dict()), 200)
