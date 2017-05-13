from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime,Boolean,Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

import datetime
import sys
import os

Base = declarative_base()


class User(Base):
    """Defines the user model"""
    __tablename__ = "user"
    user_id = Column(Integer, autoincrement=True,primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name= Column(String(50), nullable=False)
    email= Column(String(50), unique=True,nullable=False)
    password= Column(String(30), nullable=False)

class BucketList(Base):
    """Defines the bucketlist model"""
    __tablename__ = "bucketlist"
    id = Column(Integer, autoincrement=True,primary_key=True)
    created_by = Column(Integer, ForeignKey("user.user_id"), nullable= False)
    name = Column(String(50), nullable=False)
    items = relationship('bucketlistitem',backref='bucketlist')
    date_created = Column(DateTime, default=datetime.datetime.now)
    date_modified = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.utcnow)

class BucketListItems(Base):
    """Defines the bucketlist item model"""
    __tablename__= "bucketlistitem"
    id = Column(Integer, autoincrement=True,primary_key=True)
    name = Column(String(50), nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.now)
    date_modified = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    status = Column(Boolean, default=False)



engine = create_engine('sqlite:///bucketlist.db')
Base.metadata.create_all(engine)
