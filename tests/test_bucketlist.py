import unittest
from flask import json
from app import create_app
from instance.config import app_config
# from app.models import User, BucketList, BucketListItems, db



class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test cases"""
    def setUp(self):
        self.app = create_app('testing')
        with self.app.app_context():
            from app.models import db, User, BucketList, BucketListItems
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
        new_user = self.create_user()
        logged_in_user = self.login_user()
        self.header={"Content-Type": "application/json",
                     'Accept': 'application/json'}
        self.header['Authorization'] = 'Bearer ' + json.loads(
            logged_in_user.get_data(as_text=True))['token']
        self.new_bucketlist = {
            'name': 'Learn German'
        }

        self.new_bucketlist_item = {
            'name': 'Download tutorials'
        }

    def create_user(self):
        created_user = self.client.post(
            '/api/v1/auth/register',data=json.dumps(self.user),
            headers={"Content-Type": "application/json",
                     'Accept': 'application/json'})
        return created_user
    def login_user(self):
        current_user = self.client.post(
            '/api/v1/auth/login', data=json.dumps(self.login),
            headers={"Content-Type": "application/json",
                     'Accept': 'application/json'})
        return current_user
    def new_bucket_list(self):
        new_bucket = self.client.post('/api/v1/bucketlists/',
                                      headers=self.header,
                                      data=json.dumps(self.new_bucketlist))
        return new_bucket

    def tearDown(self):
        with self.app.app_context():
            from app.models import db, User, BucketList, BucketListItems
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_bucketlist_successfully(self):
        """Test API can create a bucketlist succesfully"""
        new_bucket = self.new_bucket_list()
        self.assertEqual(json.loads(new_bucket.get_data(as_text=True))
                         ['status'], 201)
    def test_cannot_create_existing_bucketlist(self):
        """Test API cannot create existing bucketlist"""
        first_bucketlist=self.new_bucket_list()
        second_bucketlist=self.new_bucket_list()
        self.assertEqual(json.loads(second_bucketlist.get_data(as_text=True))
                         ['status'], 409)

    def test_delete_bucketlist_successfully(self):
        """Test API can delete a bucketlist successfully"""
        self.new_bucket_list()
        response = self.client.delete('/api/v1/bucketlists/1',headers=self.header)
        print(json.loads(response.get_data(as_text=True)))
        self.assertEqual(json.loads(response.get_data(as_text=True))['status'], 200)

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get bucketlist by id"""
        self.new_bucket_list()
        response = self.client.get('/api/v1/bucketlists/1',headers=self.header)
        self.assertEqual(response.status_code, 200)

    def test_create_bucketlist_item_successfully(self):
        """Test API can create a bucketlist item successfully"""
        self.new_bucket_list()
        response = self.client.post('/api/v1/bucketlists/1/items/',
                                    headers=self.header,
                                    data=json.dumps(self.new_bucketlist_item))
        self.assertEqual(json.loads(response.get_data(as_text=True))['status'],
                        201)

    def test_cannot_create_bucketlist_if_unauthorized(self):
        """Test cannot create bucketlist if unauthorized"""
        #add unauthorized user
        response = self.client.post('/api/v1/bucketlists/',
                                    data=json.dumps(self.new_bucketlist))
        self.assertEqual(response.status_code, 401)

    def test_cannot_list_all_bucketlists_if_unauthorized(self):
        """Test API cannot list all bucketlists if unauthorized"""
        #add unauthorized user
        response = self.client.get('/api/v1/bucketlists/')
        self.assertEqual(response.status_code, 401)

    def test_api_can_cannot_get_bucketlist_by_id_if_unauthorized(self):
        """Test API cannot get bucketlist by id if unauthorized"""
        #add unauthorized user
        response = self.client.get('/api/v1/bucketlists/1')
        self.assertEqual(response.status_code, 401)

    def test_cannot_create_bucketlist_item_if_unauthorized(self):
        """Test API cannot create a bucketlist item if unauthorized"""
        #add unauthorized user
        response = self.client.post('/api/v1/bucketlists/1/items/',
                                    data=json.dumps(self.new_bucketlist_item))
        self.assertEqual(response.status_code, 401)

    def test_edit_bucketlist(self):
        """Test API can edit bucketlist successfully"""
        self.new_bucket_list()
        edit_bucketlist = {
            'name': 'Learn French'
        }
        response = self.client.put('/api/v1/bucketlists/1',
                                   headers=self.header,
                                   data=json.dumps(edit_bucketlist))
        self.assertEqual(response.status_code, 200)

    def test_delete_item_successfully(self):
        """Test one can delete an item successfully"""
        self.new_bucket_list()
        response = self.client.post('/api/v1/bucketlists/1/items/',
                                    headers=self.header,
                                    data=json.dumps(self.new_bucketlist_item))
        response = self.client.delete('/api/v1/bucketlists/1/items/1',
                                      headers=self.header)
        self.assertEqual(response.status_code, 200)
    def test_edit_bucketlist_item_successfully(self):
        """Assert updating item successfully"""
        update_item = {"name":"ride"}
        self.new_bucket_list()
        response = self.client.post('/api/v1/bucketlists/1/items/',
                                    headers=self.header,
                                    data=json.dumps(self.new_bucketlist_item))
        response = self.client.put('/api/v1/bucketlists/1/items/1',
                                   headers=self.header,
                                   data=json.dumps(update_item))
        self.assertEqual(response.status_code, 200)
    def test_cannot_get_bucketlist_item_if_unauthorized(self):
        """Assert that cannot list item if unauthorized"""
        self.new_bucket_list()
        response = self.client.post('/api/v1/bucketlists/1/items/',
                                    headers=self.header,
                                    data=json.dumps(self.new_bucketlist_item))
        response = self.client.get('/api/v1/bucketlists/1/items/1')
        self.assertEqual(response.status_code, 401)
    def test_cannot_get_item_if_non_existent(self):
        """Assert that cannot list item if unauthorized"""
        response = self.client.get('/api/v1/bucketlists/1/items/1')
        self.assertEqual(response.status_code, 401)
    def test_cannot_create_already_existing_item(self):
        """Assert that one cannot create an aleady existing item"""
        self.new_bucket_list()
        self.client.post('/api/v1/bucketlists/1/items/',
                         headers=self.header,
                         data=json.dumps(self.new_bucketlist_item))
        existing_item = self.client.post('/api/v1/bucketlists/1/items/',
                                         headers=self.header,
                                         data=json.dumps(
                                             self.new_bucketlist_item))
        self.assertEqual(
            json.loads(existing_item.get_data(as_text=True))['status'], 409)
    def test_cannot_create_item_if_name_not_provided(self):
        """Assert cannot create bucketlist item if no items are provided"""
        self.new_bucket_list()
        no_data = {}
        item = self.client.post('/api/v1/bucketlists/1/items/',
                                headers=self.header, data=json.dumps(no_data))
        self.assertEqual(json.loads(item.get_data(as_text=True))['status'], 400)
    def test_cannot_get_item_for_wrong_url(self):
        """Asserts that one cannot get an item for the wrong url"""
        self.new_bucket_list()
        self.client.post('/api/v1/bucketlists/1/items/',
                         headers=self.header,
                         data=json.dumps(self.new_bucketlist_item))
        response = self.client.get('/api/v1/bucketlists/1/item/12')
        self.assertEqual(response.status_code, 404)
