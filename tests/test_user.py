import os
import unittest
from flask import json
from app import create_app
from instance.config import app_config
from app.models import db, User,BucketList,BucketListItems

class UserTest(unittest.TestCase):
    """Creates class for testing user edge cases"""
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.client = self.app.test_client()

        self.user = {
            'first_name': 'Felistas',
            'last_name': 'Ngumi',
            'email': 'felistaswambugu@gmail.com',
            'password': '12345678',
            'verify_password': '12345678'
        }
        self.wrong_password = {
            'first_name': 'Felistas',
            'last_name': 'Ngumi',
            'email': 'felistaswambugu@gmail.com',
            'password': '12345678',
            'verify_password': '1234567'
        }
        self.no_data = {

        }
        # User login
        self.login = {
            'email': 'felistaswambugu@gmail.com',
            'password': '12345678'
        }

        # Login with no username
        self.login_with_no_username = {
            'email': '',
            'password': '12345678'
        }

        # Login with no password
        self.login_with_no_password = {
            'email': 'felistaswaceera@gmail.com',
            'password': ''
        }

        # Login with no username and password
        self.login_no_credentials = {
        }
        self.invalid_password = {
            'email': 'felistaswaceera@gmail.com',
            'password': '1234'
        }
        self.login_wrong_email = {
            "email": "felistas@gmail.com",
            'password': '1234'
        }


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_create_user_successfully(self):
        """Asserts that a user can be created successfully"""
        response = self.client.post('/api/v1/auth/register',
                                    data=json.dumps(self.user),
                                    headers={
                                        "Content-Type": "application/json",
                                        'Accept': 'application/json'})
        self.assertEquals(response.status_code, 200)
    def test_login_successful(self):
        """Asserts a user can login successfully"""
        self.client.post('/api/v1/auth/register',data=json.dumps(self.user),
                         headers={
                             "Content-Type": "application/json",
                             'Accept': 'application/json'})
        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(self.login),
                                    headers={
                                        "Content-Type": "application/json",
                                         'Accept': 'application/json'})
        self.assertEqual(response.status_code, 200)

    def test_login_with_invalid_password(self):
        """Asserts user cannot login with invalid password"""
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.user),
                         headers={
                             "Content-Type": "application/json",
                             'Accept': 'application/json'})
        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(self.invalid_password),
                                    headers = {
                                        "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
    def test_login_with_no_credentials(self):
        """Asserts user cannot login with no credentials"""
        self.client.post('/api/v1/auth/register',data=json.dumps(self.user),
                         headers={"Content-Type": "application/json",
                                  'Accept': 'application/json'})
        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(self.invalid_password),
                                    headers = {
                                        "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)

    def test_login_with_no_username(self):
        """Asserts user cannot login with no username"""
        self.client.post('/api/v1/auth/register',data=json.dumps(self.user),
                         headers={"Content-Type": "application/json",
                                  'Accept': 'application/json'})
        response = self.client.post('/api/v1/auth/login/',
                                    data=json.dumps(
                                        self.login_with_no_username),
                                    headers = {
                                        "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 404)

    def test_login_with_no_password(self):
        """Asserts user cannot login with no password"""
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.user),
                         headers={"Content-Type": "application/json",
                                  'Accept': 'application/json'})
        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(
                                        self.login_with_no_password),
                                    headers = {
                                        "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)

    def test_create_user_with_password_mismatch(self):
        """Asserts user cannot be created successfully with wrong passwords"""
        response = self.client.post('/api/v1/auth/register',
                                    data=json.dumps(self.wrong_password),
                                    headers={"Content-Type": "application/json",
                                             'Accept': 'application/json'})
        self.assertEquals(json.loads(
            response.get_data(as_text=True))['status'], 400)
    #
    def test_register_with_no_data(self):
        """Asserts that a user cannot register with no data"""
        response = self.client.post('/api/v1/auth/register',
                                    data=json.dumps(self.no_data),
                                    headers={"Content-Type": "application/json",
                                             'Accept': 'application/json'})
        self.assertEquals(json.loads(
            response.get_data(as_text=True))['status'], 400)

    def test_cannot_register_existing_user(self):
        """Asserts cannot register an already existing user"""
        self.client.post('/api/v1/auth/register',data=json.dumps(self.user),
                         headers={"Content-Type": "application/json",
                                  'Accept': 'application/json'})
        response = self.client.post('/api/v1/auth/register',
                                    data=json.dumps(self.user),
                                    headers={"Content-Type": "application/json",
                                             'Accept': 'application/json'})
        self.assertEquals(json.loads(
            response.get_data(as_text=True))['status'], 409)
    def test_cannot_login_with_no_data(self):
        """Asserts user cannot login if data is not provided"""
        self.client.post('/api/v1/auth/register',data=json.dumps(self.user),
                         headers={"Content-Type": "application/json",
                                  'Accept': 'application/json'})
        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(self.login_no_credentials),
                                    headers = {
                                        "Content-Type": "application/json"})
        self.assertEquals(json.loads(
            response.get_data(as_text=True))['status'], 400)
    def test_cannot_login_with_invalid_email(self):
        """Asserts that a user cannot login with invalid email"""
        self.client.post('/api/v1/auth/register',data=json.dumps(self.user),
                         headers={"Content-Type": "application/json",
                                  'Accept': 'application/json'})
        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(self.login_wrong_email),
                                    headers = {
                                        "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
