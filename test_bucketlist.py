import unittest
from flask import json
from app import create_app, db
from instance.config import app_config
from app.models import User, BucketList, BucketListItems



class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test cases"""

    def setUp(self):
        self.app = app_config('testing')
        #gets the current state
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.new_bucketlist = {
            'id': 1,
            'name': 'Learn German',
            'date_created': '2017-05-14 16:43:15',
            'date_modified': '2017-05-30 16:43:15',
            'created_by': 1
        }

        self.new_item = {
            'item_id': 1,
            'item_name': 'Download tutorials',
            'date_created': '2017-05-14 16:45:17',
            'date_modified': '2017-06-1 18:04:10',
            'status': 'False'
        }
