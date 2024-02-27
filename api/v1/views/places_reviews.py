#!/usr/bin/python3
"""Add view for object"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.review import Review
from models.place import Place
