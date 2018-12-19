from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from profSearch.config import *
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)
app.config.from_object(StagingConfig)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

from profSearch.professors.routes import professors
from profSearch.main.routes import main
app.register_blueprint(professors)
app.register_blueprint(main)
