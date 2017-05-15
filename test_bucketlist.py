import unittest
from flask import json
from app import create_app, db
from instance.config import app_config
from app.models import User, BucketList, BucketListItems


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test cases"""

    def setUp(self):
        self.app = app_config['testing']
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

        self.new_bucketlist_item = {
            'item_id': 1,
            'item_name': 'Download tutorials',
            'date_created': '2017-05-14 16:45:17',
            'date_modified': '2017-06-1 18:04:10',
            'status': 'False'
        }
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_bucketlist_successfully(self):
        """Test API can create a bucketlist successfully"""
        response = self.client.post('/bucketlists/',data=json.dumps(self.new_bucketlist))
        self.assertEqual(response.status_code, 201)

    def test_list_all_bucketlists(self):
        """Test API can get list all bucketlists"""
        response = self.client.get('/bucketlists/',data=json.loads(self.new_bucketlist))
        self.assertEqual(response.status_code, 200)

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get bucketlist by id"""
        response = self.client.get('/bucketlists/1', data=json.loads(self.new_bucketlist))
        self.assertEqual(response.status_code, 200)

    def test_create_bucketlist_item_successfully(self):
        """Test API can create a bucketlist item successfully"""
        response = self.client.post('/bucketlists/id/items',data=json.dumps(self.new_bucketlist_item))
        self.assertEqual(response.status_code, 201)
