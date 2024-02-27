#!/usr/bin/python3
"""Add view for object"""

from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
