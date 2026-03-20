from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text content of the review'),
    'rating': fields.Integer(required=True, description='Rating between 1 and 5'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed'),
    'user_id': fields.String(required=True, description='ID of the user writing the review')
})

@api.route('/')
class ReviewList(Resource):
    """
    Handles operations on the global collection of reviews.
    """

    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review created successfully')
    @api.response(400, 'Invalid input')
    @api.response(404, 'User or Place not found')
    def post(self):
        """
        Create a new review.
        The facade ensures both the user and the place exist before creating.
        """
        current_user_id = get_jwt_identity()
        try:
            
            review_data = api.payload
            # We set `user_id` to the logged-in user
            review_data['user_id'] = current_user_id

            place = facade.get_place(review_data['place_id'])
            if not place:
                return {'error': 'Place not found'}, 404
            
            if place.owner.id == current_user_id:
                return {'error': 'You cannot review your own place'}, 400
            
            existing_review = facade.get_reviews_by_place(place.id)
            for review in existing_review:
                if review.user.id == current_user_id:
                    return {'error': 'You have already reviewed this place'}, 400
                
            review = facade.create_review(review_data)
            return review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of all reviews retrieved')
    def get(self):
        """
        Retrieve all reviews across the platform.
        """
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    """
    Handles operations on a specific review.
    """

    @api.response(200, 'Review found')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Get details of a single review by ID.
        """
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @jwt_required()
    @api.expect(review_model, validate=False)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """
        Update an existing review's text or rating.
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        if not is_admin and review.user.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.update_review(review_id, api.payload)
            return facade.get_review(review_id).to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """
        Delete a review from the system.
        """
        current_user_id = get_jwt_identity()
       
        claims = get_jwt()
        is_admin = claims.get('is_admin', False) 

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if not is_admin and review.user.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    """
    Handles fetching reviews filtered by a specific place.
    """

    @api.response(200, 'Reviews for place retrieved')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get all reviews for a specific place.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        reviews = facade.get_reviews_by_place(place_id)
        return [r.to_dict() for r in reviews], 200