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

