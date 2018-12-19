from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from profSearch.config import *

db = SQLAlchemy()

def create_app(config=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    from profSearch.professors.routes import professors
    from profSearch.main.routes import main
    app.register_blueprint(professors)
    app.register_blueprint(main)

    return app