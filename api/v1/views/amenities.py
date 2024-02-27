#!/usr/bin/python3
"""Add view for object"""

from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, request
