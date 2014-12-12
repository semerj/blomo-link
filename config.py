import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'jimblomo'

# for heroku w/ postgres
# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# for local w/ mysql
SQLALCHEMY_DATABASE_URI = 'mysql://apps:password@localhost/apps'
