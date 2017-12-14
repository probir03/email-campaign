#!/usr/local/bin python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Command
from flask_migrate import Migrate, MigrateCommand
from __init__ import app, db
from models import *
# from managers import DripCampaign

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
# manager.add_command('run:campaign', DripCampaign)

if __name__ == '__main__':
    manager.run()
