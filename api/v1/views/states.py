#!/usr/bin/python3
"""Add view for object"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
