
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from api.resources import UserRegisterApi, UserLoginApi, BucketlistApi,
      BucketlistsApi, BucketlistItemApi, BucketlistItemsApi

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)
    api.add_resource(UserRegisterApi, '/api/v1/auth/login', endpoint='user_registration')
    api.add_resource(UserLoginApi, '/api/v1/auth/register',endpoint='user_login')
    api.add_resource(BucketlistsApi, '/api/v1 /bucketlists/',endpoint='bucketlists')
    api.add_resource(BucketlistApi, '/api/v1/bucketlists/<int: id>',endpoint='bucketlist')
    api.add_resource(BucketlistItemsApi, '/api/v1/bucketlists/<int: id>/items/',endpoint='bucketlistitems')
    api.add_resource(BucketlistItemApi,'/api/v1/bucketlists/<int: id>/items/<int: item_id>',endpoint='bucketlistitem’)



    return app
