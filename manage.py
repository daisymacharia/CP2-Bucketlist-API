# manage.py

import os
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app import models,db

app = create_app(config_name=os.getenv('APP_SETTINGS'))
with app.app_context():
    from app.models import db, User, BucketList, BucketListItems
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    """Creates database with tables"""
    os.system('createdb bucketlist_db')
    os.system('createdb bucketlist_db')
    db.create_all()
    db.session.commit()


@manager.command
def drop_db():
    """Deletes database"""
    os.system('dropdb bucketlist_db')
    os.system('dropdb bucketlist_db')


if __name__ == '__main__':
    manager.run()
