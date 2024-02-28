#!/usr/bin/python3
"""
Create Flask app; and register the blueprint app_views to Flask instance app.
"""


from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)

# enable CORS and allow for origins:
CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})

app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def downtear_engine(exceptyion):
    '''
    Removes the current SQLAlchemy Session object after each request.
    '''
    storage.close()


# Error handlers for expected app behavior:
@app.errorhandler(404)
def page_not_found(error):
    '''return render_template'''
    return jsonify('error='Not found'), 404


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
