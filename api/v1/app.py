#!/usr/bin/python3
"""Starts a Flask web application ( api for AirBnB_clone_v3 )"""

from models import storage
from flask import Flask
from os import getenv
from flask import jsonify
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """Closes the current SQLAlchemy Session"""
    return storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """returns a JSON-formatted 404 status code response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    my_host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    my_port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=my_host, port=my_port, threaded=True)
