from flask_restx import Namespace, Resource, fields
from app.services import facade

""" 
Namespace for place-related operations
"""
api = Namespace('places', description='Place operations')

"""
Place model for validation and documentation
"""

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'owner_id': fields.String(required=True, description='ID of the user who owns the place'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

@api.route('/')
class PlaceList(Resource):
    """
    Handles operations on the collection of places.
    """

    @api.expect(place_model, validate=True)
    @api.response(201, 'Place created successfully')
    @api.response(400, 'Invalid input')
    @api.response(404, 'Owner not found')
    def post(self):
        """
        Create a new place.
        Links the place to its owner and a list of amenities.
        """
        try:
            place_data = api.payload
            amenity_ids = place_data.pop('amenities', [])
            place = facade.create_place(place_data)

            for amenity_id in amenity_ids:
                amenity = facade.get_amenity(amenity_id)
                if amenity:
                    place.add_amenity(amenity)

            return place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved')
    def get(self):
        """
        Retrieve all places.
        """
        places = facade.get_all_places()
        return [p.to_dict() for p in places], 200

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    """
    Handles operations on a specific place.
    """

    @api.response(200, 'Place found')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get place details by ID.
        Includes detailed owner information.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        place_dict = place.to_dict()
        place_dict['owner'] = {
            'first_name': place.owner.first_name,
            'last_name': place.owner.last_name,
            'email': place.owner.email
        }
        return place_dict, 200

    @api.expect(place_model, validate=False)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """
        Update a place's information.
        Note: Amenities updates are handled separately.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        try:
            place_data = api.payload
            place_data.pop('amenities', None)
            facade.update_place(place_id, place_data)
            return facade.get_place(place_id).to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400