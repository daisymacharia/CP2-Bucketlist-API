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
