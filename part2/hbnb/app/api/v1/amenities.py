from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity (e.g., Wi-Fi, Pool)')
})

@api.route('/')
class AmenityList(Resource):
    """
    Handles operations on the collection of amenities.
    Allows listing all amenities or creating a new one.
    """

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity created successfully')
    @api.response(400, 'Invalid input')
    def post(self):
        """
        Create a new amenity.
        Uses the facade to validate and store the amenity.
        """
        try:
            amenity = facade.create_amenity(api.payload)
            return amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities')
    def get(self):
        """
        Retrieve all amenities.
        Returns a list of all amenity objects in dictionary format.
        """
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    """
    Handles operations on a specific amenity instance.
    """

    @api.response(200, 'Amenity found')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get amenity details by its unique ID.
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model, validate=False)
    @api.response(200, 'Amenity updated')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input')
    def put(self, amenity_id):
        """
        Update an amenity's information.
        Catches ValueErrors if the new name violates validation rules.
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        try:
            facade.update_amenity(amenity_id, api.payload)
            return facade.get_amenity(amenity_id).to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400