import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'password'

#SQLALCHEMY_DATABASE_URI = 'mysql://apps:password@localhost/apps'
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']