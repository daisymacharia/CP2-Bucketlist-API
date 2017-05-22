import os
import unittest
from flask import json
from instance.config import app_config
from app.models import User, BucketList, BucketListItems
from app import create_app
from instance.config import app_config
from app.models import User, BucketList, BucketListItems,db

class UserTests(unittest.TestCase):
    """Creates class for testing user edge cases"""
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # User registration
        self.user = {
            'first_name': 'Felistas',
            'last_name': 'Ngumi',
            'email': 'felistaswaceera@gmail.com',
            'password': '123456',
            'verify_password': '1234'
        }

        # User login
        self.login = {
            'username': 'felistaswaceera@gmail.com',
            'password': '123456'
        }

        # Login with no username
        self.login_with_no_username = {
            'username': '',
            'password': '1234'
        }

        # Login with no password
        self.login_with_no_password = {
            'username': 'felistaswaceera@gmail.com',
            'password': ''
        }

        # Login with no username and password
        self.login_no_credentials = {
            'username': '',
            'password': ''
        }


    def tearDown(self):
        # Delete the test database
        os.remove('/Users/Shera/Desktop/bucketlist/CP2-BUCKETLIST-APPLICATION/tests/test_bucketlist_db')
        self.app_context.pop()
    # def setUp(self):
    #     self.app = create_app('testing')
    #     self.app_context = self.app.app_context()
    #     self.app_context.push()
    #     db.create_all()
    #     self.client = self.app.test_client()
    def create_user(self):
        self.user = {
            'first_name': 'Felistas',
            'last_name': 'Ngumi',
            'email': 'felistaswaceera@gmail.com',
            'password': '1234',
            'verify_password': '1234'
        }

    def test_create_user_successfully(self):
        """Asserts that a user can be created successfully"""
        response = self.client.post('/api/v1/auth/register',data=json.dumps(self.user))
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
