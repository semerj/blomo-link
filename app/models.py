from app import db
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    #password = db.Column(db.String(255), nullable=False, default='')
    #reset_password_token = db.Column(db.String(100), nullable=False, default='')
    email = db.Column(db.String(120), index=True, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    links = db.relationship('Link', backref='author', lazy='dynamic')

    def is_authenticated(self):
        '''Return True if the user is authenticated.'''
        return True

    def is_active(self):
        '''True, as all users are active'''
        return True

    def is_anonymous(self):
        '''False, as anonymous users aren't supported.'''
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<user %r>' % (self.username)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    longurl = db.Column(db.String(140), index=True)
    shorturl = db.Column(db.String(140), index=True, unique=True)
    timestamp = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<long %r, short %r>' % (self.longurl, self.shorturl)
'''

# http://pythonhosted.org/Flask-User/data_models.html#all-in-one-user-datamodel
# Define User model. Make sure to add flask.ext.user UserMixin !!!
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # User Authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    reset_password_token = db.Column(db.String(100), nullable=False, default='')

    # User Email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')

    def is_active(self):
        return self.is_enabled

# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
user_manager = UserManager(db_adapter, app)     # Initialize Flask-User
'''

'''
# https://blog.openshift.com/use-flask-login-to-add-user-authentication-to-your-python-application/
class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(10))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)
 
    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)
'''