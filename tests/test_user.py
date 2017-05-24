import os
import unittest
from flask import json
from instance.config import app_config
from app.models import User, BucketList, BucketListItems
from app import create_app
from tests.base_test import BaseTest
from instance.config import app_config
from app.models import User, BucketList, BucketListItems,db

class UserTests(BaseTest):
    """Creates class for testing user edge cases"""
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    #
    # def create_user(self):
    #     self.user = {
    #         'first_name': 'Felistas',
    #         'last_name': 'Ngumi',
    #         'email': 'felistaswaceera@gmail.com',
    #         'password': '1234',
    #         'verify_password': '1234'
    #     }
    def get_accept_content_type_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json' }
    def get_authentication_headers(self, username, password):
        authentication_headers = self.get_accept_content_type_headers()
        authentication_headers['Authorization'] = 'Basic ' + b64encode((username + ':' + password).encode('utf- 8')).decode('utf-8')
        return authentication_headers
    def create_user(self, name, password):
        # url = url_for('api.userlistresource', _external=True)
        user = {
            'first_name': 'Felistas',
            'last_name': 'Ngumi',
            'email': 'felistaswaceera@gmail.com',
            'password': '1234',
            'verify_password': '1234'
            }
        response = self.client.post('/api/v1/auth/register', headers=self.get_accept_content_type_headers(), data=json.dumps(user))
        return response

    def test_create_user_successfully(self):
        """Asserts that a user can be created successfully"""
        response = self.create_user(self.test_user_name,self.test_user_password)
        self.assertEquals(response.status_code, 200)
    def test_login_successful(self):
        """Asserts a user can login successfully"""
        data = {
                 "email":"felistaswaceera@gmail.com",
                 "password":"waceera"
                }
        response = self.client.post('api/v1/auth/login', data=data)
        self.assertEquals(response.status_code, 200)

    def test_login_with_invalid_password(self):
        """Asserts user cannot login with invalid password"""
        data = {
                 "email":"felistaswaceera@gmail.com",
                 "password":"waceera1"
                }
        response = self.client.post('api/v1/auth/login', data=data)
        self.assertEquals(response.status_code, 400)
    def test_login_with_no_credentials(self):
        """Asserts user cannot login with no credentials"""
        data = {
                 "email":" ",
                 "password":" "
                }
        response = self.client.post('api/v1/auth/login', data=data)
        self.assertEquals(response.status_code, 400)
    def test_cannot_register_existing_user(self):
        """Asserts cannot register an already existing user"""
        self.client.post('/api/v1/auth/register',data=json.dumps(self.user))
        response = self.client.post('/api/v1/auth/register',data=json.dumps(self.user))
        self.assertEquals(response.status_code, 409)
