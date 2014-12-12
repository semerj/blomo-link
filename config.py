import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'jimblomo'

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

