import unittest
from flask import json
from app import create_app, db
from instance.config import app_config
from app.models import User, BucketList, BucketListItems


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test cases"""
    def setUp(self):
        self.app = create_app('testing')
        #gets the current state
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.user = {
            'first_name': 'John',
            'last_name': 'Ngumi',
            'email': 'johnngumi@gmail.com',
            'password': '12345678',
            'verify_password': '12345678'
        }

        # User login
        self.login = {
            'email': 'johnngumi@gmail.com',
            'password': '12345678'
        }

        self.new_bucketlist = {
            'name': 'Learn German'
        }

        self.new_bucketlist_item = {
            'name': 'Download tutorials'
        }
    def create_user(self):
        created_user = self.client.post('/api/v1/auth/register',data=json.dumps(self.user),headers={"Content-Type": "application/json",'Accept': 'application/json'})
        return created_user
    def login(self):
        current_user = self.client.post('/api/v1/auth/login', data=json.dumps(self.login),headers={"Content-Type": "application/json", 'Accept': 'application/json'})
        return current_user
    def new_bucketlist(self):
        new_user = self.create_user()
        self.assertEqual(new_user.status_code, 201)
        logged_in_user = self.login()
        self.assertEqual(logged_in_user.status_code, 200)
        header={"Content-Type": "application/json", 'Accept': 'application/json'}
        header['Authorization'] = 'Bearer ' + json.loads(logged_in_user.data.decode())['token']
        new_bucket = self.client.post('/api/v1/bucketlists/', headers=header,data=json.dumps(self.new_bucketlist))
        return new_bucket

    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()
    #     self.app_context.pop()

    def test_create_bucketlist_successfully(self):
        """Test API can create a bucketlist succesfully"""
        new_bucket = self.new_bucketlist()
        print(new_bucket)
        self.assertEqual(new_bucket.status_code, 201)
    def test_cannot_create_existing_bucketlist(self):
        """Test API cannot create existing bucketlist"""
        first_bucketlist=self.new_bucketlist()
        second_bucketlist=self.new_bucketlist()
        self.assertEqual(second_bucketlist.status_code, 409)

    def test_list_all_bucketlists(self):
        """Test API can list all bucketlists"""
        response = self.client.get('/bucketlists/')
        self.assertEqual(response.status_code, 200)

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get bucketlist by id"""
        response = self.client.get('/bucketlists/1')
        self.assertEqual(response.status_code, 200)
    #
    # def test_create_bucketlist_item_successfully(self):
    #     """Test API can create a bucketlist item successfully"""
    #     response = self.client.post('/bucketlists/1/items',data=json.dumps(self.new_bucketlist_item))
    #     self.assertEqual(response.status_code, 201)
    #
    # def test_cannot_create_bucketlist_if_unauthorized(self):
    #     """Test cannot create bucketlist if unauthorized"""
    #     #add unauthorized user
    #     response = self.client.post('/bucketlists/',data=json.dumps(self.new_bucketlist))
    #     self.assertEqual(response.status_code, 401)
    #
    # def test_cannot_list_all_bucketlists_if_unauthorized(self):
    #     """Test API cannot list all bucketlists if unauthorized"""
    #     #add unauthorized user
    #     response = self.client.get('/bucketlists/')
    #     self.assertEqual(response.status_code, 401)
    #
    # def test_api_can_cannot_get_bucketlist_by_id_if_unauthorized(self):
    #     """Test API cannot get bucketlist by id if unauthorized"""
    #     #add unauthorized user
    #     response = self.client.get('/bucketlists/1')
    #     self.assertEqual(response.status_code, 401)
    #
    # def test_cannot_create_bucketlist_item_if_unauthorized(self):
    #     """Test API cannot create a bucketlist item if unauthorized"""
    #     #add unauthorized user
    #     response = self.client.post('/bucketlists/1/items',data=json.dumps(self.new_bucketlist_item))
    #     self.assertEqual(response.status_code, 401)
    #
    # def test_edit_bucketlist(self):
    #     """Test API can edit bucketlist successfully"""
    #     self.new_bucketlist = {
    #         'id': 2,
    #         'name': 'Learn French',
    #     }
    #     response = self.client.put('/bucketlists/',data=json.dumps(self.new_bucketlist))
    #     self.assertEqual(response.status_code, 201)
    #
    # def test_delete_bucketlist_successfully(self):
    #     """Test API can delete a bucketlist successfully"""
    #     response = self.client.delete('/bucketlist/1')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_delete_item_successfully(self):
    #     """Test one can delete an item successfully"""
    #     response = self.client.delete('/bucketlists/1/items/1/')
    #     self.assertEqual(response.status_code, 200)
