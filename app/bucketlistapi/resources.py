from flask_restful import Api, Resource, fields, marshal_with, abort


class UserRegister(Resource):
    """Register user"""
    pass


class UserLogin(Resource):
    """Login user"""
    pass


class Bucketlists(Resource):
    """Create and list bucketlists"""
    pass


class BucketlistsId(Resource):
    """get,update and delete bucketlists"""
    pass


class BucketlistItem(Resource):
    """Create new bucketlist item"""
    pass


class BucketlistItems(Resource):
    """Update and delete bucketlist items"""
    pass
