from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from importlib import import_module
from authentication.models import Users
from authentication.util import hash_pass
import os


sqlalchemy = SQLAlchemy()
mongo = MongoEngine()
login_manager = LoginManager()


def register_extensions(app):
    '''初始化擴充套件'''
    sqlalchemy.init_app(app)
    mongo.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    '''載入藍圖'''
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):
    '''sqlalchemy 設定

    before_first_request
    註冊一個函數，在處理第一個請求之前執行
    before_request
    註冊一個函數，在每次請求之前執行
    after_request
    註冊一個函數，如果沒有未處理的異常拋出，在每次請求之後執行
    teardown_request
    註冊一個函數，如果有未處理的異常拋出，在每次請求之後執行
    '''

    @app.before_first_request
    def initialize_database():
        sqlalchemy.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        sqlalchemy.session.remove()


def create_root():
    '''mongodb創建初始root帳號'''
    Users(
        username='root',
        email=os.environ.get('ROOT_EMAIL', None),
        password=hash_pass(os.environ.get('ROOT_PASSWORD', 'root'))
    ).save()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app
