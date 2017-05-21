from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
#from app import *
# from bucketlistapi.resources import *
from app.bucketlistapi.resources import *

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # initialize app on the SQLAlchemy instance
    db.init_app(app)

    api = Api(app)

    api.add_resource(UserRegister, '/api/v1/auth/register',
                     endpoint='user_registration')
    api.add_resource(UserLogin, '/api/v1/auth/login',
                     endpoint='user_login')
    api.add_resource(Bucketlists, '/api/v1 /bucketlists/',
                     endpoint='bucketlists')
    api.add_resource(BucketlistsId, '/api/v1/bucketlists/<id>',
                     endpoint='bucketlist')
    api.add_resource(BucketlistItems, '/api/v1/bucketlists/<id>/items/',
                     endpoint='bucketlistitems')
    api.add_resource(BucketlistItem,
                     '/api/v1/bucketlists/<id>/items/<item_id>',
                     endpoint='bucketlistitem')
    return app
