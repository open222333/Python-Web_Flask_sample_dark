from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from importlib import import_module


sqlalchemy = SQLAlchemy()
mongo = MongoEngine()
login_manager = LoginManager()


def register_extensions(app):
    sqlalchemy.init_app(app)
    mongo.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        sqlalchemy.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        sqlalchemy.session.remove()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app
