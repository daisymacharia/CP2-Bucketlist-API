import re
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from flask_restful import  Resource, abort
from flask import request,jsonify,g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from models import User,BucketList,BucketListItems
from schema import (UserRegistrationSchema,
                                    UserLoginSchema,
                                    BucketListItemSchema,
                                    BucketListSchema)

auth = HTTPTokenAuth()
user_register_schema = UserRegistrationSchema()
user_login_schema = UserLoginSchema()
bucket_list_schema = BucketListSchema()
bucket_list_item_schema = BucketListItemSchema()

@auth.verify_token
def verify_user_token(token):
    verified_user = User.verify_auth_token(token)
    if type(verified_user) is not User:
        return False
    else:
        g.user = verified_user
        return True

class AuthResource(Resource):
    method_decorators = [auth.login_required]

class UserRegister(Resource):
    """Register user"""
    def post(self):
        data = request.get_json()
        if not data:
            response = jsonify({'Error': 'No data provided', 'status': 400})
            return response
        errors = user_register_schema.validate(data)
        if errors:
            return errors, 400
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        verify_password = data['verify_password']
        if password != verify_password:
            response = jsonify({'Error': 'Passwords dont match', 'status': 400})
            return response, 400
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            response = jsonify({'Error': 'Email already in use','status': 409 })
            return response
        new_user = User(first_name=first_name,last_name=last_name,email=email, password=password)
        new_user.add(new_user)
        new_user.hash_password(password)
        username = first_name + ' ' + last_name
        return {'message': '{} added successfully'.format(username)}, 201


class UserLogin(Resource):
    """Login user"""
    def post(self):
        login_data = request.get_json()
        if not login_data:
            return 'No data provided'
        errors = user_login_schema.validate(login_data)
        if errors:
            return errors, 400
        email = login_data['email']
        password = login_data['password']
        email = User.query.filter_by(email=email).first()
        if not email:
            response = jsonify({'Error': 'Email provided does not exist','status': 400})
            return response
        if email.verify_password(password):
            token = email.generate_auth_token()
            response = {'Message': 'Login successful','status': 200,
                                'token': token}
            return response
        else:
            response =jsonify({'Error': 'Wrong password', 'status':400})
            return response

class Bucketlists(AuthResource):
    """Creates a new bucketlist"""
    def post(self):
        bucketlist_data = request.get_json()
        if not bucketlist_data:
            response = jsonify({'Error': 'No data provided'})
            return response
        validation_errors = bucket_list_schema.validate(bucketlist_data)
        if validation_errors:
            return validation_errors, 400
        bucketlist_name = bucketlist_data['name']
        existing_bucketlist = BucketList.query.filter_by(name=bucketlist_name).first()
        if existing_bucketlist:
            response = jsonify({'Error': 'Bucketlist with the same name already exists','status': 400})
        new_bucketlist_name = BucketList(name=bucketlist_name)
        new_bucketlist_name.add(new_bucketlist_name)
        response = jsonify({'Message': 'Created bucketlist successfully','status': 200})
        return response


class BucketlistsId(AuthResource):
    """List by id,update and delete bucketlists"""
    def get(self, id):
        bucket = BucketList.query.filter_by(id=id).first()
        print(bucket)
        if not bucket:
            response = {'Error': 'The bucketlist requested does not exist','status': 400}
            return response
        return bucket_list.dump(bucket)
    def delete(self, id):
        bucket = BucketList.query.filter_by(id=id).first()
        if not bucket:
            response = jsonify({'Error': 'The bucketlist requested does not exist','status': 400})
        bucket.delete(bucket)
        return 'Successfully deleted'
    def put(self, id):
        bucket = BucketList.query.filter_by(id=id).first()
        if not bucket:
            response = jsonify({'Error': 'The bucketlist requested does not exist','status': 400})
        bucketlist_update = request.get_json()
        validation_errors = bucket_list.validate(bucketlist_update)
        if validation_errors:
            return validation_errors, 400
        bucket.update(bucket)
        return 'Successfully updated'


class BucketlistItem(Resource):
    """Create new bucketlist item"""
    pass


class BucketlistItems(Resource):
    """Update and delete bucketlist items"""
    pass
