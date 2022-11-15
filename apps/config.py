import os

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    # SECRET_KEY = config('SECRET_KEY'  , default='S#perS3crEt_007')
    # SECRET_KEY = os.getenv('SECRET_KEY', 'S#perS3crEt_007')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask-mongoengine
    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGODB_HOST'),
        'password': os.environ.get('MONGODB_PASSWORD', None),
        'username': os.environ.get('MONGODB_USERNAME', None),
        'tz_aware': True,
    }

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')

class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_ENGINE'   , 'mysql'),
        os.getenv('DB_USERNAME' , 'appseed_db_usr'),
        os.getenv('DB_PASS'     , 'pass'),
        os.getenv('DB_HOST'     , 'localhost'),
        os.getenv('DB_PORT'     , 3306),
        os.getenv('DB_NAME'     , 'appseed_db')
    )

    # flask-mongoengine
    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGODB_HOST'),
        'password': os.environ.get('MONGODB_PASSWORD', None),
        'username': os.environ.get('MONGODB_USERNAME', None),
        'tz_aware': True,
    }

class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
# 根據key選擇配置
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
