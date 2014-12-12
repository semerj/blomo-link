import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'password'

# to run w/ mysql locally
SQLALCHEMY_DATABASE_URI = 'mysql://apps:password@localhost/apps'

# for heroku
# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
