import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


class DevConfig(object):
    # Flask core
    # APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    # PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG = True
    JSON_SORT_KEYS = False
    BCRYPT_LOG_ROUNDS = 13
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask Jwt extended
    # for more info either look at the offical page or jwt_manager.py file
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET', 'JWT_SUPER_SECRET')
    JWT_ALGORITHM = 'HS512'
    JWT_AUTH_USERNAME_KEY = 'username'
    JWT_AUTH_HEADER_PREFIX = 'Bearer'
    JWT_EXPIRATION_DELTA = datetime.timedelta(days=60)
    JWT_AUTH_URL_RULE = '/api/users/login'

    # CORS
    CORS_ORIGIN_WHITELIST = [
        'http://localhost:4000'
    ]


class ProdConfig(object):
    pass
