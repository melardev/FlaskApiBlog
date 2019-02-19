import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from config import DevConfig

# config = DevConfig if get_debug_flag() else ProdConfig
config = DevConfig

app = Flask(__name__, root_path=os.getcwd(), static_url_path='/static')
app.config.from_object(config)

basedir = os.path.abspath(os.path.dirname(__file__))

bcrypt = Bcrypt()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cache = Cache()
api = Api(app)

# cors with defaults, which means allow all domains, it is fine for the moment
cors = CORS(app)
