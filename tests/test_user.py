
import unittest

from flask import json
from app import create_app, db
from instance.config import app_config
from tests.base_test import BaseTest
from app.models import User, BucketList, BucketListItems

class UserTests(BaseTest):
    """Creates class for testing user edge cases"""
    def setUp(self):
        self.app = create_app('testing')
        #gets the current state
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.user = {
            "first_name":"felistas",
             "last_name":"ngumi",
             "email":"felistaswaceerangumiiif@gmail.com",
             "password":"waceera",
             "verify_password":"waceera"
        }
    def test_create_user_successfully(self):
        """Asserts that a user can be created successfully"""
        response = self.client.post('/api/v1/auth/register',data=json.dumps(self.user))
        self.assertEquals(response.status_code, 200)
    def test_login_successful(self):
        """Asserts a user can login successfully"""
        response = self.client.post('/auth/login', data=json.dumps(self.login))
        self.assertEquals(response.status_code, 200)
    def test_login_with_invalid_email(self):
        """Asserts that a user cannot login with invalid email"""
        response = self.client.post('/auth/login', data=json.dumps(self.login_with_no_username))
        self.assertEquals(response.status_code, 401)
    def test_login_with_invalid_password(self):
        """Asserts user cannot login with invalid password"""
        response = self.client.post('/auth/login', data=json.dumps(self.login_with_no_password))
        self.assertEquals(response.status_code, 401)
    def test_login_with_no_credentials(self):
        """Asserts user cannot login with no credentials"""
        response = self.client.post('/auth/login', data=json.dumps(self.login_no_credentials))
        self.assertEquals(response.status_code, 401)
    def test_cannot_register_existing_user(self):
        """Asserts that an already existing user cannot register again"""
        self.client.post('/auth/register',data=json.dumps(self.user))
        register_user = self.client.post('/auth/register',data=json.dumps(self.user))
        self.assertEquals(response.status_code, 409)
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
