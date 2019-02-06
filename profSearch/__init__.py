from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from profSearch.config import *

app = Flask(__name__)

app.config.from_object(ProductionConfig)

db = SQLAlchemy(app)

from profSearch.professors.routes import professors
from profSearch.main.routes import main
from profSearch.classroom.routes import classrooms
from profSearch.api.routes import api
# подключение модулей
app.register_blueprint(classrooms)
app.register_blueprint(professors)
app.register_blueprint(main)
app.register_blueprint(api)
