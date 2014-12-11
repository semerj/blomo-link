from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
#from flask.ext.bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
#bcrypt = Bcrypt(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views, models
