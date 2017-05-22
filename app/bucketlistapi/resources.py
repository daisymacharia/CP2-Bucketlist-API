import re
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from flask_restful import  Resource, abort
from flask import request,jsonify
from models import User,BucketList,BucketListItems
from schema import (UserRegistrationSchema,
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
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        verify_password = data['verify_password']
        if password != verify_password:
            response = {'error': 'Passwords dont match'}
            return response, 400
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            response = {'error': 'Email already in use'}
            return response, 400
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
        errors = user_login.validate(login_data)
        if errors:
            return errors, 400
        email = login_data['email']
        password = login_data['password']
        email = User.query.filter_by(email=email).first()
        if not email:
            response = {'error': 'Email provided does not exist'}
            return response
        if user.verify_user_password(password):
            token = user.generate_auth_token()
            return 'Login successful'

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
