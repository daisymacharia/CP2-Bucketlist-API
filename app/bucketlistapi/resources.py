
from flask_restful import  Resource, abort
from flask import request,jsonify
from flask_httpauth import HTTPDigestAuth
from flask_httpauth import HTTPBasicAuth
from app.bucketlistapi.schema import (UserResigrationSchema,
                                      UserLoginSchema,
                                      BucketListItemSchema,
                                      BucketListSchema)


user_register = UserResigrationSchema()
user_login = UserLoginSchema()
bucket_list = BucketListSchema()
bucket_list_item = BucketListItemSchema()
class UserRegister(Resource):
    """Register user"""
    def post(self):
        data = request.get_json()
        print(data)
        if not data:
            response = {'error': 'No data provided'}
            return response, 400
        errors = user_register.validate(data)
        if errors:
            return errors
        email = data['email']
        email = User.query.filter_by(email=email).first()
        if email:
            response = {'error': 'Email already in use'}
            return response, 400
        try:
            #register user
            new_user = User(first_name,last_name,email,password)
            # new_user.first_name = first_name
            # new_user.last_name = last_name
            # username= first_name + last_name
            # new_user.email = email
            # new_user.password = password
            db.session.add(new_user)
            db.session.commit()
            return {'message': '{} added successfully'.format(username)}, 201
        except Exception as error:
            db.session.rollback()
            return {'error': '{} try again'.format(username)}, 400






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
