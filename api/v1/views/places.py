#!/usr/bin/python3
"""Add view for object"""

from flask import jsonify, request
from models import storage
from models.place import Place
from api.v1.views import app_views
