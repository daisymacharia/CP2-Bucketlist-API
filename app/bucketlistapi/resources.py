
from flask_restful import  Resource, abort
from flask import request,jsonify
from app.bucketlistapi.schema import (UserRegistrationSchema,
                                      UserLoginSchema,
                                      BucketListItemSchema,
                                      BucketListSchema)


user_register = UserRegistrationSchema()
user_login = UserLoginSchema()
bucket_list = BucketListSchema()
bucket_list_item = BucketListItemSchema()
class UserRegister(Resource):
    """Register user"""
    def post(self):
        data = request.get_json()
        if not data:
            response = {'error': 'No data provided'}
            return response, 400
        errors = user_register.validate(data)
        if errors:
            return errors, 400
        password = data['password']
        verify_password = data['verify_password']
        if password != verify_password:
            return 'Passwords dont match'

class UserLogin(Resource):
    """Login user"""
    pass


class Bucketlists(Resource):
    """Create and list bucketlists"""
    pass


class BucketlistsId(Resource):
    """get,update and delete bucketlists"""
    pass


class BucketlistItem(Resource):
    """Create new bucketlist item"""
    pass


class BucketlistItems(Resource):
    """Update and delete bucketlist items"""
    pass
