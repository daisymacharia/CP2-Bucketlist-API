import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from app import db

class User(db.Model):
    """Defines the user model"""
    __tablename__ = "user"
    user_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name= db.Column(db.String(50), nullable=False)
    email= db.Column(db.String(50), unique=True,nullable=False)
    password= db.Column(db.String(30), nullable=False)

    def __repr__(self):
        """returning a printable version for the object"""
        return "<UserModel: {}>".format(self.first_name)
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

class BucketList(db.Model):
    """Defines the bucketlist model"""
    __tablename__ = "bucketlist"
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable= False)
    name = db.Column(db.String(50), nullable=False)
    items = db.relationship("bucketlistitem", backref="bucketlists",
                            cascade='all, delete-orphan', lazy='dynamic')
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())




class BucketListItems(db.Model):
    """Defines the bucketlist item model"""
    __tablename__= "bucketlistitem"
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())
    done = db.Column(db.Boolean, default=False)
