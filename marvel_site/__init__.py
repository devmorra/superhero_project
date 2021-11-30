from flask import Flask
from config import Config
from .site.routes import site
from .auth.routes import auth
from .api.routes import api

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .models import db as root_db, loginManager, ma
from flask_cors import CORS
from marvel_site.helpers import JSONEncoder

app = Flask(__name__, template_folder="main_templates")

app.register_blueprint(site)
app.register_blueprint(api)
app.register_blueprint(auth)

app.config.from_object(Config)

root_db.init_app(app)
loginManager.init_app(app)
loginManager.login_view = 'auth.signin' # specify which page to load for non-authenticated users
ma.init_app(app)

migrate = Migrate(app, root_db)

cors = CORS(app)

app.json_encoder = JSONEncoder
