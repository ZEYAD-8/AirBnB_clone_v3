#!/usr/bin/python3
""" starts a Flask web application ( api for AirBnB_clone_v3 ) """

from api.v1.views import app_views
from models import storage
from flask import Flask
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(self):
    """Closes the current SQLAlchemy Session"""
    return storage.close()


if __name__ == '__main__':
    my_host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    my_port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=my_host, port=my_port, threaded=True)
