import os
from flask_migrate import Migrate
from flask_minify import Minify
from sys import exit

from apps.config import config_dict
from apps import create_app, mongo


try:
    # 配置設定
    DEBUG = (os.getenv('DEBUG', 'False') == 'True')
    get_config_mode = 'Debug' if DEBUG else 'Production'
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, mongo)

if not DEBUG:
    # Minify是用來壓縮JavaScritp跟CSS的PHP 5應用程式。
    Minify(app=app, html=True, js=False, cssless=False)

if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG))
    app.logger.info('FLASK_ENV        = ' + os.getenv('FLASK_ENV'))
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE')
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('DB               = ' + app_config.MONGODB_SETTINGS['host'])
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT)

if __name__ == "__main__":
    app.run()
