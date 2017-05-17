import unittest
from flask import json
from instance.config import app_config
from app.models import User, BucketList, BucketListItems
from app import create_app, db


class BaseTest(unittest.TestCase):
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
            'password': '1234',
            'verify_password': '1234'
        }

        # User login
        self.login = {
            'username': 'felistaswaceera@gmail.com',
            'password': '1234'
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
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
