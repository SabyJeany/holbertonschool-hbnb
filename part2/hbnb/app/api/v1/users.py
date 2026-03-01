from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Unique email address'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/')
class UserList(Resource):
    """
    Handles operations on the collection of users, such as listing all users
    or creating a new user instance.
    """

    @api.expect(user_model, validate=True)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Email already registered')
    def post(self):
        """
        Register a new user.
        Validates the input data and ensures the email is unique via the Facade.
        """
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        
        user = facade.create_user(user_data)
        return user.to_dict(), 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """
        Retrieve all registered users.
        Returns a list of user objects in dictionary format.
        """
        users = facade.get_all_users()
        return [u.to_dict() for u in users], 200

@api.route('/<string:user_id>')
class UserResource(Resource):
    """
    Handles operations on a specific user identified by their unique ID.
    """

    @api.response(200, 'User found')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Fetch a single user's details by their ID.
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model, validate=False)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """
        Update an existing user's profile.
        Partial updates are allowed as validation is set to False for this model.
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        facade.update_user(user_id, api.payload)
        return facade.get_user(user_id).to_dict(), 200