import sys

from flask import Flask
from flask_mongoalchemy import MongoAlchemy

from app.config import DevelopmentConfig

db = MongoAlchemy()

app = Flask(__name__)


def create_app(mode):
    if mode == "dev":
        app.config.from_object(DevelopmentConfig)
    else:
        print("Mode is not specified")
        sys.exit(1)

    db.init_app(app)

    return app


from app import models
from app import views
