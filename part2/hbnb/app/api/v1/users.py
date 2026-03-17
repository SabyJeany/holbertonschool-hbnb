from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

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

    @jwt_required()  # Ensure the user is authenticated before allowing user creation
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Email already registered')
    def post(self):
        """
        Register a new user.
        Validates the input data and ensures the email is unique via the Facade.
        """
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
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

    @jwt_required()  # Ensure the user is authenticated before allowing updates
    @api.expect(user_model, validate=False)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """
        Update an existing user's profile.
        Partial updates are allowed as validation is set to False for this model.
        """
        claims = get_jwt()
        current_user_id = get_jwt_identity()
        is_admin = claims.get('is_admin', False)

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        # Admin path — can modify everything
        if is_admin:
            data = api.payload
            if 'email' in data:
                existing = facade.get_user_by_email(data['email'])
                if existing and existing.id != user_id:
                    return {'error': 'Email already in use'}, 400
            if 'password' in data:
                user.hash_password(data.pop('password'))
            facade.update_user(user_id, data)
            return facade.get_user(user_id).to_dict(), 200
    
        # Regular user path — can only modify their own profile, and not email/password
        if current_user_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        data = api.payload

        if 'email' in data or 'password' in data:
            return {'error': 'You cannot modify email or password'}, 400

        facade.update_user(user_id, data)
        return facade.get_user(user_id).to_dict(), 200