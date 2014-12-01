from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.user import login_required, UserManager, UserMixin, SQLAlchemyAdapter

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

#from flask.ext.login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views, models

#from models import User
#db_adapter = SQLAlchemyAdapter(db, User) 
#user_manager = UserManager(db_adapter, app)