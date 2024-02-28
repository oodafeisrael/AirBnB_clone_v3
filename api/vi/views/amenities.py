#!/usr/bin/python3
"""
Creates a view for Amenity objects - handles all default RESTful API actions.
"""

# Import necessary modules
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from datetime import datetime
import uuid


# Route for retrieving all Amenity objects
@app_views.route('/amenities/', methods=['GET'])
def list_amenities():
    '''Retrieves a list of all Amenity objects'''
    # list all Amenity objects from the storage
    list_amenities = [obj.to_dict() for obj in storage.all("Amenity").values()]
    # Convert objects to dictionaries and jsonify the list
    return jsonify(list_amenities)


# Route for retrieving a specific Amenity object by ID
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    '''Retrieves an Amenity object'''
    # Get the Amenity object with the given ID from the storage
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities
                   if obj.id == amenity_id]
    # Return 404 error if the Amenity object is not found
    if amenity_obj == []:
        abort(404)
    # Return the Amenity object in JSON format
    return jsonify(amenity_obj[0])


# Route for deleting a specific Amenity object by ID
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    '''Deletes an Amenity object'''
    # Get the Amenity object with the given ID from the storage
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        # Return 404 error if the Amenity object is not found
        abort(404)
    # Delete the Amenity object from the storage and save changes
    amenity_obj.remove(amenity_obj[0])
    for obj in all_amenities:
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
    # Return an empty JSON with 200 status code
    return jsonify({}), 200


# Route for creating a new Amenity object
@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''Creates an Amenity object'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        # Return 400 error if the request data is not in JSON format
        abort(400, 'Not a JSON')
    # Get the JSON data from the request
    data = request.get_json()
    if 'name' not in data:
        # Return 400 error if 'name' key is missing in the JSON data
        abort(400, 'Missing name')

    # Create a new Amenity object with the JSON data
    amenity = Amenity(**data)
    # Save the Amenity object to the storage
    amenity.save()
    # Return the newly created Amenity
    #   object in JSON format with 201 status code
    return jsonify(amenity.to_dict()), 201


# Route for updating an existing Amenity object by ID
@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updates_amenity(amenity_id):
    '''Updates an Amenity object'''
    # Get the Amenity object with the given ID from the storage
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    # Return 400 error if the request data is not in JSON format
    if not request.get_json():
        abort(400, 'Not a JSON')
    # Get the JSON data from the request
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    # Update the attributes of the Amenity object with the JSON data
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)

    # Save the updated Amenity object to the storage
    amenity.save()
    # Return the updated Amenity object in JSON format with 200 status code
    return jsonify(amenity.to_dict()), 200
    else:
        # Return 404 error if the Amenity object is not found
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    '''Returns 404: Not Found'''
    # Return a JSON response for 404 error
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    '''Return Bad Request message for illegal requests to the API.'''
    # Return a JSON response for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
