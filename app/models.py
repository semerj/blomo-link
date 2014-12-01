from app import db
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(255), nullable=False, default='password')
    #reset_password_token = db.Column(db.String(100), nullable=False, default='')
    email = db.Column(db.String(120), index=True, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    links = db.relationship('Link', backref='author', lazy='dynamic')
    #active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.timestamp = datetime.datetime.utcnow()

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

    def __init__(self, longurl, shorturl):
        self.longurl = longurl
        self.shorturl = shorturl
        self.timestamp = datetime.datetime.utcnow()

    def __repr__(self):
        return '<long %r, short %r>' % (self.longurl, self.shorturl)


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